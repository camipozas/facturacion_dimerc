import pandas as pd
from func_rw import *
from func_recon import *
from func_match import *
from func_f import *

""" MAIN """

print("1. Reconocimiento")
print("2. Calces")
print("3. Salir")

opcion = input("Elija una opción [1, 2, 3]: ")
while opcion not in ("1", "2", "3"):
    opcion = input("Ingrese una opción válida [1, 2, 3]: ")



""" PARTE 1. RECONOCIMIENTO """

if opcion == "1":
    # Leer archivos
    sociedad = input("Ingrese la sociedad: ")
    FBL3N = leer_excel("{} Bancos.xlsx".format(sociedad))
    KNA1 = leer_excel("KNA1.xlsx")

    # Reconocer RUTs/RUCs (y luego IDs), y números de factura
    print("Realizando reconocimiento de datos...")
    ID_FBL3N, FACT_FBL3N = reconocer(FBL3N, KNA1)

    # Liberar memoria
    del FBL3N
    del KNA1

    # Solicitar escribir los archivos
    print("Reconocimiento finalizado.")
    opcion = input("¿Desea escribir los archivos? [S/N]: ")
    while opcion not in ("S", "s", "N", "n"):
        opcion = input("Ingrese una opción válida [S/N]: ")
    if opcion in ("S", "s"):
        nombre_id = "{} Bancos - IDs.xlsx".format(sociedad)
        nombre_fact = "{} Bancos - Facturas.xlsx".format(sociedad)
        escribir_excel(ID_FBL3N, nombre_id)
        escribir_excel(FACT_FBL3N, nombre_fact)


    
""" PARTE 2. CALCES """

if opcion == "2":
    print("¿Qué archivos desea leer?")
    print("1. IDs")
    print("2. Facturas")
    print("3. Ambos archivos")

    opcion = input("Elija una opción [1, 2, 3]: ")
    while opcion not in ("1", "2", "3"):
        opcion = input("Ingrese una opción válida [1, 2, 3]: ")

    sociedad = input("Ingrese la sociedad: ")

    # Leer archivos
    if opcion in ("1", "3"):
        ID_FBL3N = leer_excel("{} Bancos - IDs.xlsx".format(sociedad))
    if opcion in ("2", "3"):
        FACT_FBL3N = leer_excel("{} Bancos - Facturas.xlsx".format(sociedad))
        
    FBL5N = leer_excel("{} PAs.xlsx".format(sociedad))

    # Realizar calces por ID
    if opcion in ("1", "3"):
        MATCHES_ID = calzar_por_id(ID_FBL3N, FBL5N)

        # Dar formato
        MATCHES_ID_USUARIO = formatear_para_usuario_id(MATCHES_ID)
        MATCHES_ID_EXPORTAR = formatear_para_exportar(MATCHES_ID)

        # Escribir archivos
        nombre_usuario_id = "{} Resultados Usuario - IDs.xlsx".format(sociedad)
        nombre_exportar_id = "{} Resultados Exportar - IDs.csv".format(sociedad)
        escribir_excel(MATCHES_ID_USUARIO, nombre_usuario_id)
        escribir_csv(MATCHES_ID_EXPORTAR, nombre_exportar_id)
        
    # Realizar calces por factura
    if opcion in ("2", "3"):
        MATCHES_FACT = calzar_por_factura(FACT_FBL3N, FBL5N)

        # Dar formato
        MATCHES_FACT_USUARIO = formatear_para_usuario_fact(MATCHES_FACT)
        MATCHES_FACT_EXPORTAR = formatear_para_exportar(MATCHES_FACT)

        # Escribir archivos
        nombre_usuario_fact = "{} Resultados Usuario - Facturas.xlsx".format(sociedad)
        nombre_exportar_fact = "{} Resultados Exportar - Facturas.csv".format(sociedad)
        escribir_excel(MATCHES_FACT_USUARIO, nombre_usuario_fact)
        escribir_csv(MATCHES_FACT_EXPORTAR, nombre_exportar_fact)



if opcion == "3":
    pass
