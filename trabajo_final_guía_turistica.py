# -*- coding: utf-8 -*-

# Instalar librerías necesarias
pip install openpyxl unidecode

# Importar librerías
from google.colab import files
import pandas as pd
import streamlit as st
from IPython.display import display, Image
from unidecode import unidecode
import zipfile
import os

# Subir archivos
print("🔼 Sube el archivo Excel y el ZIP con los mapas (ambos desde tu computadora)")
uploaded = files.upload()

#Extraer ZIP con mapas
for filename in uploaded.keys():
    if filename.endswith(".zip"):
        with zipfile.ZipFile(filename, 'r') as zip_ref:
            zip_ref.extractall("mapas_departamentos")
        print(" Mapas extraídos en la carpeta mapas_departamentos")

# Cargar Excel (base de datos)
excel_files = [f for f in uploaded if f.endswith(".xlsx")]
if not excel_files:
    raise ValueError("No se subió ningún archivo Excel.")
excel_path = excel_files[0]

df = pd.read_excel(excel_path, index_col=0)
df.index = [unidecode(str(idx).strip().lower()) for idx in df.index]
df.columns = [unidecode(str(col).strip().lower()) for col in df.columns]

# Mostrar departamentos disponibles
print("\n📌 Departamentos disponibles:")
print(", ".join(df.columns))

# Crear mapeo
departamento_originales = df.columns.tolist()
departamento_normalizados = [unidecode(dep.lower().strip()) for dep in departamento_originales]
mapeo_departamentos = dict(zip(departamento_normalizados, departamento_originales))

# Preguntar al usuario qué departamento desea visitar
while True:
    departamento_usuario = input("\n🔍 ¿Qué departamento del Perú te gustaría visitar?\n").strip().lower()
    departamento_usuario = unidecode(departamento_usuario)

    if departamento_usuario in mapeo_departamentos:
        col_departamento = mapeo_departamentos[departamento_usuario]
        nombre_mapa = f"mapa {departamento_usuario}.png"
        ruta_mapa = os.path.join("mapas_departamentos", nombre_mapa)

        # Mostrar mapa
        if os.path.exists(ruta_mapa):
            print(f"\n🗺️ Mapa de {col_departamento.title()}:")
            display(Image(filename=ruta_mapa))
        else:
            print(f"⚠️ No se encontró el mapa: {ruta_mapa}")

        # Mostrar información
        try:
            descripcion = df.at["descripcion", departamento_usuario]
            tips = df.at["tips", departamento_usuario]
            top3 = df.at["top 3 lugares para visitar", departamento_usuario]

            print(f"\n📍 {col_departamento.title()}")
            print(f"\n📝 Descripción:\n{descripcion}")
            print(f"\n💡 Tips:\n{tips}")
            print(f"\n🌟 Top 3 lugares para visitar:\n{top3}")
        except KeyError as e:
            print(f"❌ Falta en el Excel la fila: {e}")
        break
    else:
        print("Ese departamento no está en la lista. Intenta nuevamente.")
