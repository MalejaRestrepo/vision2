import os
import streamlit as st
import base64
from openai import OpenAI
import openai
from PIL import Image

# =========================================================
# ✅ CSS — Estética moderna, legible, clara
# =========================================================
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

html, body, .stApp, .main {
    background-color: #F4F8F1 !important;   /* verde MUY suave */
    color: #2D2D2D !important;
    font-family: 'Inter', sans-serif !important;
}

/* HEADER */
.header {
    background: #F9F5D7;
    padding: 32px;
    border-radius: 18px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.06);
    text-align: center;
    margin-top: 25px;
    margin-bottom: 28px;
}
.header h1 {
    color: #2D2D2D;
    font-weight: 700;
    font-size: 32px;
}

/* CARDS */
.box {
    background: #FFFFFF;
    padding: 22px;
    border-radius: 14px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.06);
    margin-bottom: 25px;
}

/* TITULOS */
h2, h3, h4, label {
    color: #2D2D2D !important;
}

/* BOTÓN */
div.stButton > button {
    background-color: #7FB77E !important;
    color: white !important;
    border-radius: 10px !important;
    padding: 10px 20px !important;
    border: none !important;
    font-weight: 600 !important;
    font-size: 15px !important;
    transition: 0.2s ease !important;
}
div.stButton > button:hover {
    background-color: #6EA86D !important;
    transform: scale(1.02);
}

/* INPUTS */
input[type=password], input[type=text], textarea, .stTextInput > div > div > input {
    border-radius: 10px !important;
    border: 1.5px solid #CCCCCC !important;
    background:white !important;
    color:#2D2D2D !important;
}

/* FILE UPLOADER */
.stFileUploader {
    background-color: white !important;
    border-radius: 10px !important;
    border: 1.5px dashed #C8C8C8 !important;
    padding: 14px !important;
}
.stFileUploader label {
    color: #2D2D2D !important;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background-color: #ECF4E9 !important;
}

/* arreglo del texto blanco invisible */
.css-17eq0hr, .css-1p0v0b0, .uploadedFile > div > span {
    color: #2D2D2D !important;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# ✅ HEADER LIMPIO
# =========================================================
st.markdown("""
<div class="header">
    <h1>🍌 Analizador de Frutas con IA</h1>
    <p style="font-size:16px; margin-top:8px; color:#3A3A3A;">
        Usa inteligencia artificial para interpretar imágenes relacionadas con frutas y clasificación visual.
    </p>
</div>
""", unsafe_allow_html=True)

# =========================================================
# ✅ SUBIR IMAGEN
# =========================================================
st.markdown("<div class='box'>", unsafe_allow_html=True)
st.subheader("📤 Sube una imagen para analizar")
uploaded_file = st.file_uploader("Selecciona una imagen", type=["jpg", "png", "jpeg"])
st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# ✅ API KEY
# =========================================================
st.markdown("<div class='box'>", unsafe_allow_html=True)
ke = st.text_input("🔐 Ingresa tu clave API", type="password")
st.markdown("</div>", unsafe_allow_html=True)

os.environ['OPENAI_API_KEY'] = ke
api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# =========================================================
# ✅ PREVIEW IMAGEN
# =========================================================
if uploaded_file:
    st.markdown("<div class='box'>", unsafe_allow_html=True)
    st.subheader("🖼 Vista previa")
    st.image(uploaded_file, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# ✅ CONTEXTO EXTRA
# =========================================================
st.markdown("<div class='box'>", unsafe_allow_html=True)
show_details = st.toggle("📝 Agregar contexto adicional a la imagen")
if show_details:
    additional_details = st.text_area("Detalles:")
st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# ✅ Botón de análisis
# =========================================================
st.markdown("<div class='box'>", unsafe_allow_html=True)
analyze_button = st.button("🔍 Analizar imagen con IA")
st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# ✅ ENCODE
# =========================================================
def encode_image(img):
    return base64.b64encode(img.getvalue()).decode("utf-8")

# =========================================================
# ✅ Procesamiento IA
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

            st.markdown("<div class='box'>", unsafe_allow_html=True)
            st.subheader("✅ Resultado del análisis")
            st.write(result)
            st.markdown("</div>", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ Error: {e}")
