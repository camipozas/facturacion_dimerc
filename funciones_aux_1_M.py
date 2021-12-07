import itertools as it
import numpy as np

def choose(n, k):
    """
    Retorna el número combinatorio "n sobre k".
    """
    resultado = 1
    for i in range(1, k+1):
        resultado *= (n-i+1)
        resultado //= i
    return resultado

def suma(arr, largo):
    for tupla in it.combinations(arr, largo):
        yield sum(tupla)
    
def comb(arr, N):
    comb_arr = [suma(arr, largo) for largo in range(2, N+1)]
    comb_arr = it.chain.from_iterable(comb_arr)
    comb_arr = it.islice(comb_arr, 100000)
    return np.fromiter(comb_arr, np.int32)

def obtener_indices(i, largo):
    """
    Dado un arreglo de largo "largo", si se realizan todas las combinaciones
    posibles de n elementos en tal arreglo, se pueden colocar en un nuevo
    arreglo de largo choose(largo, n).

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
        
    # 1. ¿Combinaciones de 2? ¿De 3? Encontrar n
    n = 2
    while True:
        termino = choose(largo, n)
        if I + termino <= i:
            I += termino
            n += 1
            if I == i:
                return np.arange(n)
        else:
            break

    # 2. Ahora que se conoce n, encontrar la combinación exacta de índices
    indices = np.arange(n)
    for pos in range(n):
        while True:
            # termino: igual al siguiente número combinatoriio: "cantidad
            # de números del 0 al 9 restantes" sobre "cantidad de posiciones
            # restantes".

            # "Cantidad de números del 0 al 9 restantes": obtenido a partir
            # del último número fijado (indices[pos]). Es decir, si el
            # último número fijado es 1, solo quedan los números del 2 al 9.
            # Entonces, esta cantidad es largo - indices[pos] - 1

            # "Cantidad de posiciones restantes": n - pos - 1
                
            termino = choose(largo - indices[pos] - 1, n - pos - 1)
            if I + termino <= i:
                I += termino
                indices[pos:] += 1
                if I == i:
                    return indices
            else:
                break

    return indices
