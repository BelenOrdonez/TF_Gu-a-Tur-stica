import streamlit as st
import pandas as pd
from unidecode import unidecode
import urllib.parse

st.set_page_config(page_title="Guía Turística del Perú", layout="centered")
st.title("🇵🇪 Guía Turística del Perú")

# 📄 Cargar Excel localmente (ya que las imágenes vienen de GitHub)
EXCEL_PATH = "base de datos guia turistica.xlsx"
df = pd.read_excel(EXCEL_PATH, index_col=0)
df.index = [unidecode(str(idx).strip().lower()) for idx in df.index]
df.columns = [unidecode(str(col).strip().lower()) for col in df.columns]

# GitHub base URL para imágenes
BASE_GITHUB_URL = "https://raw.githubusercontent.com/BelenOrdonez/TF_Gu-a-Tur-stica/main/mapas/"

# Lista de departamentos
departamentos = df.columns.tolist()
departamento_normalizados = [unidecode(dep.lower().strip()) for dep in departamentos]
mapeo_departamentos = dict(zip(departamento_normalizados, departamentos))

# Selección
seleccion = st.selectbox("🔍 Elige un departamento para explorar:", departamentos)

if seleccion:
    clave = unidecode(seleccion.lower().strip())
    nombre_archivo = f"mapa {clave}.png"
    nombre_archivo = urllib.parse.quote(nombre_archivo)  # para manejar espacios y tildes
    imagen_url = f"{BASE_GITHUB_URL} {nombre_archivo}"

    st.header(f"📍 {seleccion}")
    st.image(imagen_url, caption=f"Mapa de {seleccion}", use_container_width=True)

    try:
        descripcion = df.at["descripcion", clave]
        tips = df.at["tips", clave]
        top3 = df.at["top 3 lugares para visitar", clave]

        st.subheader("📝 Descripción")
        st.write(descripcion)

        st.subheader("💡 Tips")
        st.write(tips)

        st.subheader("🌟 Top 3 lugares para visitar")
        st.write(top3)
    except KeyError as e:
        st.error(f"❌ Falta información en el Excel: {e}")
