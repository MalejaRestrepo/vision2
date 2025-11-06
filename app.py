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

/* ================================
   ✅ FONDO DEGRADADO GENERAL
================================ */
.stApp {
    background: linear-gradient(180deg, #DFF5DA 0%, #EAFBE2 40%, #F8FFF5 100%) !important;
    font-family: 'Inter', sans-serif !important;
}


/* ================================
   ✅ TOP BAR – ÍCONOS VERDE FUERTE + FONDO INVISIBLE
================================ */

/* Hacer invisible la barra negra */
header[data-testid="stHeader"] {
    background-color: rgba(0,0,0,0) !important;
    box-shadow: none !important;
}

/* Hacer invisible el overlay */
header[data-testid="stHeader"] > div:first-child {
    background-color: transparent !important;
}

/* Íconos de la top bar en verde fuerte */
header svg {
    color: #1FAE3D !important;       /* VERDE VIVO */
    stroke: #1FAE3D !important;
    fill: #1FAE3D !important;
}

/* Texto de "Share" también verde fuerte */
header div {
    color: #1FAE3D !important;
}



/* ================================
   ✅ FILE UPLOADER VERDE OSCURO CON TEXTO AMARILLO
================================ */

/* Caja del uploader */
.stFileUploader {
    background-color: #0F3A21 !important;     /* VERDE MUY OSCURO */
    border: 2px dashed #2ECC71 !important;    /* VERDE LIMA */
    border-radius: 12px !important;
    padding: 15px !important;
}

/* Título y textos dentro del uploader */
.stFileUploader label,
.stFileUploader div,
.stFileUploader span,
.stFileUploader p {
    color: #FBDD3B !important;      /* AMARILLO LEGIBLE */
}

/* Botón Browse files */
.stFileUploader button {
    background-color: #145A32 !important;     /* verde oscuro */
    border-radius: 8px !important;
    border: none !important;
    color: #FBDD3B !important;                /* amarillo */
}

/* Hover del botón */
.stFileUploader button:hover {
    background-color: #0E4225 !important;
    color: #FFE96A !important;
}


/* ================================
   ✅ INPUTS LEÍBLES
================================ */
input[type=text], input[type=password], textarea {
    background-color: #FFFFFF !important;
    color: #1B4B2E !important;
    border-radius: 10px !important;
    border: 1.5px solid #9AC89A !important;
    padding: 10px !important;
}


/* ================================
   ✅ BOTÓN ANALIZAR
================================ */
div.stButton > button {
    background-color: #1FAE3D !important;
    color: white !important;
    border-radius: 10px !important;
    padding: 10px 20px !important;
    border: none !important;
    font-weight: 600 !important;
}
div.stButton > button:hover {
    background-color: #199A34 !important;
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
