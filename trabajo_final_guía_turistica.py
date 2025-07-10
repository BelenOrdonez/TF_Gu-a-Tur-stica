# -*- coding: utf-8 -*-
import pandas as pd
import streamlit as st
from unidecode import unidecode
import zipfile
import os

st.set_page_config(page_title="Guía Turística del Perú", layout="centered")

st.title("🇵🇪 Guía Turística del Perú")
st.markdown("Sube tu archivo Excel y el ZIP con los mapas para comenzar.")

# Subir archivos
excel_file = st.file_uploader("📄 Sube tu archivo Excel", type=["xlsx"])
zip_file = st.file_uploader("🗺️ Sube tu archivo ZIP con mapas (.png)", type=["zip"])


if excel_file and zip_file:
    # Extraer ZIP
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall("mapas_departamentos")
    st.success("✅ Mapas extraídos correctamente.")

    # Cargar Excel
    df = pd.read_excel(excel_file, index_col=0)
    df.index = [unidecode(str(idx).strip().lower()) for idx in df.index]
    df.columns = [unidecode(str(col).strip().lower()) for col in df.columns]

    departamentos = df.columns.tolist()
    departamento_normalizados = [unidecode(dep.lower().strip()) for dep in departamentos]
    mapeo_departamentos = dict(zip(departamento_normalizados, departamentos))

    # Selección de departamento
    seleccion = st.selectbox("Selecciona un departamento para explorar:", departamentos)

    if seleccion:
        clave = unidecode(seleccion.lower().strip())
        ruta_mapa = os.path.join("mapas_departamentos", f"mapa {clave}.png")

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
            st.error(f"❌ Falta información en el Excel: {e}")
else:
    st.info("⬆️ Esperando que subas los archivos.")



