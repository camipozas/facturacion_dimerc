import numpy as np
import pandas as pd
from match_1_M_aux import *

def limites(arr):
    # Obtener límites de cada grupo de datos
    # Se entiende por "grupo" todos los datos con la misma ID.
    #
    # Ejemplo: arr = [101 101 101 102 102 103 103 103 103]
    # Hay 3 grupos:
    # - 101: elementos del 0 al 2 (0:3)
    # - 102: elementos del 3 al 4 (3:5)
    # - 103: elementos del 5 al 8 (5:9)
    #
    # En este ejemplo, los "límites" son el arreglo [0, 3, 5, 9].
    # Si quiero obtener el grupo 1, solo hago A[0:3], o A[lim[0]:lim[1]]
    # SI quiero obtener el grupo 3, solo hago A[5:9], o A[lim[2]:lim[3]]
    #
    # Para obtener estos límites, hay que analizar cuándo hay una diferencia
    # entre el elemento actual y el siguiente.
    # Por ejemplo, al analizar 101 y 101, son iguales por lo que pertenecen
    # al mismo grupo. Pero al analizar 101 y 102, son distintos: aquí ocurrió
    # un cambio de grupo.
    #
    # El truco acá es comparar el arreglo con una copia "desplazada" de sí mismo.
    # Esto se logra así:
    # - Agregando un elemento vacío al inicio de una copia
    # - Agregando un elemento vacío al final de otra copia
    # - Comparar ambas copias
    #
    # En el ejemplo anterior, sería comparar los siguientes arreglos y ver
    # cuándo son iguales y cuándo son distintos:
    # arr1 = [""    101   101   101   102   102   103   103   103   103  ]
    # arr2 = [101   101   101   102   102   103   103   103   103   ""   ]
    # 
    # res  = [True  False False True  False True  False False False True ]
    #
    # Finalmente, obtener los índices donde R = True. Es decir, 0, 3, 5 y 9.
    
    return np.where(np.append([""], arr) != np.append(arr, [""]))[0]
    

def extraer_datos(FBL3N, FBL5N):
    # Obtener ndarrays (arreglos de NumPy) importantes
    # a partir de FBL3N y FBL5N
    ind3 = np.arange(len(FBL3N.index))
    ids3 = FBL3N["Cliente"].to_numpy()
    mon3 = -FBL3N["Importe en moneda local"].to_numpy()

    ind5 = np.arange(len(FBL5N.index))
    ids5 = FBL5N["Cuenta"].to_numpy()
    mon5 = FBL5N["Importe en moneda doc."].to_numpy()
    dem5 = FBL5N["Demora tras vencimiento neto"].to_numpy()

    D = {"ORD": {}, "1-1": {}, "1-T": {}, "1-V": {}, "1-M": {}, "SOL": {3: {}, 5: {}}}

    # Separar partidas que estén solas
    filtro3 = np.isin(ids3, ids5)
    filtro5 = np.isin(ids5, ids3)

    ids3_sol = ids3[~filtro3]
    ind3_sol = ind3[~filtro3]
    ids5_sol = ids5[~filtro5]
    ind5_sol = ind5[~filtro5]

    i3_sol = np.argsort(ids3_sol)
    ind3_sol = ind3_sol[i3_sol]
    lim3_sol = limites(ids3_sol[i3_sol])

    i5_sol = np.argsort(ids5_sol)
    ind5_sol = ind5_sol[i5_sol]
    lim5_sol = limites(ids5_sol[i5_sol])

    D["SOL"][3] = {
        ID: ind3_sol[ lim3_sol[i] : lim3_sol[i+1] ].copy()
        for i, ID in enumerate(np.unique(ids3_sol))
    }

    D["SOL"][5] = {
        ID: ind5_sol[ lim5_sol[i] : lim5_sol[i+1] ].copy()
        for i, ID in enumerate(np.unique(ids5_sol))
    }

    ind3 = ind3[filtro3]
    ids3 = ids3[filtro3]
    mon3 = mon3[filtro3]

    ind5 = ind5[filtro5]
    ids5 = ids5[filtro5]
    mon5 = mon5[filtro5]
    dem5 = dem5[filtro5]
    
    # Ordenar datos de FBL3N en base a las IDs
    i3 = np.argsort(ids3)
    ind3 = ind3[i3]
    mon3 = mon3[i3]
    lim3 = limites(ids3[i3])

    # Ordenar datos de FBL5N en base a las IDs y luego en base a las demoras
    i5 = np.lexsort((-dem5, ids5))
    ind5 = ind5[i5]
    mon5 = mon5[i5]
    dem5 = dem5[i5]
    lim5 = limites(ids5[i5])
    
    D["ORD"] = {
        ID: { 
            "ind3": ind3[ lim3[i] : lim3[i+1] ].copy(),
            "mon3": mon3[ lim3[i] : lim3[i+1] ].copy(),
            "ind5": ind5[ lim5[i] : lim5[i+1] ].copy(),
            "mon5": mon5[ lim5[i] : lim5[i+1] ].copy(),
            "dem5": dem5[ lim5[i] : lim5[i+1] ].copy(),
        } for i, ID in enumerate(np.unique(ids3))
    }
        
    return D


def match_1_1(D):
    for ID in D["ORD"].copy():
        datos = D["ORD"][ID]
        _, i3, i5 = np.intersect1d(datos["mon3"], datos["mon5"], return_indices=True)
        # Si hay matches, guardarlos en D["1-1"] y encargarse del resto de datos
        if i3.size > 0:
            D["1-1"][ID] = {
                "ind3": datos["ind3"][i3],
                "ind5": datos["ind5"][i5],
            }

            # Obtener complementos de i3 e i5
            ni3 = np.ones_like(datos["ind3"], dtype=bool)
            ni3[i3] = False
            ni5 = np.ones_like(datos["ind5"], dtype=bool)
            ni5[i5] = False

            # Si todavía sobran datos, guardar los restantes en D["ORD"],
            # sobreescribiendo lo que había ahí
            if i3.size < datos["ind3"].size and i5.size < datos["ind5"].size:
                D["ORD"][ID] = {
                    "ind3": datos["ind3"][ni3],
                    "mon3": datos["mon3"][ni3],
                    "ind5": datos["ind5"][ni5],
                    "mon5": datos["mon5"][ni5],
                    "dem5": datos["dem5"][ni5],
                }

            # En cambio, si se acabaron todas las partidas en FBL3N o FBL5N,
            # eliminar D["ORD"][ID]
            else:
                # Si hay partidas solas en FBL3N, guardarlas acá
                if i3.size < datos["ind3"].size:
                    if ID in D["SOL"][3]:     
                        D["SOL"][3][ID] = np.append(D["SOL"][3][ID], datos["ind3"][ni3])
                    else:
                        D["SOL"][3][ID] = datos["ind3"][ni3]

                # Si hay partidas solas en FBL5N, guardarlas acá
                elif i5.size < datos["ind5"].size:
                    if ID in D["SOL"][5]:     
                        D["SOL"][5][ID] = np.append(D["SOL"][5][ID], datos["ind5"][ni5])
                    else:
                        D["SOL"][5][ID] = datos["ind5"][ni5]
                
                D["ORD"].pop(ID)
            

def match_1_T(D):
    for ID in D["ORD"].copy():
        datos = D["ORD"][ID]
        suma = datos["mon5"].sum()
        _, i3, _ = np.intersect1d(datos["mon3"], suma, return_indices=True)
        # Si hay un match, guardarlo en D["1-T"] y borrarlo de D["ORD"].
        # Los datos restantes se irán a D["SOL"]
        if i3.size > 0:
            D["1-T"][ID] = {
                "ind3": datos["ind3"][i3],
                "ind5": datos["ind5"],
            }

            # Obtener complemento de i3
            ni3 = np.ones_like(datos["ind3"], dtype=bool)
            ni3[i3] = False

            # Si sobran datos en FBL3N, guardarlos en D["SOL"]
            if i3.size < datos["ind3"].size:
                if ID in D["SOL"][3]:     
                    D["SOL"][3][ID] = np.append(D["SOL"][3][ID], datos["ind3"][ni3])
                else:
                    D["SOL"][3][ID] = datos["ind3"][ni3]
                
            D["ORD"].pop(ID)


def match_1_V(D):
    for ID in D["ORD"].copy():
        datos = D["ORD"][ID]
        v = (datos["dem5"] > 0)
        suma = datos["mon5"][v].sum()
        _, i3, _ = np.intersect1d(datos["mon3"], suma, return_indices=True)
        # Si hay un match, guardarlo en D["1-V"].
        # Los datos restantes se irán a D["SOL"]
        if i3.size > 0:
            D["1-V"][ID] = {
                "ind3": datos["ind3"][i3],
                "ind5": datos["ind5"][v],
            }

            # Obtener complemento de i3
            ni3 = np.ones_like(datos["ind3"], dtype=bool)
            ni3[i3] = False

            # Si todavía sobran datos, guardar los restantes en D["ORD"],
            # sobreescribiendo lo que había ahí
            if i3.size < datos["ind3"].size and datos["ind5"][~v].size > 0:
                D["ORD"][ID] = {
                    "ind3": datos["ind3"][ni3],
                    "mon3": datos["mon3"][ni3],
                    "ind5": datos["ind5"][~v],
                    "mon5": datos["mon5"][~v],
                    "dem5": datos["dem5"][~v],
                }

            # En cambio, si se acabaron todas las partidas en FBL3N o FBL5N,
            # eliminar D["ORD"][ID]
            else:
                # Si hay partidas solas en FBL3N, guardarlas acá
                if i3.size < datos["ind3"].size:
                    if ID in D["SOL"][3]:     
                        D["SOL"][3][ID] = np.append(D["SOL"][3][ID], datos["ind3"][ni3])
                    else:
                        D["SOL"][3][ID] = datos["ind3"][ni3]

                # Si hay partidas solas en FBL5N, guardarlas acá
                elif datos["ind5"][~v].size > 0:
                    if ID in D["SOL"][5]:     
                        D["SOL"][5][ID] = np.append(D["SOL"][5][ID], datos["ind5"][~v])
                    else:
                        D["SOL"][5][ID] = datos["ind5"][~v]
                    
                D["ORD"].pop(ID)

def match_1_M(D):
    """
    NOTA IMPORTANTE
    Esta función requiere varias funciones auxiliares contenidas en
    funciones_aux_1_M.py

    Funciones usadas directamente aquí:
        indices_comb
        calcular_n_max
        
    Funciones requeridas por las anteriores:
        choose
    """

    """
    INDICES_20 = {}
    for largo in range(2, 21):
        INDICES_20[largo] = {}
        for n in range(2, largo+1):
            INDICES_20[largo][n] = indices_comb(largo, n)
    """
        
    for ID in D["ORD"].copy():
        datos = D["ORD"][ID]

        # Es importante tener registro de los índices de los datos que van
        # a hacer match. Por eso, se crean los arreglos range3 y range5, que
        # contienen los índices de los datos de FBL3N y FBL5N respectivamente
        # que le corresponden al cliente con esta ID.
        range3 = np.arange(datos["ind3"].size)
        range5 = np.arange(datos["ind5"].size)

        """
        filtro = (datos["mon5"] < (1 * datos["mon3"].max()))
        """

        # i3 contiene índices.
        # i5 contiene TUPLAS de índices.
        # Así, por ejemplo, puede ser que i3[0] = 1, e i5[0] = (3, 6, 10),
        # indicando que el elemento de índice 1 en FBL3N fue pareado con
        # los elementos de índices 3, 6 y 10 en FBL5N.
        #
        # ni3 es una SERIE BOOLEANA que representa el complemento de i3.
        #
        # ni5_flat es una SERIE BOOLEANA que vendría a ser el complemento
        # de un hipotético "i5_flat" que sería igual a True en todos
        # los índices de FBL5N ya seleccionados.
        # ni5_flat sería entonces False en todos aquellos índices, y True
        # en los que todavía no han sido usados. Esto sirve de filtro:
        # "datos["mon5"][ni5_flat]" son todos los datos de datos["mon5"]
        # que todavía no han sido seleccionados.
        i3 = []
        i5 = []
        ni3 = np.ones_like(datos["mon3"], dtype=bool)
        i5_flat = np.zeros_like(datos["mon5"], dtype=bool)

        largo = range5.size
        
        n = 2
        n_combs_restantes = 1000000
        while n <= largo and n_combs_restantes > 0:
            # Obtener arreglo de todas las combinaciones de n elementos
            # de datos["mon5"] que no estén siendo usados actualmente
            if False: #largo <= 20:
                indices = INDICES_20[largo][n]
            else:
                indices = indices_comb(largo, n, n_combs_restantes)
            suma_mon5 = datos["mon5"][indices].sum(axis=0)

            # Obtener índices en el arreglo de sumas donde sus elementos
            # estén contenidos entre los elementos no seleccionados de
            # datos["mon3"]
            si5 = np.nonzero(np.isin(suma_mon5, datos["mon3"][ni3]))[0]

            # Buscar entre todos los índices en suma_mon5 marcados
            for i in si5:
                indices5 = indices[:, i].flatten()
                
                # Si hay algún índice ocupado, descartar esta combinación
                if np.isin(indices5, np.nonzero(i5_flat)).any():
                    pass
                
                else:
                    # Buscar todos los datos restantes en datos["mon3"] cuyo
                    # monto coincida con el valor seleccionado de suma_mon5.
                    # Es posible que este dato haya sido marcado en una
                    # iteración anterior, por eso se debe verificar
                    j3 = (datos["mon3"][ni3] == suma_mon5[i])
                    if j3.any():
                        # Obtener el primer índice de entre los seleccionados
                        indice3 = range3[ni3][j3][0]
                        
                        i3.append(indice3)
                        i5.append(indices5)
                        
                        ni3[indice3] = False
                        i5_flat[indices5] = True

                        #largo = range5[ni5_flat].size
                        #n_max = calcular_n_max(largo)

            # Si todos los índices están ocupados (es decir, si todos los índices
            # en ni3 están marcados como False), terminar acá
            if not ni3.any():
                break

            n_combs_restantes -= choose(largo, n)
            #largo = datos["mon5"][ni5_flat]
            n += 1


        # Si hay un match, guardarlo en D["1-M"].
        # Los datos restantes se irán a D["SOL"]
        if len(i3) > 0:
            D["1-M"][ID] = [
                {
                    "ind3": datos["ind3"][[i3[i]]],
                    "ind5": datos["ind5"][ i5[i] ],
                }
                for i in range(len(i3))
            ]

            # Obtener complementos de i3 e i5
            
            ni3 = np.ones_like(datos["ind3"], dtype=bool)
            ni3[i3] = False

            i5 = [item for sublista in i5 for item in sublista]
            ni5 = np.ones_like(datos["ind5"], dtype=bool)
            ni5[i5] = False

            # Si todavía sobran datos, guardar los restantes en D["ORD"],
            # sobreescribiendo lo que había ahí
            if datos["ind3"][ni3].size > 0 and datos["ind5"][ni5].size > 0:
                D["ORD"][ID] = {
                    "ind3": datos["ind3"][ni3],
                    "mon3": datos["mon3"][ni3],
                    "ind5": datos["ind5"][ni5],
                    "mon5": datos["mon5"][ni5],
                    "dem5": datos["dem5"][ni5],
                }

            # En cambio, si se acabaron todas las partidas en FBL3N o FBL5N,
            # eliminar D["ORD"][ID]
            else:
                # Si hay partidas solas en FBL3N, guardarlas acá
                if datos["ind3"][ni3].size > 0:
                    if ID in D["SOL"][3]:     
                        D["SOL"][3][ID] = np.append(D["SOL"][3][ID], datos["ind3"][ni3])
                    else:
                        D["SOL"][3][ID] = datos["ind3"][ni3]

                # Si hay partidas solas en FBL5N, guardarlas acá
                elif datos["ind5"][ni5].size > 0:
                    if ID in D["SOL"][5]:     
                        D["SOL"][5][ID] = np.append(D["SOL"][5][ID], datos["ind5"][ni5])
                    else:
                        D["SOL"][5][ID] = datos["ind5"][ni5]
                
                D["ORD"].pop(ID)


def organizar_en_tabla(D, FBL3N, FBL5N):
    lista_doc = np.array([], dtype=str)
    lista_df = []

    FBL3N = FBL3N.add_suffix(" BANCO")
    FBL5N = FBL5N.add_suffix(" PA")

    # Agregar una nueva columna al final
    FBL5N["Correlativo"] = 0
    
    for ID in D["1-1"]:
        datos = D["1-1"][ID]

        for i in range(datos["ind3"].size):
            df3 = FBL3N.iloc[[datos["ind3"][i]]]
            doc = df3["Nº documento BANCO"].to_numpy()
            df3 = df3.reset_index(drop=True)
            
            df5 = FBL5N.iloc[[datos["ind5"][i]]]
            df5 = df5.reset_index(drop=True)
            
            df = pd.concat([df3, df5], axis=1)

            lista_df.append(df)
            lista_doc = np.append(lista_doc, [doc])

    for ID in D["1-T"]:
        datos = D["1-T"][ID]
        
        df3 = FBL3N.iloc[datos["ind3"]]
        doc = df3["Nº documento BANCO"].to_numpy()
        df3 = pd.DataFrame(np.repeat(df3.values, datos["ind5"].size, axis=0))
        df3 = df3.reset_index(drop=True)
        df3.columns = FBL3N.columns
        
        df5 = FBL5N.iloc[datos["ind5"]]
        df5 = df5.reset_index(drop=True)
        
        df = pd.concat([df3, df5], axis=1)
        
        lista_df.append(df)
        lista_doc = np.append(lista_doc, doc)

    for ID in D["1-V"]:
        datos = D["1-V"][ID]
        
        df3 = FBL3N.iloc[datos["ind3"]]
        doc = df3["Nº documento BANCO"].to_numpy()
        df3 = pd.DataFrame(np.repeat(df3.values, datos["ind5"].size, axis=0))
        df3 = df3.reset_index(drop=True)
        df3.columns = FBL3N.columns
        
        df5 = FBL5N.iloc[datos["ind5"]]
        df5 = df5.reset_index(drop=True)
        
        df = pd.concat([df3, df5], axis=1)
        
        lista_df.append(df)
        lista_doc = np.append(lista_doc, doc)

    for ID in D["1-M"]:
        grupos = D["1-M"][ID]
        for datos in grupos:
            df3 = FBL3N.iloc[datos["ind3"]]
            doc = df3["Nº documento BANCO"].to_numpy()
            df3 = pd.DataFrame(np.repeat(df3.values, datos["ind5"].size, axis=0))
            df3 = df3.reset_index(drop=True)
            df3.columns = FBL3N.columns
            
            df5 = FBL5N.iloc[datos["ind5"]]
            df5 = df5.reset_index(drop=True)
            
            df = pd.concat([df3, df5], axis=1)
            
            lista_df.append(df)
            lista_doc = np.append(lista_doc, doc)

    ind = np.argsort(lista_doc)
    correlativo = 0
    for indice in ind:
        correlativo += 1
        lista_df[indice]["Correlativo"] = correlativo

    if len(lista_df) == 0:
        return pd.DataFrame(columns=np.concatenate([FBL3N.columns, FBL5N.columns]))

    lista_df.sort(key=lambda df: df["Correlativo"][0])
    
    DF = pd.concat(lista_df, ignore_index=True)
    return DF
    

def calzar_por_id(FBL3N, FBL5N):
    D = extraer_datos(FBL3N, FBL5N)
    print("Realizando calces...")
    match_1_1(D)
    match_1_T(D)
    match_1_V(D)
    match_1_M(D)
    df = organizar_en_tabla(D, FBL3N, FBL5N)
    
    return df

def calzar_por_factura(FBL3N, FBL5N):
    print("Realizando calce...")
    FBL3N["Nº factura"] = FBL3N["Nº factura"].astype(str)
    FBL5N["Referencia"] = FBL5N["Referencia"].astype(str)
    df = pd.merge(
        FBL3N.add_suffix(" BANCO"), FBL5N.add_suffix(" PA"),
        left_on="Nº factura BANCO", right_on="Referencia PA"
    )
    df["Correlativo"] = np.arange(1, len(df) + 1)

    return df
