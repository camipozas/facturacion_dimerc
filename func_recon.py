<<<<<<< HEAD
import pandas as pd
import numpy as np
import re

""" RECONOCER RUT O RUC """

def detectar_rut(texto):
    if type(texto) != str:
        return np.nan
    
    def digito_verificador(secuencia):
        secuencia = secuencia.replace(".", "")
        suma = 0
        for i in range(len(secuencia)):
            factor = i%6 + 2
            indice = -i - 1
            suma += int(secuencia[indice]) * factor

        digito = 11 - (suma % 11)
        if digito == 11:
            return "0"
        if digito == 10:
            return "K"
        return str(digito)

    # Buscar secuencias de 8 y de 7 dígitos
    # Patrones de la forma XXXXXXXX o XX.XXX.XXX
    patron_pre_rut_8 = r"[1-9]\d{7}|[1-9]\d\.\d{3}\.\d{3}"
    # Patrones de la forma XXXXXXX o X.XXX.XXX
    patron_pre_rut_7 = r"[1-9]\d{6}|[1-9]\.\d{3}\.\d{3}"

    # Primero buscar posibles patrones de 8 dígitos
    coincidencias  = re.findall(patron_pre_rut_8, texto)
    # Luego, buscar posibles patrones de 7 dígitos POR SEPARADO,
    # y juntar los nuevos resultados con los anteriores
    coincidencias += re.findall(patron_pre_rut_7, texto)

    for secuencia in coincidencias:
        # Calcular el dígito verificador para cada secuencia encontrada.
        # Si es K, buscar k o K en el texto
        dv = digito_verificador(secuencia)
        if dv == "K":
            patron_rut = secuencia + r"-?[kK]"
        else:
            patron_rut = secuencia + r"-?" + dv

        # Si coincide el DV, retornar el RUT sin puntos y con guion
        if re.search(patron_rut, texto):
            return secuencia.replace(".", "") + "-" + dv
        
    return np.nan


def detectar_ruc(texto):
    if type(texto) == int and texto // 1000000000 in (10, 20):
        return texto
    elif type(texto) != str:
        return np.nan

    # Detectar secuencias de 11 dígitos, donde el primer dígito es 1 o 2,
    # y el segundo es 0
    
    coincidencias  = re.search(r"[12]0\d{9}", texto)
    if coincidencias:
        return coincidencias.group()
        
    return np.nan



""" RECONOCER NÚMERO DE FACTURA """

def detectar_n_factura(texto):
    if type(texto) == int and texto // 1000000 in range(1, 10):
        return texto
    elif type(texto) != str:
        return np.nan

    texto = texto.upper()
    c_factura = re.search(r"\bF(A(CT(URA(S)?)?)?)?.*\d+", texto)
    if c_factura:
        numero = re.search(r"\d+", c_factura.group())
        return numero.group().lstrip("0")
    else:
        patron_factura = r"(?<!\d)0*[1-9]\d{6}(?!\d)"
        coincidencia = re.search(patron_factura, texto)
        if coincidencia:
            return coincidencia.group().lstrip("0")
        
    return np.nan



""" FUNCIÓN PRINCIPAL """

def reconocer(FBL3N, KNA1):
    # Obtener columnas a trabajar
    columnas_FBL3N = FBL3N.columns
    clase, monto, moneda, texto = [columnas_FBL3N[i] for i in (7, 11, 12, 17)]

    columnas_KNA1 = KNA1.columns
    ID = columnas_KNA1[6]
    
    # Filtrar solo CTs
    FBL3N = FBL3N[FBL3N[clase] == "CT"].copy()

    if len(FBL3N) == 0:
        print("Error: no hay documentos de clase CT en el archivo.")
        raise Exception
    
    # Reconocer RUT o RUC según corresponda
    moneda_local = FBL3N[moneda][0]
    textos = FBL3N[texto]
    if moneda_local == "CLP":
        FBL3N["DNI"] = textos.apply(detectar_rut)
    elif moneda_local == "PEN":
        FBL3N["DNI"] = textos.apply(detectar_ruc)
    else:
        print("Moneda local no reconocida")
        raise Exception
    
    # Filtrar datos en KNA1, eliminando aquellos sin ID
    KNA1.dropna(subset=[ID], inplace=True)

    # Hay datos numéricos en esta columna. Convertirlos todos a string
    KNA1[ID] = KNA1[ID].astype(str)

    # Realizar un merge outer entre FBL3N y KNA1, para después filtrar los datos
    resultados = pd.merge(
        FBL3N, KNA1,
        left_on="DNI", right_on=ID,
        how="outer", indicator=True
    )

    # ID_FBL3N son todos los registros de FBL3N pareados con un ID de KNA1.
    # NO_ID_FBL3N son todos los demás, los que no fueron pareados con un ID.
    ID_FBL3N = resultados[resultados["_merge"] == "both"].copy()
    NO_ID_FBL3N = resultados[resultados["_merge"] == "left_only"].copy()

    del resultados

    # En NO_ID_FBL3N, reconocer todos los números de factura
    textos = NO_ID_FBL3N[texto]
    NO_ID_FBL3N["Nº factura"] = textos.apply(detectar_n_factura)
    FACT_FBL3N = NO_ID_FBL3N[pd.notna(NO_ID_FBL3N["Nº factura"])]

    # Seleccionar solo las columnas necesarias
    ID_FBL3N = ID_FBL3N[
        np.concatenate([columnas_FBL3N, ["DNI"], columnas_KNA1])
        ].copy()
    FACT_FBL3N = FACT_FBL3N[
        np.concatenate([columnas_FBL3N, ["Nº factura"]])
        ].copy()

    # Resetear el índice
    ID_FBL3N.reset_index(drop=True, inplace=True)
    FACT_FBL3N.reset_index(drop=True, inplace=True)
    
    return ID_FBL3N, FACT_FBL3N
=======
import pandas as pd
import numpy as np
import re

""" RECONOCER RUT O RUC """

def detectar_rut(texto):
    if type(texto) != str:
        return np.nan
    
    def digito_verificador(secuencia):
        secuencia = secuencia.replace(".", "")
        suma = 0
        for i in range(len(secuencia)):
            factor = i%6 + 2
            indice = -i - 1
            suma += int(secuencia[indice]) * factor

        digito = 11 - (suma % 11)
        if digito == 11:
            return "0"
        if digito == 10:
            return "K"
        return str(digito)

    # Buscar secuencias de 8 y de 7 dígitos
    # Patrones de la forma XXXXXXXX o XX.XXX.XXX
    patron_pre_rut_8 = r"[1-9]\d{7}|[1-9]\d\.\d{3}\.\d{3}"
    # Patrones de la forma XXXXXXX o X.XXX.XXX
    patron_pre_rut_7 = r"[1-9]\d{6}|[1-9]\.\d{3}\.\d{3}"

    # Primero buscar posibles patrones de 8 dígitos
    coincidencias  = re.findall(patron_pre_rut_8, texto)
    # Luego, buscar posibles patrones de 7 dígitos POR SEPARADO,
    # y juntar los nuevos resultados con los anteriores
    coincidencias += re.findall(patron_pre_rut_7, texto)

    for secuencia in coincidencias:
        # Calcular el dígito verificador para cada secuencia encontrada.
        # Si es K, buscar k o K en el texto
        dv = digito_verificador(secuencia)
        if dv == "K":
            patron_rut = secuencia + r"-?[kK]"
        else:
            patron_rut = secuencia + r"-?" + dv

        # Si coincide el DV, retornar el RUT sin puntos y con guion
        if re.search(patron_rut, texto):
            return secuencia.replace(".", "") + "-" + dv
        
    return np.nan


def detectar_ruc(texto):
    if type(texto) == int and texto // 1000000000 in (10, 20):
        return texto
    elif type(texto) != str:
        return np.nan

    # Detectar secuencias de 11 dígitos, donde el primer dígito es 1 o 2,
    # y el segundo es 0
    
    coincidencias  = re.search(r"[12]0\d{9}", texto)
    if coincidencias:
        return coincidencias.group()
        
    return np.nan



""" RECONOCER NÚMERO DE FACTURA """

def detectar_n_factura(texto):
    if type(texto) == int and texto // 1000000 in range(1, 10):
        return texto
    elif type(texto) != str:
        return np.nan

    texto = texto.upper()
    c_factura = re.search(r"\bF(A(CT(URA(S)?)?)?)?.*\d+", texto)
    if c_factura:
        numero = re.search(r"\d+", c_factura.group())
        return numero.group().lstrip("0")
    else:
        patron_factura = r"(?<!\d)0*[1-9]\d{6}(?!\d)"
        coincidencia = re.search(patron_factura, texto)
        if coincidencia:
            return coincidencia.group().lstrip("0")
        
    return np.nan



""" FUNCIÓN PRINCIPAL """

def reconocer(FBL3N, KNA1):
    # Filtrar solo CTs
    FBL3N = FBL3N[FBL3N["Clase de documento"] == "CT"].copy()

    if len(FBL3N) == 0:
        print("Error: no hay documentos de clase CT en el archivo.")
        raise Exception

    # Esto servirá para más adelante
    columnas = FBL3N.columns
    
    # Reconocer RUT o RUC según corresponda
    moneda_local = FBL3N["Moneda local"][0]
    textos = FBL3N["Texto"]
    if moneda_local == "CLP":
        FBL3N["DNI"] = textos.apply(detectar_rut)
    elif moneda_local == "PEN":
        FBL3N["DNI"] = textos.apply(detectar_ruc)
    else:
        print("Moneda local no reconocida")
        raise Exception
    
    # Filtrar datos en KNA1, eliminando aquellos sin ID
    KNA1.dropna(subset=["Nº ident.fis.1"], inplace=True)

    # Hay datos numéricos en esta columna. Convertirlos todos a string
    KNA1["Nº ident.fis.1"] = KNA1["Nº ident.fis.1"].astype(str)

    # Realizar un merge outer entre FBL3N y KNA1, para después filtrar los datos
    resultados = pd.merge(
        FBL3N, KNA1,
        left_on="DNI", right_on="Nº ident.fis.1",
        how="outer", indicator=True
    )

    # ID_FBL3N son todos los registros de FBL3N pareados con un ID de KNA1.
    # NO_ID_FBL3N son todos los demás, los que no fueron pareados con un ID.
    ID_FBL3N = resultados[resultados["_merge"] == "both"].copy()
    NO_ID_FBL3N = resultados[resultados["_merge"] == "left_only"].copy()

    del resultados

    # En NO_ID_FBL3N, reconocer todos los números de factura
    textos = NO_ID_FBL3N["Texto"]
    NO_ID_FBL3N["Nº factura"] = textos.apply(detectar_n_factura)
    FACT_FBL3N = NO_ID_FBL3N[pd.notna(NO_ID_FBL3N["Nº factura"])]

    # Seleccionar solo las columnas necesarias
    ID_FBL3N = ID_FBL3N[np.concatenate([columnas, ["DNI"], KNA1.columns])].copy()
    FACT_FBL3N = FACT_FBL3N[np.concatenate([columnas, ["Nº factura"]])].copy()
    
    return ID_FBL3N, FACT_FBL3N
>>>>>>> 9d9a7c13d916eecb05a8a9377c0d96a4d57e8b5e
