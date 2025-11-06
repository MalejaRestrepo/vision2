import os
import streamlit as st
import base64
from openai import OpenAI
import openai
from PIL import Image

# ============================
# 🎨 CSS PARA ESTILO PERSONALIZADO
# ============================

st.markdown("""
<style>

/* Fondo general */
body {
    background-color: #F5F9F1;
}

/* Título principal */
h1 {
    font-family: 'Arial Rounded MT Bold', sans-serif;
    color: #2E7D32;
    text-align: center;
    margin-bottom: -10px;
}

/* Subtítulos */
h2, h3, h4 {
    color: #4C8C4A;
    font-family: 'Arial Rounded MT Bold';
}

/* Sidebar */
.css-1d391kg { 
    background-color: #E7F4E4 !important;
    border-right: 2px solid #B8DEB1 !important;
}
.css-1d391kg h2, .css-1d391kg h3, .css-1d391kg p {
    color: #2E7D32 !important;
    font-weight: 600;
}

/* Contenedor general */
.container {
    background-color: #FFFFFF;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.06);
    margin-bottom: 25px;
}

/* Botón principal */
div.stButton > button:first-child {
    background-color: #4CAF50;
    color: white;
    padding: 0.6rem 1rem;
    border-radius: 10px;
    border: none;
    font-weight: 600;
    font-size: 16px;
    transition: 0.2s;
}
div.stButton > button:first-child:hover {
    background-color: #43A047;
    transform: scale(1.02);
}

/* Input API key */
input[type=password], input[type=text] {
    border-radius: 10px !important;
    border: 1.5px solid #A5D6A7 !important;
}

/* File uploader */
.css-1p0v0b0 {
    background-color: #FFFFFF !important;
    border: 2px dashed #A5D6A7 !important;
    border-radius: 12px !important;
}

/* Toggle switch */
.st-emotion-cache-16idsys {
    color: #2E7D32 !important;
}

</style>
""", unsafe_allow_html=True)


# ============================
# ✅ FUNCIÓN PARA ENCODE DE IMAGEN
# ============================

def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode("utf-8")


# ============================
# ✅ CONFIGURACIÓN PÁGINA
# ============================

st.set_page_config(page_title="Análisis de Imagen 🍏🤖", layout="centered", initial_sidebar_state="collapsed")
st.title("🍏 Análisis Inteligente de Imagen 🍌")


# Header decorativo
st.markdown('<div class="container">', unsafe_allow_html=True)
image = Image.open('OIG4.jpg')
st.image(image, width=350, caption="Analizador visual con IA")
st.markdown("</div>", unsafe_allow_html=True)


# ============================
# ✅ SIDEBAR
# ============================

with st.sidebar:
    st.subheader("🌿 Analizador Visual IA")
    st.write("Este agente entiende y describe cualquier imagen que subas, usando visión computacional avanzada.")
    st.write("💡 Ideal para proyectos de frutas, objetos, ambientes, etc.")


# ============================
# ✅ API KEY
# ============================

ke = st.text_input('🔐 Ingresa tu clave API:', type="password")
os.environ['OPENAI_API_KEY'] = ke
api_key = os.environ['OPENAI_API_KEY']

client = OpenAI(api_key=api_key)


# ============================
# ✅ SUBIR IMAGEN
# ============================

st.markdown('<div class="container">', unsafe_allow_html=True)
uploaded_file = st.file_uploader("📤 Sube una imagen", type=["jpg", "png", "jpeg"])
st.markdown("</div>", unsafe_allow_html=True)

if uploaded_file:
    with st.expander("🖼️ Vista previa de la imagen", expanded=True):
        st.image(uploaded_file, caption=uploaded_file.name, use_container_width=True)


# ============================
# ✅ DETALLES OPCIONALES
# ============================

show_details = st.toggle("📝 Agregar detalles sobre la imagen", value=False)

if show_details:
    additional_details = st.text_area("Describe aquí detalles adicionales:")


# ============================
# ✅ BOTÓN ANALIZAR
# ============================

st.markdown('<div class="container">', unsafe_allow_html=True)
analyze_button = st.button("🔍 Analizar imagen")
st.markdown("</div>", unsafe_allow_html=True)


# ============================
# ✅ ANÁLISIS
# ============================

if uploaded_file is not None and api_key and analyze_button:
    with st.spinner("Analizando imagen... 🍃"):

        base64_image = encode_image(uploaded_file)
        prompt_text = "Describe detalladamente lo que ves en esta imagen, en español."

        if show_details and additional_details:
            prompt_text += f"\n\nContexto adicional del usuario:\n{additional_details}"

        try:
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt_text},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            },
                        },
                    ],
                }],
                max_tokens=300,
            )

            texto = response.choices[0].message.content

            st.success("✅ Análisis completado:")
            st.markdown(f"<div class='container'>{texto}</div>", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"⚠️ Error: {e}")

else:
    if not uploaded_file and analyze_button:
        st.warning("⚠️ Sube una imagen antes de analizar.")
    if not api_key:
        st.warning("⚠️ Ingresa tu clave API para continuar.")
