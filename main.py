import pandas as pd
import numpy as np
import re
import os
from funciones import *

fecha_inicio  = input("Fecha de inicio (DD.MM.AAAA): ")
fecha_termino = "30.09.2021"

nombre_archivo = "".join((fecha_inicio, "-", fecha_termino, ".xlsx"))

dataframe = leer_archivo(nombre_archivo)

textos = dataframe["Texto"]
dataframe["Categoría"] = textos.apply(detectar_categoria)
print("Categoría detectada.")
dataframe["RUT"] = textos.apply(detectar_rut)
print("RUT detectado.")
dataframe["N° Factura"] = textos.apply(detectar_n_factura)
print("N° de factura detectado.")
dataframe["Números"] = textos.apply(detectar_numeros)

"""
dataframe["Categoría"] = dataframe["Texto"].apply(detectar_categoria)
dataframe["RUT"] = dataframe["Texto"].apply(detectar_rut)

filtro = pd.isna(dataframe["RUT"])
dataframe["N° Factura"] = np.nan
dataframe.loc[filtro, "N° Factura"] = dataframe[filtro]["Texto"].apply(detectar_n_factura)
"""

con_rut = dataframe[pd.notna(dataframe["RUT"])]
con_n_factura = dataframe[pd.isna(dataframe["RUT"]) & pd.notna(dataframe["N° Factura"])]
con_otros_numeros = dataframe[pd.isna(dataframe["RUT"]) & pd.isna(dataframe["N° Factura"]) & pd.notna(dataframe["Números"])]
sin_numero = dataframe[pd.isna(dataframe["RUT"]) & pd.isna(dataframe["N° Factura"]) & pd.isna(dataframe["Números"])]

"""
print("TODOS LOS DATOS\n")
print(dataframe)
print("\n\nCON RUT\n")
print(con_rut)
print("\n\nCON N° DE FACTURA\n")
print(con_n_factura)
print("\n\nCON OTROS NÚMEROS\n")
print(con_otros_numeros)
print("\n\nSIN NÚMERO\n")
print(sin_numero)
"""

directorio = "".join((fecha_inicio, "-", fecha_termino, "/"))

try:
	os.mkdir(directorio)
except FileExistsError:
	pass

for df, nombre in ((dataframe, "NUEVO"), (con_rut, "RUT"), (con_n_factura, "N_FACTURA"), (con_otros_numeros, "OTROS_N"), (sin_numero, "SIN_N")):
	escribir_archivo(df, directorio + nombre + ".xlsx")
