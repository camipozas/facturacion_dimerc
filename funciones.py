import pandas as pd
import numpy as np
import re

def detectar_categoria(texto):
    if type(texto) != str:
        return np.nan
    
    texto = texto.upper()
    
    if "PROVEE" in texto:
        return "Proveedor"
    if "INVER" in texto:
        return "Inversión"
    if "COTIZACION" in texto:
        return "Cotización"
    if "ASIGNA" in texto:
        return "Asignación"
    if "TRANSF" in texto:
        return "Transferencia"
    if "DEP" in texto:
        return "Depósito"

    c_factura = re.search(r"\bF(A(CT(URA(S)?)?)?)?.*\d+", texto)
    if c_factura:
        return "Factura"
    
    return np.nan

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
    coincidencias  = re.findall(patron_pre_rut_8, texto)
    coincidencias += re.findall(patron_pre_rut_7, texto)

    for secuencia in coincidencias:
        dv = digito_verificador(secuencia)
        if dv == "K":
            patron_rut = secuencia + r"-?[kK]"
        else:
            patron_rut = secuencia + r"-?" + dv

        if re.search(patron_rut, texto):
            return secuencia.replace(".", "") + dv
        
    return np.nan

def detectar_n_factura(texto):
    if type(texto) == int and texto % 1000000 > 0:
        return texto
    elif type(texto) != str:
        return np.nan

    texto = texto.upper()
    c_factura = re.search(r"\bF(A(CT(URA(S)?)?)?)?.*\d+", texto)
    if c_factura:
        numero = re.search(r"\d+", c_factura.group())
        return numero.group()
    else:
        patron_factura = r"(?<!\d)0*[1-9]\d{6}(?!\d)"
        coincidencia = re.search(patron_factura, texto)
        if coincidencia:
            return coincidencia.group()
        
    return np.nan

def detectar_numeros(texto):
    if type(texto) == int:
        return texto
    elif type(texto) != str:
        return np.nan
    
    numero = re.search(r"\d+", texto)
    if numero:
        return numero.group()
    return np.nan
    
def leer_archivo(ruta):
	while True:
		try:
		    print("Leyendo archivo Excel:", ruta)
		    dataframe = pd.read_excel(ruta)
		    print("Archivo Excel leído.")
		    break
		except PermissionError:
		    print("Error: el archivo ya está abierto. Ciérralo y vuelve a intentarlo.")
		    input("Presiona Enter cuando esté listo.")
		except:
			print("Ocurrió un error extraño")
			return None
		    
	return dataframe
    
def escribir_archivo(dataframe, ruta):
	while True:
		try:
		    print("Escribiendo nuevo archivo Excel:", ruta)
		    dataframe.to_excel(ruta)
		    print("Archivo Excel escrito.")
		    break
		except PermissionError:
		    print("Error: el archivo ya está abierto. Ciérralo y vuelve a intentarlo.")
		    input("Presiona Enter cuando esté listo.")
		except:
			print("Ocurrió un error extraño")

"""
def detectar_n_factura_1(texto):
    # Si está categorizado como "Factura"
    if type(texto) != str:
        return np.nan

    

def detectar_n_factura_2(texto):
    # Si NO está categorizado como "Factura"
    if type(texto) != str:
        return np.nan

    # Se buscan secuencias de EXACTAMENTE 7 dígitos
    patron_factura = r"(?<!\d)0*[1-9]\d{6}(?!\d)"
    coincidencias = re.findall(patron_factura, texto)
    if coincidencias:
        return int(coincidencias[0])
    return np.nan

"""
