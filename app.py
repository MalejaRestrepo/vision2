import os
import streamlit as st
import base64
from openai import OpenAI
import openai
from PIL import Image

# ---------------------------------------------------------
# ✅ DISEÑO Y ESTILO PERSONALIZADO — TEMA: MADUREZ DE FRUTAS
# ---------------------------------------------------------
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

/* Fondo con patrón sutil */
body {
    background: #FFFDF6;
}

/* Encabezado estilo "máquina clasificadora" */
.header {
    background: linear-gradient(90deg, #FFE27A, #FFCD38);
    padding: 25px;
    border-radius: 16px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    text-align: center;
    margin-bottom: 25px;
}
.header h1 {
    color: #4A4A4A;
    font-weight: 700;
    margin: 0;
}

/* Cards */
.box {
    background: white;
    padding: 22px;
    border-radius: 14px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.08);
    margin-bottom: 25px;
}

/* Botón */
div.stButton > button {
    background-color: #7ACB3F;
    color: white;
    border-radius: 12px;
    padding: 0.6rem 1.2rem;
    border: none;
    font-weight: 600;
    transition: 0.2s;
}
div.stButton > button:hover {
    background-color: #6BB634;
    transform: scale(1.03);
}

/* File uploader */
.css-1p0v0b0 {
    border-radius: 12px;
    border: 2px dashed #FFD85E !important;
}

/* API input */
input[type=password], input[type=text] {
    border-radius: 10px !important;
    border: 2px solid #FFD760 !important;
}

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# ✅ ENCABEZADO TEMÁTICO
# ---------------------------------------------------------

st.markdown("""
<div class='header'>
    <h1>🍌 Analizador de Frutas con IA</h1>
    <p style="font-size:17px; margin-top:6px; color:#5A5A5A;">
        Esta herramienta utiliza inteligencia artificial para analizar una imagen y ayudarte a interpretar su contenido.  
        Pensado para proyectos de clasificación de madurez de frutas, visión artificial y aplicaciones educativas.
    </p>
</div>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# ✅ SUBIR IMAGEN — EN UNA CARD BONITA
# ---------------------------------------------------------

st.markdown("<div class='box'>", unsafe_allow_html=True)
st.subheader("📤 Sube una imagen para analizar")
uploaded_file = st.file_uploader("Selecciona una imagen", type=["jpg", "png", "jpeg"])
st.markdown("</div>", unsafe_allow_html=True)


# API KEY
st.markdown("<div class='box'>", unsafe_allow_html=True)
ke = st.text_input("🔐 Ingresa tu Clave API:", type="password")
st.markdown("</div>", unsafe_allow_html=True)

os.environ['OPENAI_API_KEY'] = ke
api_key = os.environ['OPENAI_API_KEY']
client = OpenAI(api_key=api_key)


# ---------------------------------------------------------
# ✅ MOSTRAR IMAGEN
# ---------------------------------------------------------

if uploaded_file:
    st.markdown("<div class='box'>", unsafe_allow_html=True)
    st.subheader("🖼 Vista previa")
    st.image(uploaded_file, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------------------------------------
# ✅ DETALLES OPCIONALES
# ---------------------------------------------------------

st.markdown("<div class='box'>", unsafe_allow_html=True)
show_details = st.toggle("📝 ¿Deseas agregar más detalles sobre la imagen?")
if show_details:
    additional_details = st.text_area("Escribe contexto adicional aquí:")
st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------------------------------------
# ✅ BOTÓN DE ANÁLISIS
# ---------------------------------------------------------

st.markdown("<div class='box'>", unsafe_allow_html=True)
analyze_button = st.button("🔍 Analizar imagen con IA")
st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------------------------------------
# ✅ PROCESO DE ANÁLISIS
# ---------------------------------------------------------

def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode("utf-8")

if uploaded_file and api_key and analyze_button:

    with st.spinner("🍃 Analizando imagen..."):

        base64_image = encode_image(uploaded_file)

        prompt_text = "Describe con detalle lo que ves en esta imagen. Explica en español."

        if show_details and additional_details:
            prompt_text += f"\n\nDetalles del usuario:\n{additional_details}"

        try:
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt_text},
                        {
                            "type": "image_url",
                            "image_url": { "url": f"data:image/jpeg;base64,{base64_image}" },
                        },
                    ],
                }],
                max_tokens=300,
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
        st.warning("⚠️ Sube una imagen para analizar.")
    if not api_key:
        st.warning("⚠️ Ingresa tu API key para continuar.")
