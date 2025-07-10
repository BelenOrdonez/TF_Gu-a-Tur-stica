import streamlit as st
import pandas as pd
from unidecode import unidecode
import urllib.parse

st.set_page_config(page_title="Guía Turística del Perú", layout="centered")
st.title("🇵🇪 Guía Turística del Perú")


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


# Construye el nombre del archivo y la URL de GitHub

if seleccion:
    clave = unidecode(seleccion.lower().strip())
    nombre_archivo = f"mapa {clave}.png"
    nombre_archivo_url = urllib.parse.quote(nombre_archivo)  # codifica espacios y tildes
    imagen_url = f"https://raw.githubusercontent.com/BelenOrdonez/TF_Gu-a-Tur-stica/main/mapas/{nombre_archivo_url}"

    st.header(f"📍 {seleccion}")
    st.image(imagen_url, caption=f"Mapa de {seleccion}", use_container_width=True)

try:
    descripcion = df.at["descripcion", clave]
    tips = df.at["tips", clave]
    top3_crudo = df.at["top 3 lugares para visitar", clave]

    st.subheader("📝 Descripción")
    st.write(descripcion)

    st.subheader("💡 Tips")
    st.write(tips)

    st.subheader("🌟 Top 3 lugares para visitar")

  
    import re
    lugares = re.split(r"\s*\d+\.\s*", top3_crudo)
    lugares = [l.strip() for l in lugares if l.strip()]  # eliminar vacíos

    for i, lugar in enumerate(lugares, start=1):
        st.markdown(f"{i}. {lugar}")



for lugar in lugares:
    st.markdown(f"- {lugar}")

        st.write(top3)
    except KeyError as e:
        st.error(f"❌ Falta información en el Excel: {e}")
