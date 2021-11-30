import pandas as pd
import numpy as np
import itertools as it

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
    ids3 = FBL3N["Cliente"].to_numpy()
    doc3 = FBL3N["Nº documento"].to_numpy()
    mon3 = -FBL3N["Importe en moneda local"].to_numpy()

    ids5 = FBL5N["Cuenta"].to_numpy()
    doc5 = FBL5N["Nｺ doc."].to_numpy()
    mon5 = FBL5N["Importe en ML"].to_numpy()
    dem5 = FBL5N["Demora"].to_numpy()
    
    D = {"ORD": {}, "1-1": {}, "1-T": {}, "1-V": {}, "1-M": {}, "SOL": {3: {}, 5: {}}}
    
    # Ordenar datos de FBL3N en base a las IDs
    i3 = np.argsort(ids3)
    ids3 = ids3[i3]
    doc3 = doc3[i3]
    mon3 = mon3[i3]
    lim3 = limites(ids3)

    # Ordenar datos de FBL5N en base a las IDs y luego en base a las demoras
    i5 = np.lexsort((-dem5, ids5))
    ids5 = ids5[i5]
    doc5 = doc5[i5]
    mon5 = mon5[i5]
    dem5 = dem5[i5]
    lim5 = limites(ids5)
    
    D["ORD"] = {
        ID: { 
            "doc3": doc3[ lim3[i] : lim3[i+1] ],
            "mon3": mon3[ lim3[i] : lim3[i+1] ],
            "doc5": doc5[ lim5[i] : lim5[i+1] ],
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
                "doc3": datos["doc3"][i3],
                "mon3": datos["mon3"][i3],
                "doc5": datos["doc5"][i5],
                "mon5": datos["mon5"][i5],
                "dem5": datos["dem5"][i5],
            }

            # Obtener complementos de i3 e i5
            ni3 = np.ones_like(datos["doc3"], dtype=bool)
            ni3[i3] = False
            ni5 = np.ones_like(datos["doc5"], dtype=bool)
            ni5[i5] = False

            # Si todavía sobran datos, guardar los restantes en D["ORD"],
            # sobreescribiendo lo que había ahí
            if i3.size < datos["doc3"].size and i5.size < datos["doc5"].size:
                D["ORD"][ID] = {
                    "doc3": datos["doc3"][ni3],
                    "mon3": datos["mon3"][ni3],
                    "doc5": datos["doc5"][ni5],
                    "mon5": datos["mon5"][ni5],
                    "dem5": datos["dem5"][ni5],
                }

            # En cambio, si se acabaron todas las partidas en FBL3N o FBL5N,
            # eliminar D["ORD"][ID]
            else:
                # Si hay partidas solas en FBL3N, guardarlas acá
                if i3.size < datos["doc3"].size:
                    if ID in D["SOL"][3]:     
                        D["SOL"][3][ID] = {
                            "doc3": np.concatenate(D["SOL"][3][ID]["doc3"], datos["doc3"][ni3]),
                            "mon3": np.concatenate(D["SOL"][3][ID]["mon3"], datos["mon3"][ni3]),
                        }
                    else:
                        D["SOL"][3][ID] = {
                            "doc3": datos["doc3"][ni3],
                            "mon3": datos["mon3"][ni3],
                        }

                # Si hay partidas solas en FBL5N, guardarlas acá
                elif i5.size < datos["doc5"].size:
                    if ID in D["SOL"][5]:     
                        D["SOL"][5][ID] = {
                            "doc5": np.concatenate(D["SOL"][5][ID]["doc5"], datos["doc5"][ni5]),
                            "mon5": np.concatenate(D["SOL"][5][ID]["mon5"], datos["mon5"][ni5]),
                            "dem5": np.concatenate(D["SOL"][5][ID]["dem5"], datos["dem5"][ni5]),
                            
                        }
                    else:
                        D["SOL"][5][ID] = {
                            "doc5": datos["doc5"][ni5],
                            "mon5": datos["mon5"][ni5],
                            "dem5": datos["dem5"][ni5],
                        }

                
                    
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
                "doc3": datos["doc3"][i3],
                "mon3": datos["mon3"][i3],
                "doc5": datos["doc5"],
                "mon5": datos["mon5"],
                "dem5": datos["dem5"],
            }

            # Obtener complemento de i3
            ni3 = np.ones_like(datos["doc3"], dtype=bool)
            ni3[i3] = False

            # Si sobran datos en FBL3N, guardarlos en D["SOL"]
            if i3.size < datos["doc3"].size:
                if ID in D["SOL"][3]:     
                    D["SOL"][3][ID] = {
                        "doc3": np.concatenate(D["SOL"][3][ID]["doc3"], datos["doc3"][ni3]),
                        "mon3": np.concatenate(D["SOL"][3][ID]["mon3"], datos["mon3"][ni3]),
                    }
                else:
                    D["SOL"][3][ID] = {
                        "doc3": datos["doc3"][ni3],
                        "mon3": datos["mon3"][ni3],
                    }
                
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
                "doc3": datos["doc3"][i3],
                "mon3": datos["mon3"][i3],
                "doc5": datos["doc5"][v],
                "mon5": datos["mon5"][v],
                "dem5": datos["dem5"][v],
            }

            # Obtener complemento de i3
            ni3 = np.ones_like(datos["doc3"], dtype=bool)
            ni3[i3] = False

            # Si todavía sobran datos, guardar los restantes en D["ORD"],
            # sobreescribiendo lo que había ahí
            if i3.size < datos["doc3"].size and datos["doc5"][~v].size > 0:
                D["ORD"][ID] = {
                    "doc3": datos["doc3"][ni3],
                    "mon3": datos["mon3"][ni3],
                    "doc5": datos["doc5"][~v],
                    "mon5": datos["mon5"][~v],
                    "dem5": datos["dem5"][~v],
                }

            # En cambio, si se acabaron todas las partidas en FBL3N o FBL5N,
            # eliminar D["ORD"][ID]
            else:
                # Si hay partidas solas en FBL3N, guardarlas acá
                if i3.size < datos["doc3"].size:
                    if ID in D["SOL"][3]:     
                        D["SOL"][3][ID] = {
                            "doc3": np.concatenate(D["SOL"][3][ID]["doc3"], datos["doc3"][ni3]),
                            "mon3": np.concatenate(D["SOL"][3][ID]["mon3"], datos["mon3"][ni3]),
                        }
                    else:
                        D["SOL"][3][ID] = {
                            "doc3": datos["doc3"][ni3],
                            "mon3": datos["mon3"][ni3],
                        }

                # Si hay partidas solas en FBL5N, guardarlas acá
                elif datos["doc5"][~v].size > 0:
                    if ID in D["SOL"][5]:     
                        D["SOL"][5][ID] = {
                            "doc5": np.concatenate(D["SOL"][5][ID]["doc5"], datos["doc5"][~v]),
                            "mon5": np.concatenate(D["SOL"][5][ID]["mon5"], datos["mon5"][~v]),
                            "dem5": np.concatenate(D["SOL"][5][ID]["dem5"], datos["dem5"][~v]),
                            
                        }
                    else:
                        D["SOL"][5][ID] = {
                            "doc5": datos["doc5"][~v],
                            "mon5": datos["mon5"][~v],
                            "dem5": datos["dem5"][~v],
                        }

                
                    
                D["ORD"].pop(ID)

"""
def match_1_M(D):
    def sumas(arr):
        sumas_arr = [it.combinations(arr, largo) for largo in range(2, len(arr) + 1)]
        sumas_arr = it.chain.from_iterable(sumas_arr)
        sumas_arr = it.islice(sumas_arr, 1000000)
        sumas_arr = np.array(list(sumas_arr), dtype="object")
        sumas_arr = sumas_arr.sum(axis=-1)
        return sumas_arr
        	
        
        if len(arr) > 15 or len(arr) == 1:
            return []
        	
    	sumas_arr = [np.array(list(it.combinations(arr, largo))).sum(axis=-1)
        for largo in range(2, len(arr) + 1)]
            return np.concatenate(sumas_arr)
	

    def combinaciones(arr):
        combs_arr = [it.combinations(arr, largo) for largo in range(2, len(arr) + 1)]
        combs_arr = it.chain.from_iterable(combs_arr)
        combs_arr = it.islice(combs_arr, 16)
        combs_arr = np.array(list(combs_arr), dtype="object")
        return combs_arr
        	
        
        if len(arr) > 15 or len(arr) == 1:
            return []
        
        combs_arr = [list(it.combinations(arr, largo))
        for largo in range(2, len(arr) + 1)]
            print(combs_arr)
            return np.concatenate(combs_arr)
        
        
    ids3 = D3["ORD"]["ID"]
    mon3 = D3["ORD"]["Monto"]
    lim3 = limites(ids3)

    ids5 = D5["ORD"]["ID"]
    mon5 = D5["ORD"]["Monto"]
    lim5 = limites(ids5)
    
    n_ids = np.unique(ids3).size
    
    # Calcular sumas de cada combinación posible en cada grupo de montos en FBL5N
    sum5 = [sumas(mon5[ lim5[i] : lim5[i+1] ]) for i in range(n_ids)]
    lms5 = [0] + [len(sum5[i]) for i in range(len(sum5))]
    sum5 = np.concatenate(sum5)
    
    ind5 = np.arange(ids5.size)
    cmb5 = [combinaciones(ind5[ lim5[i] : lim5[i+1] ]) for i in range(n_ids)]
    print(cmb5)
    cmb5 = np.concatenate(cmb5)
    
    ##########
    
    # i3 es un arreglo booleano.
    # Para cada elemento en D[3]["ORD"]["Monto"], es igual a True
    # si es igual a la suma de todos los montos respectivos en sum5
    i3 = [
        np.isin(-mon3[ lim3[i] : lim3[i+1] ], sum5[ lms5[i] : lms5[i+1] ])
        for i in range(n_ids)
    ]
    i3 = np.concatenate(i3)
    print(i3)
    
    # Filtrar datos en D[3]
    # Rellenar D[3]["1-1"] con los calces 1-1 encontrados
    # Reemplazar D[3]["ORD"] con el resto de los datos
    for clave in ("ID", "Documento", "Monto"):
        D3["1-M"][clave] = D3["ORD"][clave][np.nonzero(i3)]
        D3["ORD"][clave] = D3["ORD"][clave][np.nonzero(~i3)]
    
    ##########
    
    # i5 es un arreglo booleano.
    # Para cada elemento en D[5]["ORD"]["Monto"], es igual a True
    # si se encuentra en el grupo respectivo en D[3]["ORD"]["Monto"]
    i5 = [
        np.isin(sum5[ lms5[i] : lms5[i+1] ], -mon3[ lim3[i] : lim3[i+1] ])
        for i in range(n_ids)
    ]
    i5 = np.concatenate(i5)

    resultados_suma = sum5[i5]
    resultados_comb = cmb5[i5]

    print(pd.DataFrame.from_dict({"IDs": resultados_comb, "Sumas": resultados_suma}))
        
    # Filtrar datos en D[5]
    # Rellenar D[5]["1-1"] con los calces 1-1 encontrados
    # Reemplazar D[5]["ORD"] con el resto de los datos
    for clave in ("ID", "Documento", "Monto", "Demora"):
        D5["1-M"][clave] = D5["ORD"][clave][np.nonzero(i5)]
        D5["ORD"][clave] = D5["ORD"][clave][np.nonzero(~i5)]
    
    ##########
    
    # Separar aquellas partidas que ya no pueden hacer match debido a que
    # ya no hay partidas con el mismo ID en la otra tabla
    separar_partidas_solas(D3, D5)
    separar_partidas_solas(D3, D5)
"""

def calzar(FBL3N, FBL5N):
    D = extraer_datos(FBL3N, FBL5N)
    print(len(D["ORD"]))
    match_1_1(D)
    print(len(D["ORD"]))
    match_1_T(D)
    print(len(D["ORD"]))
    match_1_V(D)
    print(len(D["ORD"]))
    #match_1_M(D)
    print(len(D["ORD"]))
    
    return D
