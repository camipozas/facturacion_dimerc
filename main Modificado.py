import pandas as pd
import re
from datetime import date, datetime
from func_rw import *
from func_recon import *
from func_match import *
from func_f import *

""" MAIN """

print("¿Qué desea hacer?")
print("1. Reconocimiento")
print("2. Calces")
print("3. Salir")
print("")

opcion = input("Elija una opción [1, 2, 3]: ")
while opcion not in ("1", "2", "3"):
    opcion = input("Ingrese una opción válida [1, 2, 3]: ")



""" PARTE 1. RECONOCIMIENTO """

# Crear un flag para después
existe_FBL3N = False
if opcion == "1":
    # Leer archivos
    print("")
    sociedad = input("Ingrese la sociedad: ")
    print("")
    FBL3N = leer_FBL3N("{} Bancos.xlsx".format(sociedad))
    KNA1 = leer_excel("KNA1.xlsx")

    # Reconocer RUTs/RUCs (y luego IDs), y números de factura
    print("")
    print("Realizando reconocimiento de datos...")
    ID_FBL3N, FACT_FBL3N = reconocer(FBL3N, KNA1)

    # Liberar memoria
    del FBL3N
    del KNA1

    # Solicitar escribir los archivos
    print("Reconocimiento finalizado.")
    print("")
    opcion = input("¿Desea escribir los archivos? [S/N]: ")
    while opcion not in ("S", "s", "N", "n"):
        opcion = input("Ingrese una opción válida [S/N]: ")
    if opcion in ("S", "s"):
        nombre_id = "{} Bancos - IDs.xlsx".format(sociedad)
        nombre_fact = "{} Bancos - Facturas.xlsx".format(sociedad)
        escribir_excel(ID_FBL3N, nombre_id)
        escribir_excel(FACT_FBL3N, nombre_fact)

    print("")
    opcion = input("¿Desea realizar calces con estos archivos? [S/N]: ")
    while opcion not in ("S", "s", "N", "n"):
        opcion = input("Ingrese una opción válida [S/N]: ")
    if opcion in ("S", "s"):
        # Settear opcion = "2" para luego pasar a la parte de calces
        opcion = "2"
        # Settear un flag para reusar los archivos en vez de releerlos
        existe_FBL3N = True


    
""" PARTE 2. CALCES """

if opcion == "2":
    print("")
    print("¿Qué archivos desea leer?")
    print("1. IDs")
    print("2. Facturas")
    print("3. Ambos archivos")
    print("")
    
    opcion = input("Elija una opción [1, 2, 3]: ")
    while opcion not in ("1", "2", "3"):
        opcion = input("Ingrese una opción válida [1, 2, 3]: ")

    print("")
    if not existe_FBL3N:
        sociedad = input("Ingrese la sociedad: ")
    fecha_cont = input("Ingrese fecha de contabilización (DD.MM.AAAA): ")
    
    # Validar que la fecha esté en el formato indicado y no sea una fecha futura
    hoy = date.today()
    flag_1, flag_2 = False, False
    while not flag_1 or not flag_2:
        flag_1 = re.fullmatch(r"\d\d\.\d\d\.\d\d\d\d", fecha_cont)
        if not flag_1:
            fecha_cont = input("La fecha debe ser en el formato (DD.MM.AAAA): ")
        else:
            try:
                flag_2 = (datetime.strptime(fecha_cont, "%d.%m.%Y").date() <= hoy)
                if not flag_2:
                    fecha_cont = input("Debe ingresar una fecha no futura (DD.MM.AAAA): ")
            except:
                flag_2 = False
                fecha_cont = input("Debe ingresar una fecha válida (DD.MM.AAAA): ")

    # Leer archivos
    print("")
    if not existe_FBL3N:
        if opcion in ("1", "3"):
            ID_FBL3N = leer_FBL3N("{} Bancos - IDs.xlsx".format(sociedad))
        if opcion in ("2", "3"):
            FACT_FBL3N = leer_FBL3N("{} Bancos - Facturas.xlsx".format(sociedad))
        
    FBL5N = leer_FBL5N("{} PAs.xlsx".format(sociedad))

    # Agregar fecha de contabilización
    if opcion in ("1", "3"):
        ID_FBL3N["Fecha nueva cont."] = fecha_cont
    if opcion in ("2", "3"):
        FACT_FBL3N["Fecha nueva cont."] = fecha_cont

    # Realizar calces por ID y por factura
    print("")
    print("Realizando calce...")
    if opcion in ("1", "3"):
        MATCHES_ID = calzar_por_id(ID_FBL3N, FBL5N)
        del ID_FBL3N
    if opcion in ("2", "3"):
        MATCHES_FACT = calzar_por_factura(FACT_FBL3N, FBL5N)
        del FACT_FBL3N
    del FBL5N

    # Pedir información adicional para dar formato a datos
    datos = {}

    print("")
    string = input("Ingrese XBLNR (referencia). Ej: ABONOMASIVO: ")
    while len(string) > 16:
        string = input("Debe ingresar un string de no más de 16 caracteres de largo: ")
    datos["XBLNR"] = string

    string = input("Ingrese BKTXT (texto). Ej: 202201_001: ")
    while len(string) > 10:
        string = input("Debe ingresar un string de no más de 10 caracteres de largo: ")
    datos["BKTXT"] = string
    
    string = input("Ingrese AUGTX (texto). Ej: BancoSantander: ")
    while len(string) > 18:
        string = input("Debe ingresar un string de no más de 18 caracteres de largo: ")
    datos["AUGTX"] = string
    
    # Dar formato y escribir archivos
    if opcion in ("1", "3"):
        MATCHES_ID_USUARIO = formatear_para_usuario_id(MATCHES_ID)
        MATCHES_ID_EXPORTAR = formatear_para_exportar_id(MATCHES_ID, datos)
        del MATCHES_ID

        nombre_usuario_id = "{} Resultados Usuario - IDs.xlsx".format(sociedad)
        nombre_exportar_id = "{} Resultados Exportar - IDs.csv".format(sociedad)
        escribir_excel(MATCHES_ID_USUARIO, nombre_usuario_id)
        escribir_csv(MATCHES_ID_EXPORTAR, nombre_exportar_id)
        
    if opcion in ("2", "3"):
        MATCHES_FACT_USUARIO = formatear_para_usuario_fact(MATCHES_FACT)
        MATCHES_FACT_EXPORTAR = formatear_para_exportar_fact(MATCHES_FACT, datos)
        del MATCHES_FACT

        nombre_usuario_fact = "{} Resultados Usuario - Facturas.xlsx".format(sociedad)
        nombre_exportar_fact = "{} Resultados Exportar - Facturas.csv".format(sociedad)
        escribir_excel(MATCHES_FACT_USUARIO, nombre_usuario_fact)
        escribir_csv(MATCHES_FACT_EXPORTAR, nombre_exportar_fact)

    input("Presione Enter para salir.")


if opcion == "3":
    pass
