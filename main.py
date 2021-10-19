import pandas as pd
import numpy as np
import re
import os
from funciones import *

# PARTE 1

FBL3N = leer_excel("FBL3N.xlsx")

textos = FBL3N["Texto"]
FBL3N["Categoría"] = textos.apply(detectar_categoria)
FBL3N["RUT"] = textos.apply(detectar_rut)
FBL3N["N° Factura"] = textos.apply(detectar_n_factura)
#FBL3N["Números"] = textos.apply(detectar_numeros)

con_rut = FBL3N[pd.notna(FBL3N["RUT"])]
con_n_factura = FBL3N[pd.isna(FBL3N["RUT"]) & pd.notna(FBL3N["N° Factura"])]
#con_otros_numeros = FBL3N[pd.isna(FBL3N["RUT"]) & pd.isna(FBL3N["N° Factura"]) & pd.notna(FBL3N["Números"])]
#sin_numero = FBL3N[pd.isna(FBL3N["RUT"]) & pd.isna(FBL3N["N° Factura"]) & pd.isna(FBl3N["Números"])]

"""
try:
	os.mkdir(ruta)
except FileExistsError:
	pass

for dataframe, nombre in ((FBL3N, "NUEVO"), (con_rut, "RUT"), (con_n_factura, "N_FACTURA"), (con_otros_numeros, "OTROS_N"), (sin_numero, "SIN_N")):
	escribir_excel(dataframe, ruta + "/" + nombre + ".xlsx")
"""


