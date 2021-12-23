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


def indices_comb(largo, n, MAX=None):
    """
    Retorna un ndarray de índices para ordenar un arreglo de largo "largo"
    en combinaciones de n elementos.
    """
    indices = np.ones((n, largo-n+1), dtype=np.int16)
    indices[0] = np.arange(largo-n+1)
    for j in range(1, n):
        reps = (largo-n+j) - indices[j-1]
        ind = np.add.accumulate(reps)
        if type(MAX) == int and ind[-1] > MAX:
            sup = np.nonzero(ind >= MAX)[0][0]
            reps2 = reps.copy()
            
            if sup - 1 >= 0:
                reps[sup] = MAX - ind[sup-1]
            else:
                reps[sup] = MAX
            
            indices = np.repeat(indices[:, :sup+1], reps[:sup+1], axis=1)
            indices[j, ind[:sup]] = 1-reps2[1:sup+1]
            indices[j, 0] = j
            indices[j] = np.add.accumulate(indices[j])
            
        else:
            indices = np.repeat(indices, reps, axis=1)
            indices[j, ind[:-1]] = 1-reps[1:]
            indices[j, 0] = j
            indices[j] = np.add.accumulate(indices[j])
    return indices
