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


# PARTE 2

FBL5N = leer_excel("FBL5N.xlsx")
FBL5N["Cuenta"] = FBL5N["Cuenta"].apply(lambda n: str(n).strip("0"))

# Calzar números de factura

matches_factura = pd.merge(FBL5N, con_n_factura, left_on="Nｺ doc.", right_on="Nº documento")
print(matches_factura)
escribir_excel(matches_factura, "MATCHES.xlsx")


# Calzar RUTs
KNA1 = leer_excel("KNA1.xlsx")
KNA1["Nº ident.fis.1"] = KNA1["Nº ident.fis.1"].apply(lambda s: str(s).replace("-", ""))

join = pd.merge(FBL5N, KNA1, left_on="Cuenta", right_on="Cliente")
join = FBL5N.merge(KNA1, left_on="Cuenta", right_on="Cliente", how='left')
#join = pd.merge(join, con_rut, left_on="Nº ident.fis.1", right_on="RUT")
escribir_excel(join, "Join.xlsx")

