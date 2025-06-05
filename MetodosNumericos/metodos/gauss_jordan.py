import numpy as np

def gauss_jordan(A, b):
    n = len(b)                             # Determinamos el número de ecuaciones (filas)
    aug = np.hstack([A, b.reshape(-1,1)])  # Construimos la matriz aumentada concatenando A y b como columna
    steps = [aug.copy()]                   # Guardamos el estado inicial de la matriz aumentada
    
    for i in range(n):
        # Pivoteo: se busca la fila con el mayor valor absoluto en la columna actual para mejorar la estabilidad numerica
        max_row = np.argmax(np.abs(aug[i:, i])) + i  # Determina la fila con el mayor valor en la columna i
        aug[[i, max_row]] = aug[[max_row, i]]        # Intercambia la fila actual con la fila del pivote
        steps.append(aug.copy())                   
        
        # Escalonar: normalizamos la fila del pivote dividiendola por el valor del pivote
        pivot = aug[i, i]               # Obtenemos el pivote de la fila actual
        aug[i] = aug[i] / pivot         # Normalizamos la fila dividiendo todos sus elementos por el pivote
        steps.append(aug.copy())        # Guardamos el estado de la matriz tras la normalización
        
        # Eliminación: hacemos ceros en todas las demás filas en la columna i
        for j in range(n):
            if j != i:                      # Aseguramos que no afectamos la fila del pivote
                factor = aug[j, i]          # Factor de eliminación basado en el valor de la columna i
                aug[j] -= factor * aug[i]   # se resta la fila escalada para hacer ceros
                steps.append(aug.copy())    #se guarda el estado de la matriz despuée de cada eliminacion
     
    return aug[:, -1], steps                #Retornamos el vector de soluciones y la lista de matrices en cada paso