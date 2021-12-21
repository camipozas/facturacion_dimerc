import numpy as np
import pandas as pd

def leer_FBL3N(ruta):
    FBL3N = leer_excel(ruta)

    # Limpiar tabla
    FBL3N.dropna(
        subset={"Nº documento", "Importe en moneda local"},
        inplace=True
    )
    
    # Convertir columnas
    col = "Importe en moneda local"
    if FBL3N["Moneda local"][0] == "CLP":
        FBL3N[col] = FBL3N[col].astype(np.int32)
    elif FBL3N["Moneda local"][0] == "PEN":
        FBL3N[col] = FBL3N[col].astype(np.float32)

    FBL3N["Cuenta de mayor"] = FBL3N["Cuenta de mayor"].astype(np.int64)
    FBL3N["Nº documento"] = FBL3N["Nº documento"].astype(np.int64)
    
    return FBL3N


def leer_FBL5N(ruta):
    FBL5N = leer_excel(ruta)

    # Limpiar tabla
    FBL5N.dropna(
        subset={"Nº documento", "Importe en moneda doc."},
        inplace=True
    )
    
    # Convertir columnas
    col = "Importe en moneda doc."
    if FBL5N["Moneda del documento"][0] == "CLP":
        FBL5N[col] = FBL5N[col].astype(np.int32)
    elif FBL5N["Moneda del documento"][0] == "PEN":
        FBL5N[col] = FBL5N[col].astype(np.float32)

    FBL5N["Sociedad"] = FBL5N["Sociedad"].astype(np.int16)
    FBL5N["Cuenta"] = FBL5N["Cuenta"].astype(np.int64)
    FBL5N["Nº documento"] = FBL5N["Nº documento"].astype(np.int64)

    return FBL5N
        

""" LEER Y ESCRIBIR EXCEL """

def leer_excel(ruta, hoja=0):
    while True:
        try:
            print("Leyendo archivo Excel:", ruta)
            dataframe = pd.read_excel(ruta, sheet_name=hoja)
            break
        except PermissionError:
            print("Error: el archivo ya está abierto. Ciérralo y vuelve a intentarlo.")
            input("Presiona Enter cuando esté listo.")
        except FileNotFoundError:
            raise FileNotFoundError
		    
    return dataframe

    
def escribir_excel(dataframe, ruta):
    while True:
        try:
            print("Escribiendo nuevo archivo Excel:", ruta)
            dataframe.to_excel(ruta, index=False)
            break
        except PermissionError:
            print("Error: el archivo ya está abierto. Ciérralo y vuelve a intentarlo.")
            input("Presiona Enter cuando esté listo.")



""" LEER Y ESCRIBIR CSV """

def leer_csv(ruta):
    while True:
        try:
            print("Leyendo archivo CSV:", ruta)
            dataframe = pd.read_csv(ruta)
            break
        except PermissionError:
            print("Error: el archivo ya está abierto. Ciérralo y vuelve a intentarlo.")
            input("Presiona Enter cuando esté listo.")
        except FileNotFoundError:
            raise FileNotFoundError
		    
    return dataframe


def escribir_csv(dataframe, ruta):
    while True:
        try:
            print("Escribiendo nuevo archivo CSV:", ruta)
            dataframe.to_csv(ruta, index=False)
            break
        except PermissionError:
            print("Error: el archivo ya está abierto. Ciérralo y vuelve a intentarlo.")
            input("Presiona Enter cuando esté listo.")
