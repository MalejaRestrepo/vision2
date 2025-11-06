import os
import streamlit as st
import base64
from openai import OpenAI
import openai
from PIL import Image


# =========================================================
# ✅ CSS — Tema verde + modo claro + limpieza total
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

html, body, .stApp, .main {
    background-color: #E8F5E9 !important;   /* verde claro */
    color: #2E2E2E !important;
    font-family: 'Poppins', sans-serif !important;
}

/* HEADER */
.header {
    background: linear-gradient(90deg, #FFE27A, #FFCD38);
    padding: 32px;
    border-radius: 18px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.10);
    text-align: center;
    margin-top: 25px;
    margin-bottom: 28px;
}
.header h1 {
    color: #3A3A3A;
    font-weight: 700;
    font-size: 32px;
}

/* CARDS */
.box {
    background: #FFFFFF;
    padding: 22px;
    border-radius: 14px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.08);
    margin-bottom: 25px;
}

/* BOTÓN */
div.stButton > button {
    background-color: #7ACB3F !important;
    color: white !important;
    border-radius: 12px !important;
    padding: 12px 22px !important;
    border: none !important;
    font-weight: 600 !important;
    font-size: 16px !important;
    transition: 0.2s ease !important;
}
div.stButton > button:hover {
    background-color: #6BB634 !important;
    transform: scale(1.03);
}

/* INPUTS */
input[type=password], input[type=text] {
    border-radius: 12px !important;
    border: 2px solid #FFD760 !important;
    padding: 8px 10px !important;
    background:white !important;
}

/* FILE UPLOADER */
.stFileUploader {
    border: 2px dashed #FFC83D !important;
    border-radius: 12px !important;
    padding: 10px !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #D6EED3 !important;
}

/* Fix Streamlit unwanted wrappers */
.css-1cpxqw2, .css-ocqkz7, .e1f1d6gn0 {
    background-color: transparent !important;
}

</style>
""", unsafe_allow_html=True)



# =========================================================
# ✅ ENCABEZADO
# =========================================================

st.markdown("""
<div class="header">
    <h1>🍌 Analizador de Frutas con IA</h1>
    <p style="font-size:17px; margin-top:8px; color:#4A4A4A;">
        Esta herramienta utiliza inteligencia artificial para describir el contenido de cualquier imagen. <br>
        Diseñada para proyectos de clasificación de madurez de frutas, visión artificial y aplicaciones educativas.
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
api_key = os.environ['OPENAI_API_KEY']
client = OpenAI(api_key=api_key)



# =========================================================
# ✅ PREVIEW DE LA IMAGEN
# =========================================================

if uploaded_file:
    st.markdown("<div class='box'>", unsafe_allow_html=True)
    st.subheader("🖼 Vista previa")
    st.image(uploaded_file, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)



# =========================================================
# ✅ DETALLES EXTRA
# =========================================================

st.markdown("<div class='box'>", unsafe_allow_html=True)
show_details = st.toggle("📝 Agregar contexto adicional a la imagen")
if show_details:
    additional_details = st.text_area("Escribe tu contexto aquí:")
st.markdown("</div>", unsafe_allow_html=True)



# =========================================================
# ✅ BOTÓN ANALIZAR
# =========================================================

st.markdown("<div class='box'>", unsafe_allow_html=True)
analyze_button = st.button("🔍 Analizar imagen con IA")
st.markdown("</div>", unsafe_allow_html=True)



# =========================================================
# ✅ FUNCIÓN ENCODE
# =========================================================

def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode("utf-8")



# =========================================================
# ✅ ANALIZAR IMAGEN
# =========================================================

if uploaded_file and api_key and analyze_button:
    with st.spinner("🍃 Analizando imagen..."):

        base64_image = encode_image(uploaded_file)

        prompt_text = "Describe detalladamente lo que ves en esta imagen, en español."

        if show_details and additional_details:
            prompt_text += f"\nDetalles del usuario: {additional_details}"

        try:
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt_text},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                        },
                    ],
                }],
                max_tokens=350,
            )

            texto = response.choices[0].message.content

            st.markdown("<div class='box'>", unsafe_allow_html=True)
            st.subheader("✅ Resultado del análisis")
            st.write(texto)
            st.markdown("</div>", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ Error: {e}")

else:
    if analyze_button and not uploaded_file:
        st.warning("⚠️ Sube una imagen antes de analizar.")
    if not api_key:
        st.warning("⚠️ Ingresa tu clave API.")


