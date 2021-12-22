import numpy as np
import pandas as pd

def leer_FBL3N(ruta):
    FBL3N = leer_excel(ruta)

    # Obtener columnas
    mayor, n_doc, monto, moneda = [FBL3N.columns[i] for i in (2, 5, 11, 12)]

    # Limpiar tabla
    FBL3N.dropna(subset={n_doc, monto}, inplace=True)

    if len(FBL3N) == 0:
        return FBL3N
    
    # Convertir columnas
    if FBL3N[moneda].iloc[0] == "CLP":
        FBL3N[monto] = FBL3N[monto].astype(np.int32)
    elif FBL3N[moneda].iloc[0] == "PEN":
        FBL3N[monto] = FBL3N[monto].astype(np.float32)

    FBL3N[mayor] = FBL3N[mayor].astype(np.int64)
    FBL3N[n_doc] = FBL3N[n_doc].astype(np.int64)
    
    return FBL3N


def leer_FBL5N(ruta):
    FBL5N = leer_excel(ruta)

    # Obtener columnas
    sociedad, cuenta, n_doc, monto, moneda = [
        FBL5N.columns[i] for i in (0, 2, 4, 14, 15)
    ]

    # Limpiar tabla
    FBL5N.dropna(subset={n_doc, monto}, inplace=True)

    if len(FBL5N) == 0:
        return FBL5N
    
    # Convertir columnas
    if FBL5N[moneda].iloc[0] == "CLP":
        FBL5N[monto] = FBL5N[monto].astype(np.int32)
    elif FBL5N[moneda].iloc[0] == "PEN":
        FBL5N[monto] = FBL5N[monto].astype(np.float32)

    FBL5N[sociedad] = FBL5N[sociedad].astype(np.int16)
    FBL5N[cuenta] = FBL5N[cuenta].astype(np.int64)
    FBL5N[n_doc] = FBL5N[n_doc].astype(np.int64)

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
            print("No existe un archivo '{}'.".format(ruta))
            input("Presione Enter para salir.")
            exit()
		    
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
            print("No existe un archivo '{}'.".format(ruta))
            input("Presione Enter para salir.")
            exit()
		    
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
