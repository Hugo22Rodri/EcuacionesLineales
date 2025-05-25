import numpy as np

def eliminacion_gaussiana(A, b):
    n = len(b)
    aug = np.hstack([A, b.reshape(-1,1)])
    steps = [aug.copy()]
    
    for i in range(n):
        # Pivoteo parcial
        max_row = np.argmax(np.abs(aug[i:, i])) + i
        aug[[i, max_row]] = aug[[max_row, i]]
        #steps.append(aug.copy())
        
        # Eliminación hacia adelante
        for j in range(i+1, n):
            factor = aug[j,i] / aug[i,i]
            aug[j,i:] -= factor * aug[i,i:]
            steps.append(aug.copy())
    
    # Sustitución hacia atrás
    x = np.zeros(n)
    for i in range(n-1, -1, -1):
        x[i] = (aug[i,-1] - aug[i,i+1:n].dot(x[i+1:])) / aug[i,i]
    return x, steps