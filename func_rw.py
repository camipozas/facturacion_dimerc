import pandas as pd

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
