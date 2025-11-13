import os
import streamlit as st
import base64
from openai import OpenAI
import openai
from PIL import Image
from pathlib import Path
import paho.mqtt.client as mqtt
import json

# =========================================================
# MQTT CONFIG — WOKWI / ESP32
# =========================================================
MQTT_BROKER = "157.230.214.127"    # TU BROKER
MQTT_PORT = 1883
MQTT_TOPIC = "cmqtt_a"             # El canal que escucha tu ESP32

mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)

# =========================================================
# CSS — Fondo + estilos completos
# =========================================================
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

html, body, .stApp, .main {
  font-family: 'Inter', sans-serif !important;
  color: #1B4B2E !important;
}

.stApp {
  background: linear-gradient(180deg, #DFF5DA 0%, #E4F8D9 40%, #F5FFF1 100%) !important;
}

/* ============================================================
   TOP BAR Verde + iconos blancos
=============================================================== */
header[data-testid="stHeader"] {
  background-color: #CDEFCB !important;
  box-shadow: 0 1px 4px rgba(0,0,0,0.05) !important;
}
header svg, header span, header div {
  color: #FFFFFF !important;
  fill: #FFFFFF !important;
  stroke: #FFFFFF !important;
}

/* ============================================================
   FILE UPLOADER
=============================================================== */
.stFileUploader {
  background-color: #0F3A21 !important;
  border: 2px dashed #26C430 !important;
  border-radius: 15px !important;
}
.stFileUploader * { color: #FFD84D !important; }
.stFileUploader button {
  background-color: #145A32 !important;
  color: #FFD84D !important;
}
.stFileUploader button:hover {
  background-color: #0E4225 !important;
}

/* ============================================================
   INPUTS
=============================================================== */
input[type=text], input[type=password], textarea {
  color: #1B4B2E !important;
  background-color: white !important;
  border-radius: 10px !important;
  border: 1.5px solid #9BCFA0 !important;
}

/* ============================================================
   BOTÓN PRINCIPAL
=============================================================== */
div.stButton > button {
  background-color: #26C430 !important;
  color: white !important;
  border-radius: 10px !important;
}
div.stButton > button:hover {
  background-color: #1FA62E !important;
}

/* ============================================================
   LABELS NARANJAS
=============================================================== */
label, .stTextInput label, .stToggle label, .stTextArea label {
  color: #E69A2A !important;
}

/* ============================================================
   FIX PARA TOGGLE
=============================================================== */
.stSwitch *, div[data-testid="stSwitch"] * {
  color: #E69A2A !important;
}

/* ============================================================
   Imagen centrada
=============================================================== */
.img-center {
    display: block;
    margin: 14px auto 24px auto;
    max-width: 520px;
    width: 90%;
    border-radius: 12px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.08);
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================
st.markdown("""
<h1 style='text-align:center; font-size:34px;'>
    🍌 Analizador de Frutas con IA
</h1>
<p style='text-align:center; font-size:16px; margin-top:-10px;'>
    Clasificación visual asistida por inteligencia artificial
</p>
""", unsafe_allow_html=True)

# =========================================================
# IMAGEN "verduras"
# =========================================================
def render_center_image(filename_base="verduras"):
    for ext in (".png", ".jpg", ".jpeg", ".webp"):
        p = Path(f"{filename_base}{ext}")
        if p.exists():
            img_bytes = p.read_bytes()
            b64 = base64.b64encode(img_bytes).decode()
            st.markdown(
                f'<img src="data:image/{ext[1:]};base64,{b64}" class="img-center" />',
                unsafe_allow_html=True
            )
render_center_image()

# =========================================================
# UPLOADER
# =========================================================
st.subheader("📤 Sube una imagen para analizar")
uploaded_file = st.file_uploader("Selecciona una imagen", type=["jpg", "png", "jpeg"])

# =========================================================
# API KEY
# =========================================================
ke = st.text_input("🔐 Ingresa tu clave API", type="password")
os.environ["OPENAI_API_KEY"] = ke
api_key = ke
client = OpenAI(api_key=api_key)

# =========================================================
# TOGGLE CONTEXTO
# =========================================================
show_details = st.toggle("📝 Agregar contexto adicional a la imagen")
if show_details:
    additional_details = st.text_area("Detalles:")

# =========================================================
# FUNCIÓN ENCODE
# =========================================================
def encode_image(img):
    return base64.b64encode(img.getvalue()).decode("utf-8")

# =========================================================
# BOTÓN ANALIZAR
# =========================================================
if uploaded_file and api_key and st.button("🔍 Analizar imagen con IA"):

    with st.spinner("🍃 Analizando imagen..."):
        base64_image = encode_image(uploaded_file)

        prompt = """
Eres un clasificador de frutas. 

Devuelve SOLO:
- "maduro" si la fruta está madura
- "no maduro" si la fruta NO está madura
SIN explicar nada más.
"""

        if show_details:
            prompt += f"\nContexto adicional: {additional_details}"

        try:
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url",
                         "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
                    ],
                }],
                max_tokens=30,
            )

            result = response.choices[0].message.content.lower().strip()

            st.subheader("📌 Resultado del modelo:")
            st.success(result)

            # =========================================================
            # LÓGICA → MQTT HACIA EL ESP32
            # =========================================================

            if "maduro" in result:
                payload = {"Act1": "ON", "Analog": 100}
            else:
                payload = {"Act1": "OFF", "Analog": 0}

            mqtt_client.publish(MQTT_TOPIC, json.dumps(payload))

            st.info(f"📡 Enviado a Wokwi: {payload}")

        except Exception as e:
            st.error(f"❌ Error: {e}")
