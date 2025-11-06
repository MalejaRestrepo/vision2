import os
import streamlit as st
import base64
from openai import OpenAI
import openai
from PIL import Image

# =========================================================
# ✅ CSS — Fondo degradado + texto verde oscuro + NO CARDS
# =========================================================
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

/* =========================
   Base de tipografía / color
========================= */
html, body, .stApp, .main {
  font-family: 'Inter', sans-serif !important;
  color: #1B4B2E !important;            /* texto verde oscuro */
}

/* =========================
   Fondo degradado global
========================= */
.stApp {
  background: linear-gradient(180deg, #DFF5DA 0%, #E4F8D9 40%, #F5FFF1 100%) !important;
}

/* =========================
   Top bar transparente + iconos verde fuerte
========================= */
header[data-testid="stHeader"] {
  background-color: transparent !important;
  box-shadow: none !important;
}
header[data-testid="stHeader"] > div:first-child {
  background-color: transparent !important;
}
header svg, header span, header div {
  color: #26C430 !important;            /* verde fuerte */
  fill: #26C430 !important;
  stroke: #26C430 !important;
}

/* =========================
   File Uploader: verde oscuro + texto amarillo
========================= */
.stFileUploader {
  background-color: #0F3A21 !important; /* verde oscuro */
  border: 2px dashed #26C430 !important;
  border-radius: 15px !important;
  padding: 16px !important;
}
.stFileUploader * {
  color: #FFD84D !important;            /* amarillo legible */
}
.stFileUploader button {
  background-color: #145A32 !important;
  color: #FFD84D !important;
  border-radius: 10px !important;
  border: none !important;
}
.stFileUploader button:hover {
  background-color: #0E4225 !important;
  color: #FFE279 !important;
}

/* =========================
   Inputs
========================= */
input[type=text], input[type=password], textarea {
  color: #1B4B2E !important;
  background-color: white !important;
  border-radius: 10px !important;
  border: 1.5px solid #9BCFA0 !important;
  padding: 10px !important;
}

/* =========================
   Botón principal
========================= */
div.stButton > button {
  background-color: #26C430 !important;
  color: white !important;
  border-radius: 10px !important;
  padding: 10px 20px !important;
  font-weight: 600 !important;
  border: none !important;
}
div.stButton > button:hover {
  background-color: #1FA62E !important;
}

/* =========================
   Labels naranjas (incluye casos comunes)
========================= */
label,
.stCheckbox label,
.stTextInput label,
.stTextArea label,
.stToggle label,
.css-1p0v0b0,
.css-17eq0hr,
.css-1vbkxwb,
.stRadio label,
div[data-testid="stWidgetLabel"] *,
div[data-testid="stWidgetLabel"] p {
  color: #E69A2A !important;            /* naranja fuerte */
}

/* =========================
   FIX robusto para el TOGGLE (este era el que faltaba)
   Cubrimos múltiples variantes del DOM de Streamlit.
========================= */
.stSwitch, .stSwitch * {
  color: #E69A2A !important;            /* naranja fuerte */
}
div[data-testid="stSwitch"], div[data-testid="stSwitch"] * {
  color: #E69A2A !important;            /* naranja fuerte */
}
/* En algunos temas el texto queda en un contenedor hermano de la palanca */
div[data-testid="stHorizontalBlock"] > div:has(div[role="switch"]) + div *,
div[role="switch"] ~ * {
  color: #E69A2A !important;
}

/* (Compat: si :has no aplica, las reglas anteriores ya lo cubren) */

</style>
""", unsafe_allow_html=True)



# =========================================================
# ✅ HEADER DEL PROYECTO
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
# ✅ SUBIR IMAGEN
# =========================================================

st.subheader("📤 Sube una imagen para analizar")
uploaded_file = st.file_uploader("Selecciona una imagen", type=["jpg", "png", "jpeg"])


# =========================================================
# ✅ API KEY
# =========================================================

ke = st.text_input("🔐 Ingresa tu clave API", type="password")
os.environ['OPENAI_API_KEY'] = ke
api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


# =========================================================
# ✅ PREVIEW IMAGEN
# =========================================================

if uploaded_file:
    st.subheader("🖼 Vista previa")
    st.image(uploaded_file, use_container_width=True)


# =========================================================
# ✅ CONTEXTO EXTRA
# =========================================================

show_details = st.toggle("📝 Agregar contexto adicional a la imagen")
if show_details:
    additional_details = st.text_area("Detalles:")


# =========================================================
# ✅ BOTÓN ANALIZAR
# =========================================================

analyze_button = st.button("🔍 Analizar imagen con IA")


# =========================================================
# ✅ ENCODE
# =========================================================

def encode_image(img):
    return base64.b64encode(img.getvalue()).decode("utf-8")


# =========================================================
# ✅ ANALIZAR IMAGEN
# =========================================================

if uploaded_file and api_key and analyze_button:

    with st.spinner("🍃 Analizando imagen..."):

        base64_image = encode_image(uploaded_file)

        prompt = "Describe con detalle lo que ves en esta imagen, en español."
        if show_details:
            prompt += f"\nContexto: {additional_details}"

        try:
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
                    ],
                }],
                max_tokens=350,
            )

            result = response.choices[0].message.content

            st.subheader("✅ Resultado del análisis")
            st.write(result)

        except Exception as e:
            st.error(f"❌ Error: {e}")
