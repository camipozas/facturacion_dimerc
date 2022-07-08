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
