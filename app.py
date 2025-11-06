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

html, body, .stApp, .main {
    font-family: 'Inter', sans-serif !important;
    color: #1B4B2E !important;        /* ✅ TEXTO VERDE OSCURO */
}


/* ============================================================
   ✅ FONDO DEGRADADO GLOBAL
=============================================================== */
.stApp {
    background: linear-gradient(180deg, #DFF5DA 0%, #E4F8D9 40%, #F5FFF1 100%) !important;
}


/* ============================================================
   ✅ TOP BAR – TRANSPARENTE + ÍCONOS VERDE FUERTE
=============================================================== */

/* Fondo transparente */
header[data-testid="stHeader"] {
    background-color: rgba(0,0,0,0) !important;
    box-shadow: none !important;
}

/* Contenedor interno transparente */
header[data-testid="stHeader"] > div:first-child {
    background-color: transparent !important;
}

/* Íconos y texto Share → VERDE FUERTE */
header svg, header span, header div {
    color: #26C430 !important;
    fill: #26C430 !important;
    stroke: #26C430 !important;
}


/* ============================================================
   ✅ FILE UPLOADER – VERDE OSCURO + TEXTO AMARILLO
=============================================================== */

.stFileUploader {
    background-color: #0F3A21 !important;    /* verde oscuro */
    border: 2px dashed #26C430 !important;   /* verde fuerte */
    border-radius: 15px !important;
    padding: 16px !important;
}

/* Texto del uploader */
.stFileUploader * {
    color: #FFD84D !important;               /* amarillo */
}

/* Botón browse */
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


/* ============================================================
   ✅ INPUTS
=============================================================== */

input[type=text], input[type=password], textarea {
    color: #1B4B2E !important;               /* verde oscuro */
    background-color: white !important;
    border-radius: 10px !important;
    border: 1.5px solid #9BCFA0 !important;
    padding: 10px !important;
}


/* ============================================================
   ✅ BOTÓN PRINCIPAL
=============================================================== */

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


/* ============================================================
   ✅ LABELS → NARANJA LEGIBLE
=============================================================== */

label,
.stCheckbox label,
.stTextInput label,
.stTextArea label,
.stToggle label,
.css-1p0v0b0,
.css-17eq0hr,
.css-1vbkxwb,
.stRadio label {
    color: #E69A2A !important;               /* naranja fuerte */
}


/* ============================================================
   ✅ TOGGLE (el que te faltaba)
=============================================================== */

/* etiqueta del toggle */
.stSwitch label, .stSwitch span {
    color: #E69A2A !important;               /* naranja */
}

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
