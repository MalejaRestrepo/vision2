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

/* FUENTE GENERAL */
html, body, .stApp, .main {
    font-family: 'Inter', sans-serif !important;
}

/* ✅ FONDO DEGRADADO VERDE */
.stApp {
    background: linear-gradient(180deg, #E7F5E6 0%, #F4FAF2 100%) !important;
}

/* ✅ TITULOS LEGIBLES */
h1, h2, h3, h4, label, p, span, div {
    color: #1B4B2E !important;
}

/* ✅ INPUTS SUPER LEIBLES */
input[type=text], input[type=password], textarea {
    background-color: #FFFFFF !important;
    color: #1B4B2E !important;
    border-radius: 10px !important;
    border: 1.5px solid #9AC89A !important;
    padding: 10px !important;
    font-size: 15px !important;
}

/* ✅ FILE UPLOADER CLARO Y LIMPIO */
.stFileUploader {
    background-color: white !important;
    border: 2px dashed #9AC89A !important;
    border-radius: 10px !important;
    padding: 12px !important;
}
.stFileUploader label {
    color: #1B4B2E !important;
}

/* ✅ BOTÓN */
div.stButton > button {
    background-color: #4DAA57 !important;
    color: white !important;
    border-radius: 10px !important;
    padding: 10px 20px !important;
    border: none !important;
    font-weight: 600 !important;
    font-size: 15px !important;
}
div.stButton > button:hover {
    background-color: #3C8F46 !important;
    transform: scale(1.02);
}

/* ✅ REMOVER CUADROS BLANCOS FANTASMAS CREADOS POR STREAMLIT */
.css-1cpxqw2, .css-ocqkz7, .css-1v0mbdj, .e1f1d6gn0 {
    background: transparent !important;
    box-shadow: none !important;
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
