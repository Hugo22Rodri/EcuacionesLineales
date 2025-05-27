import numpy as np                         # para manejar operaciones matriciales

def eliminacion_gaussiana(A, b):
    n = len(b)                             # Determinamos el número de ecuaciones (filas)
    aug = np.hstack([A, b.reshape(-1,1)])  # Construimos la matriz aumentada concatenando A y b como columna
    steps = [aug.copy()]                   # Guardamos el estado inicial de la matriz aumentada
    
    for i in range(n):
        # Pivoteo parcial: buscamos la fila con el mayor valor absoluto en la columna actual
        max_row = np.argmax(np.abs(aug[i:, i])) + i
        aug[[i, max_row]] = aug[[max_row, i]]  # Intercambiamos la fila actual con la fila del pivote
        #steps.append(aug.copy())              # Podemos guardar este paso si queremos ver la transformación
        
        # Eliminación hacia adelante: 
        # hacemos ceros debajo del pivote en la columna actual
        for j in range(i+1, n):
            factor = aug[j, i] / aug[i, i]     # Calculamos el factor de eliminación
            aug[j, i:] -= factor * aug[i, i:]  # Restamos la fila escalada para hacer ceros
            steps.append(aug.copy())           # Guardamos el estado de la matriz tras cada eliminación
    
    # Sustitución hacia atrás: resolvemos el sistema triangular superior
    x = np.zeros(n)                            # Inicializamos el vector de soluciones con ceros
    for i in range(n-1, -1, -1):               # Iteramos desde la última ecuación hacia la primera
        x[i] = (aug[i, -1] - aug[i, i+1:n].dot(x[i+1:])) / aug[i, i]  # Despejamos la variable
    return x, steps                            # Retornamos la solución y la lista de pasos intermedios
