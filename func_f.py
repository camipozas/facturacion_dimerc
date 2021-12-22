<<<<<<< HEAD
import pandas as pd
import numpy as np
from datetime import date, datetime

def formatear_para_usuario_id(tabla):
    nombres = [
        (56, "Correlativo"),
        (28, "Sociedad"),
        ( 5, "Nº documento BANCO"),
        (27, "Fecha contabilización"),
        ( 7, "Clase de documento BANCO"),
        (11, "Monto BANCO"),
        (12, "Moneda local BANCO"),
        (17, "Texto"),
        (20, "Cliente"),
        (26, "Nº ident.fis.1"),
        (22, "Nombre 1"),
        (33, "Asignación"),
        (32, "Nº documento PA"),
        (34, "Referencia"),
        (31, "Clase de documento PA"),
        (42, "Monto PA"),
        (43, "Moneda local PA"),
    ]

    cambios_nombres = {
        tabla.columns[i]: nombre
        for i, nombre in nombres
        }

    _, columnas = zip(*nombres)
    columnas = list(columnas)

    tabla = tabla.copy()
    tabla = tabla.rename(columns=cambios_nombres)
    return tabla[columnas].copy()

def formatear_para_usuario_fact(tabla):    
    nombres = [
        (49, "Correlativo"),
        (21, "Sociedad"),
        ( 5, "Nº documento BANCO"),
        (20, "Fecha contabilización"),
        ( 7, "Clase de documento BANCO"),
        (11, "Monto BANCO"),
        (12, "Moneda local BANCO"),
        (17, "Texto"),
        (19, "Nº factura"),
        (26, "Asignación"),
        (25, "Nº documento PA"),
        (27, "Referencia"),
        (24, "Clase de documento PA"),
        (35, "Monto PA"),
        (36, "Moneda local PA"),
    ]

    cambios_nombres = {
        tabla.columns[i]: nombre
        for i, nombre in nombres
        }

    _, columnas = zip(*nombres)
    columnas = list(columnas)

    tabla = tabla.copy()
    tabla = tabla.rename(columns=cambios_nombres)
    return tabla[columnas].copy()


def formatear_para_exportar_id(tabla, datos):
    nombres = [
        (56, "CORR"),
        (27, "BUDAT"),
        ( 9, "VALUT"),
        (28, "BUKRS"),
        (12, "WAERS"),
        ( 2, "KONTO"),
        (11, "WRBTR"),
        (30, "AGKON"),
        (17, "SGTXT"),
        (32, "BELNR"),
    ]

    cambios_nombres = {
        tabla.columns[i]: nombre
        for i, nombre in nombres
        }
    
    tabla = tabla.copy()
    tabla = tabla.rename(columns=cambios_nombres)
    return aux_exportar(tabla, datos)

def formatear_para_exportar_fact(tabla, datos):
    nombres = [
        (49, "CORR"),
        (20, "BUDAT"),
        ( 9, "VALUT"),
        (21, "BUKRS"),
        (12, "WAERS"),
        ( 2, "KONTO"),
        (11, "WRBTR"),
        (23, "AGKON"),
        (17, "SGTXT"),
        (25, "BELNR"),
    ]

    cambios_nombres = {
        tabla.columns[i]: nombre
        for i, nombre in nombres
        }

    tabla = tabla.copy()
    tabla = tabla.rename(columns=cambios_nombres)
    return aux_exportar(tabla, datos)

def aux_exportar(tabla, datos):
    columnas = [
        "CORR",
        "BLDAT",
        "BUDAT",
        "VALUT",
        "BLART",
        "BUKRS",
        "WAERS",
        "XBLNR",
        "BKTXT",
        "KONTO",
        "WRBTR",
        "AGKON",
        "AGUMS",
        "KOART",
        "AUGTX",
        "SGTXT",
        "BELNR",
    ]
                           
    if len(tabla) == 0:
        return pd.DataFrame(columns=columnas)

    # Agregar algunas columnas
    tabla["BLART"] = "DZ"
    tabla["XBLNR"] = datos["XBLNR"]
    tabla["BKTXT"] = datos["BKTXT"]
    tabla["AGUMS"] = ""
    tabla["KOART"] = "D"
    tabla["AUGTX"] = datos["AUGTX"]

    # Cambiar el formato de la fecha de valor
    tabla["VALUT"] = tabla["VALUT"].dt.strftime("%d.%m.%Y")

    # Agregar una fecha
    tabla["BLDAT"] = tabla["BUDAT"]

    # Sacar valor absoluto de los montos
    tabla["WRBTR"] = tabla["WRBTR"].abs()

    # Seleccionar columnas
    return tabla[columnas].copy()
=======
import pandas as pd
import numpy as np
from datetime import date, datetime

def formatear_para_usuario_fact(tabla):
    cambios_nombres = {
        "Sociedad PA": "Sociedad",
        "Importe en moneda local BANCO": "Importe en moneda local",
        "Moneda local BANCO": "Moneda local",
        "Texto BANCO": "Texto",
        "Nº factura BANCO": "Nº factura",
        "Asignación PA": "Asignación",
        "Referencia PA": "Referencia",
        "Importe en moneda doc. PA": "Importe en moneda doc.",
        "Moneda del documento PA": "Moneda del documento",
        "Fecha nueva cont. BANCO": "Fecha contabilización",
    }
    
    columnas = [
        "Correlativo",
        "Sociedad",
        "Nº documento BANCO",
        "Clase de documento BANCO",
        "Importe en moneda local",
        "Moneda local",
        "Texto",
        "Nº factura",
        "Asignación",
        "Nº documento PA",
        "Referencia",
        "Clase de documento PA",
        "Importe en moneda doc.",
        "Moneda del documento",
    ]

    tabla = tabla.copy()
    tabla = tabla.rename(columns=cambios_nombres)
    return tabla[columnas].copy()


def formatear_para_usuario_id(tabla):
    cambios_nombres = {
        "Sociedad PA": "Sociedad",
        "Importe en moneda local BANCO": "Importe en moneda local",
        "Moneda local BANCO": "Moneda local",
        "Texto BANCO": "Texto",
        "Cliente BANCO": "Cliente",
        "Nº ident.fis.1 BANCO": "Nº ident.fis.1",
        "Nombre 1 BANCO": "Nombre 1",
        "Asignación PA": "Asignación",
        "Referencia PA": "Referencia",
        "Importe en moneda doc. PA": "Importe en moneda doc.",
        "Moneda del documento PA": "Moneda del documento",
    }
    
    columnas = [
        "Correlativo",
        "Sociedad",
        "Nº documento BANCO",
        "Clase de documento BANCO",
        "Importe en moneda local",
        "Moneda local",
        "Texto",
        "Cliente",
        "Nº ident.fis.1",
        "Nombre 1",
        "Asignación",
        "Nº documento PA",
        "Referencia",
        "Clase de documento PA",
        "Importe en moneda doc.",
        "Moneda del documento",
    ]

    tabla = tabla.copy()
    tabla = tabla.rename(columns=cambios_nombres)
    return tabla[columnas].copy()

def formatear_para_exportar(tabla):
    cambios_nombres = {
        "Correlativo": "CORR",
        "Fecha nueva cont. BANCO": "BUDAT",
        "Fecha valor BANCO": "VALUT",
        "Sociedad PA": "BUKRS",
        "Moneda local BANCO": "WAERS",
        "Cuenta de mayor BANCO": "KONTO",
        "Importe en moneda local BANCO": "WRBTR",
        "Cuenta PA": "AGKON",
        "Texto BANCO": "SGTXT",
        "Nº documento PA": "BELNR",
    }

    columnas = [
        "CORR",
        "BLDAT",
        "BUDAT",
        "VALUT",
        "BLART",
        "BUKRS",
        "WAERS",
        "XBLNR",
        "BKTXT",
        "KONTO",
        "WRBTR",
        "AGKON",
        "AGUMS",
        "KOART",
        "AUGTX",
        "SGTXT",
        "BELNR",
    ]
                           
    if len(tabla) == 0:
        return pd.DataFrame(columns=columnas)
    
    tabla = tabla.copy()

    # Agregar algunas columnas
    tabla["BLART"] = "DZ"
    
    string = input("XBLNR (referencia): ")
    while len(string) > 16:
        string = input("Debe ingresar un string de no más de 16 caracteres de largo: ")
    tabla["XBLNR"] = string

    string = input("BKTXT (texto): ")
    while len(string) > 10:
        string = input("Debe ingresar un string de no más de 10 caracteres de largo: ")
    tabla["BKTXT"] = string
    
    tabla["AGUMS"] = ""
    tabla["KOART"] = "D"

    string = input("AUGTX (texto): ")
    while len(string) > 18:
        string = input("Debe ingresar un string de no más de 18 caracteres de largo: ")
    tabla["AUGTX"] = string

    # Renombrar columnas   
    tabla = tabla.rename(columns=cambios_nombres)

    # Cambiar el formato de la fecha de valor
    tabla["VALUT"] = tabla["VALUT"].dt.strftime("%d.%m.%Y")

    # Agregar una fecha
    tabla["BLDAT"] = tabla["BUDAT"]

    # Sacar valor absoluto de los montos
    tabla["WRBTR"] = tabla["WRBTR"].abs()

    # Seleccionar columnas
    return tabla[columnas].copy()
>>>>>>> 9d9a7c13d916eecb05a8a9377c0d96a4d57e8b5e
