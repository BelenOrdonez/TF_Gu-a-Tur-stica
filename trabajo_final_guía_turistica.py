# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
from unidecode import unidecode
import zipfile
import os
import requests
from io import BytesIO

# Configuración
st.set_page_config(page_title="Guía Turística del Perú", layout="centered")
st.title("🇵🇪 Guía Turística del Perú")

# Enlaces de los archivos en GitHub
EXCEL_URL = "https://raw.githubusercontent.com/BelenOrdonez/TF_Gu-a-Tur-stica/main/base%20de%20datos%20guia%20turistica.xlsx"
ZIP_URL = "https://raw.githubusercontent.com/BelenOrdonez/TF_Gu-a-Tur-stica/main/mapas%20zip/mapas_departamentos.zip"

# Crear carpeta temporal para mapas
MAPA_DIR = "mapas_departamentos"
if not os.path.exists(MAPA_DIR):
    os.makedirs(MAPA_DIR)

# Descargar y cargar Excel
@st.cache_data
def cargar_excel(url):
    response = requests.get(url)
    df = pd.read_excel(BytesIO(response.content), index_col=0)
    df.index = [unidecode(str(idx).strip().lower()) for idx in df.index]
    df.columns = [unidecode(str(col).strip().lower()) for col in df.columns]
    return df

# Descargar y extraer ZIP
@st.cache_resource
def extraer_zip(url, carpeta_destino):
    response = requests.get(url)
    with zipfile.ZipFile(BytesIO(response.content)) as zip_ref:
        zip_ref.extractall(carpeta_destino)

# Cargar archivos
with st.spinner("📥 Cargando archivos desde GitHub..."):
    df = cargar_excel(EXCEL_URL)
    extraer_zip(ZIP_URL, MAPA_DIR)

st.success("✅ Archivos cargados exitosamente desde GitHub.")

# Crear lista de departamentos
departamentos = df.columns.tolist()
departamento_normalizados = [unidecode(dep.lower().strip()) for dep in departamentos]
mapeo_departamentos = dict(zip(departamento_normalizados, departamentos))

# Selección de departamento
seleccion = st.selectbox("🔍 Elige un departamento para explorar:", departamentos)

if seleccion:
    clave = unidecode(seleccion.lower().strip())
    ruta_mapa = os.path.join(MAPA_DIR, f"mapa {clave}.png")

    st.header(f"📍 {seleccion}")

    if os.path.exists(ruta_mapa):
        st.image(ruta_mapa, caption=f"Mapa de {seleccion}", use_column_width=True)
    else:
        st.warning("⚠️ Mapa no encontrado para este departamento.")

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
        st.error(f"❌ Faltan datos en el Excel: {e}")


