import pandas as pd
import numpy as np
import itertools as it
from funciones_aux_1_M import *

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


def separar_partidas_solas(DA, DB):
    idsA = DA["ORD"]["ID"]
    idsB = DB["ORD"]["ID"]
    
    filtroA = np.isin(idsA, idsB)
    iA_ord = np.nonzero(filtroA)
    iA_sol = np.nonzero(~filtroA)
    
    for clave in DA["ORD"]:
        DA["SOL"][clave] = np.concatenate((
            DA["SOL"][clave],
            DA["ORD"][clave][iA_sol]
        ))
        DA["ORD"][clave] = DA["ORD"][clave][iA_ord]
    

def extraer_datos(FBL3N, FBL5N):
    # Obtener ndarrays (arreglos de NumPy) importantes
    # a partir de FBL3N y FBL5N
    ind3 = np.arange(len(FBL3N.index))
    ids3 = FBL3N["Cliente"].to_numpy()
    mon3 = -FBL3N["Importe en moneda local"].to_numpy()

    ind5 = np.arange(len(FBL5N.index))
    ids5 = FBL5N["Cuenta"].to_numpy()
    mon5 = FBL5N["Importe en ML"].to_numpy()
    dem5 = FBL5N["Demora"].to_numpy()
    
    D = {"ORD": {}, "1-1": {}, "1-T": {}, "1-V": {}, "1-M": {}, "SOL": {3: {}, 5: {}}}
    
    # Ordenar datos de FBL3N en base a las IDs
    i3 = np.argsort(ids3)
    ind3 = ind3[i3]
    ids3 = ids3[i3]
    mon3 = mon3[i3]
    lim3 = limites(ids3)

    # Ordenar datos de FBL5N en base a las IDs y luego en base a las demoras
    i5 = np.lexsort((-dem5, ids5))
    ind5 = ind5[i5]
    ids5 = ids5[i5]
    mon5 = mon5[i5]
    dem5 = dem5[i5]
    lim5 = limites(ids5)
    
    D["ORD"] = {
        ID: { 
            "ind3": ind3[ lim3[i] : lim3[i+1] ],
            "mon3": mon3[ lim3[i] : lim3[i+1] ],
            "ind5": ind5[ lim5[i] : lim5[i+1] ],
            "mon5": mon5[ lim5[i] : lim5[i+1] ],
            "dem5": dem5[ lim5[i] : lim5[i+1] ],
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
    def choose(n, k):
        """
        Retorna el número combinatorio "n sobre k".
        """
        resultado = 1
        for i in range(1, k+1):
            resultado *= (n-i+1)
            resultado //= i
        return resultado
    
    
    def sumasn(arr, n):
        """
        Retorna un arreglo con todas las sumas de las combinaciones
        de n elementos del arreglo arr.
        """
        largo = arr.size
        if n > largo:
            return np.array([], dtype=int)
        if n == 1:
            return arr
        
        resultado = np.empty(choose(largo, n), dtype=int)
            
        rinf = 0
        rsup = 0
        for K in it.combinations(np.arange(1, largo), n-1):
            rinf = rsup
            rsup += largo - K[-1]
            resultado[rinf:rsup] = arr[:largo-K[-1]]
            for k in K:
                resultado[rinf:rsup] += arr[k : (largo-K[-1]) + k]
                    
        return resultado
    
    
    def calcular_n_max(largo):
        """
        Calcula la cantidad máxima de elementos por combinación (n_max)
        a realizar en un arreglo de largo "largo".

        Si hay un arreglo con 800 elementos, no es posible realizar
        todas las 2^800 combinaciones de esos elementos. Idealmente, se
        deberían realizar menos de 100.000 combinaciones por arreglo para
        evitar que el programa se demore demasiado tiempo en ejecutar.

        Para un arreglo con 800 elementos, por ejemplo, no se deberían
        realizar combinaciones de más de 2 elementos. En ese caso, el
        valor retornado por esta función sería n_max = 2.

        Pero para un arreglo con 15 elementos, es perfectamente viable
        hacer las 2^15 combinaciones, así que n_max = 15.
        """
        
        if largo <= 2:
            return largo

        n_max = 2
        while n_max < largo:
            if choose(largo, n_max) > 100000:
                return n_max - 1
            n_max += 1

        return n_max

    
    def obtener_indices(i, largo, n):
        """
        Dado un arreglo de largo "largo", si se realizan todas las combinaciones
        posibles de n elementos en tal arreglo, se pueden colocar en un nuevo
        arreglo de largo (largo)! / [(largo - n)! * n!].

        Dado un índice i de este nuevo arreglo, esta función retorna la
        combinación de índices en el arreglo original que entregaría la
        combinación de elementos que encuentras en la posición i del nuevo
        arreglo.

        Por ejemplo, para un arreglo de largo 10, donde se hacen combinaciones de
        2 elementos, se crearía un arreglo de largo 45. La combinación de
        los elementos en las posiciones 2 y 5, por dar un ejemplo, se encontraría
        en la posición 19 en el nuevo arreglo, de acuerdo a la manera en que
        funciona la función sumasn. Así, si a la función obtener_indices se le
        entregan los argumentos i = 19, largo = 10 y n = 2, debe retornar el
        arreglo [2, 5].

        Esta función existe para evitar crear un arreglo con todas las posibles
        combinaciones de índices. Así, se crearía solamente un arreglo con todas
        las posibles sumas de combinaciones de elementos del arreglo, haciendo
        que el programa sea más eficiente en tiempo.
        """
        I = 0
        for K in it.combinations(np.arange(1, largo), n-1):
            I += largo - K[-1]
            if I > i:
                break

        indices = np.append([0], K)
        indices += (largo - K[-1]) - (I - i)
        return indices
    

    """'''''''''"""
        
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
        ni5_flat = np.ones_like(datos["mon5"], dtype=bool)

        largo = range5.size
        
        n = 2
        n_max = calcular_n_max(largo)
        while n <= n_max:
            # Obtener arreglo de todas las combinaciones de n elementos
            # de datos["mon5"] que no estén siendo usados actualmente
            suma_mon5 = sumasn(datos["mon5"][ni5_flat], n)

            # Obtener índices en el arreglo de sumas donde sus elementos
            # estén contenidos entre los elementos no seleccionados de
            # datos["mon3"]
            si5 = np.nonzero(np.isin(suma_mon5, datos["mon3"][ni3]))[0]
            if si5.size > 0:
                print(ID)
                print(datos["mon3"][ni3])
                print(suma_mon5[si5])
                print("-"*20)

            # Filtrar en i3 y si5
            # Buscar entre todos los índices en suma_mon5 marcados
            for i in si5:
                # Obtener la combinación de índices en el arreglo original,
                # datos["mon5"], que produciría la suma encontrada en
                # el índice seleccionado actualmente, i
                indices5 = obtener_indices(i, largo, n)
                
                # Si hay algún índice ocupado, descartar esta combinación
                if np.isin(indices5, np.nonzero(ni5_flat), invert=True).any():
                    pass
                
                else:
                    # Buscar todos los datos restantes en datos["mon3"] cuyo
                    # monto coincida con el valor seleccionado de suma_mon5.
                    # Es posible que este dato haya sido marcado en una
                    # iteración anterior, por eso se debe verificar
                    j3 = (datos["mon3"][ni3] == suma_mon5[i])
                    if range3[ni3][j3].size > 0:
                        # Obtener el primer índice de entre los seleccionados
                        indice3 = range3[ni3][j3][0]
                        
                        i3.append(indice3)
                        i5.append(indices5)
                        
                        ni3[indice3] = False
                        ni5_flat[indices5] = False

                        #largo = range5[ni5_flat].size
                        #n_max = calcular_n_max(largo)

                        break

            # Si todos los índices están ocupados (es decir, si todos los índices
            # en ni3 están marcados como False), terminar acá
            if not ni3.any():
                break

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


def match_1_M_2(D):
    """
    NOTA IMPORTANTE
    Esta función requiere varias funciones auxiliares contenidas en
    funciones_aux_1_M.py

    Funciones usadas directamente aquí:
        comb
        obtener_indices
        
    Funciones requeridas por las anteriores:
        choose
        suma
    """
    
    for ID in D["ORD"].copy():
        datos = D["ORD"][ID]

        i3 = []
        i5 = []

        range3 = np.arange(datos["ind3"].size, dtype=np.int32)
        range5 = np.arange(datos["ind5"].size, dtype=np.int32)

        largo = range5.size
        
        suma_mon5 = comb(datos["mon5"], largo)

        # i3 y ci5 todavía no están del todo "listos".
        # Se debe filtrar después de esto
        i3 = np.nonzero(np.isin(datos["mon3"], suma_mon5))[0]
        ci5 = np.nonzero(np.isin(suma_mon5, datos["mon3"]))[0]

        # Filtrar en i3 y ci5
        usados3 = []
        usados5 = []
        usados5_flat = []
        # Buscar entre todos los índices en suma_mon5 marcados
        for i in ci5.copy():
            indices = obtener_indices(i, largo)
            # Si hay algún índice ocupado, descartar esta combinación
            if np.isin(indices, usados5_flat).any():
                pass
            else:
                j3 = (datos["mon3"] == suma_mon5[i]) & np.isin(range3, usados3, invert=True)
                if range3[j3].size > 0:
                    usados3.append(range3[j3][0])
                    usados5.append(indices)
                    for indice in indices:
                        usados5_flat.append(indice)

        i3 = usados3
        i5 = usados5

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
    cols3 = [
        "Nº documento",
        "Clase de documento",
        "Fecha de documento",
        "Importe en moneda local",
        "Moneda local",
        "Texto",
        "Cliente",
        "Nº ident.fis.1",
        "Nombre 1",
    ]
    
    cols5 = [
        "Soc.",
        "Asignación",
        "Ejerc./mes",
        "Nº doc.",
        "Referencia",
        "Cla",
        "Importe en ML",
        "Mon.",
    ]

    cols_ord = [
        "Grupo",
        "Soc.",
        "Nº documento",
        "Clase de documento",
        "Fecha de documento",
        "Importe en moneda local",
        "Moneda local",
        "Texto",
        "Cliente",
        "Nº ident.fis.1",
        "Nombre 1",
        "Asignación",
        "Ejerc./mes",
        "Nº doc.",
        "Referencia",
        "Cla",
        "Importe en ML",
        "Mon.",
    ]

    lista_doc = np.array([], dtype=str)
    lista_df = []
    
    for ID in D["1-1"]:
        datos = D["1-1"][ID]

        for indice in datos["ind3"]:
            df3 = FBL3N[cols3].iloc[[indice]]
            df3 = df3.reset_index(drop=True)
            df3.columns = cols3
            doc = df3["Nº documento"].to_numpy()
            
            df5 = FBL5N[cols5].iloc[datos["ind5"]]
            df5 = df5.reset_index(drop=True)
            df5.columns = cols5
            
            df = pd.concat([df3, df5], axis=1)

            lista_df.append(df)
            lista_doc = np.append(lista_doc, [doc])

    for ID in D["1-T"]:
        datos = D["1-T"][ID]
        
        df3 = FBL3N[cols3].iloc[datos["ind3"]]
        doc = df3["Nº documento"].to_numpy()
        df3 = pd.DataFrame(np.repeat(df3.values, datos["ind5"].size, axis=0))
        df3 = df3.reset_index(drop=True)
        df3.columns = cols3
        
        df5 = FBL5N[cols5].iloc[datos["ind5"]]
        df5 = df5.reset_index(drop=True)
        df5.columns = cols5
        
        df = pd.concat([df3, df5], axis=1)
        
        lista_df.append(df)
        lista_doc = np.append(lista_doc, doc)

    for ID in D["1-V"]:
        datos = D["1-V"][ID]
        
        df3 = FBL3N[cols3].iloc[datos["ind3"]]
        doc = df3["Nº documento"].to_numpy()
        df3 = pd.DataFrame(np.repeat(df3.values, datos["ind5"].size, axis=0))
        df3 = df3.reset_index(drop=True)
        df3.columns = cols3
        
        df5 = FBL5N[cols5].iloc[datos["ind5"]]
        df5 = df5.reset_index(drop=True)
        df5.columns = cols5
        
        df = pd.concat([df3, df5], axis=1)
        
        lista_df.append(df)
        lista_doc = np.append(lista_doc, doc)

    for ID in D["1-M"]:
        grupos = D["1-M"][ID]
        for datos in grupos:
            df3 = FBL3N[cols3].iloc[datos["ind3"]]
            doc = df3["Nº documento"].to_numpy()
            df3 = pd.DataFrame(np.repeat(df3.values, datos["ind5"].size, axis=0))
            df3 = df3.reset_index(drop=True)
            df3.columns = cols3
            
            df5 = FBL5N[cols5].iloc[datos["ind5"]]
            df5 = df5.reset_index(drop=True)
            df5.columns = cols5
            
            df = pd.concat([df3, df5], axis=1)
            
            lista_df.append(df)
            lista_doc = np.append(lista_doc, doc)

    ind = np.argsort(lista_doc)
    
    lista_df = np.array(lista_df, dtype="object")
    lista_df = lista_df[ind]
    for i in range(len(lista_df)):
        lista_df[i]["Grupo"] = i+1
    
    DF = pd.concat(lista_df, ignore_index=True)
    return DF[cols_ord]
    

def calzar(FBL3N, FBL5N):
    D = extraer_datos(FBL3N, FBL5N)
    match_1_1(D)
    match_1_T(D)
    match_1_V(D)
    match_1_M_2(D)
    DF = organizar_en_tabla(D, FBL3N, FBL5N)
    
    return DF, D
