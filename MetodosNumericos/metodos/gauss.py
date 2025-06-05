import numpy as np 

def eliminacion_gaussiana(A, b):
    n = len(b)  # Determina el número de ecuaciones (filas) en el sistema
    
    # Crea la matriz aumentada [A|b] convirtiendo a float para evitar errores en divisiones
    aug = np.hstack([A, b.reshape(-1, 1)]).astype(float)
    steps = [aug.copy()]  # Almacena el estado inicial de la matriz aumentada
    
    # Bucle principal: recorre cada columna para la eliminación
    for i in range(n):
        # PIVOTEO PARCIAL
        # Encuentra la fila con el máximo valor absoluto desde la fila actual hacia abajo
        max_row = np.argmax(np.abs(aug[i:, i])) + i
        
        # Verifica si el pivote es cero (matriz singular)
        if not np.isclose(aug[max_row, i], 0):
            # Intercambia filas para colocar el pivote máximo en posición actual
            aug[[i, max_row]] = aug[[max_row, i]]
            steps.append(aug.copy())  # Guarda el estado post-pivoteo
        else:
            raise ValueError("La matriz es singular. No hay solución única.")
        
        # ELIMINACIÓN HACIA ADELANTE
        # Recorre filas inferiores para crear ceros debajo del pivote
        for j in range(i+1, n):
            # Calcula el factor de multiplicación para anular el elemento
            factor = aug[j, i] / aug[i, i]
            # Resta la fila actual multiplicada por el factor a la fila objetivo
            aug[j, i:] -= factor * aug[i, i:]
        
        steps.append(aug.copy())  # Guarda el estado después de procesar la columna
    
    # SUSTITUCIÓN HACIA ATRAS
    x = np.zeros(n)  # Vector para almacenar las soluciones
    
    # Recorre las filas de abajo hacia arriba
    for i in range(n-1, -1, -1):
        # Calcula la solución para la variable actual:
        # 1. Resta la contribución de variables ya resueltas (x[i+1:])
        # 2. Divide por el coeficiente diagonal
        x[i] = (aug[i, -1] - aug[i, i+1:n].dot(x[i+1:])) / aug[i, i]
    
    return x, steps  