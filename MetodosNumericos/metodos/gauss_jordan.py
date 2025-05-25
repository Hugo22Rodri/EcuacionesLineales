import numpy as np

def gauss_jordan(A, b):
    n = len(b)
    aug = np.hstack([A, b.reshape(-1,1)])
    steps = [aug.copy()]
    
    for i in range(n):
        # Pivoteo
        max_row = np.argmax(np.abs(aug[i:, i])) + i
        aug[[i, max_row]] = aug[[max_row, i]]
        #steps.append(aug.copy())
        
        # Escalonar
        pivot = aug[i,i]
        aug[i] = aug[i] / pivot
        steps.append(aug.copy())
        
        for j in range(n):
            if j != i:
                factor = aug[j,i]
                aug[j] -= factor * aug[i]
                steps.append(aug.copy())
    
    return aug[:,-1], steps