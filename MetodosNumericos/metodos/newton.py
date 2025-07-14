import numpy as np
import sympy as sp
from django.core.exceptions import ValidationError

def calcular_diferencias_divididas(x, y):
    """Calcula la tabla de diferencias divididas con validación"""
    n = len(x)
    tabla = np.zeros((n, n))
    tabla[:, 0] = y
    
    for j in range(1, n):
        for i in range(n - j):
            denominador = x[i+j] - x[i]
            if abs(denominador) < 1e-10:
                raise ValidationError("Valores de x demasiado cercanos")
            tabla[i][j] = (tabla[i+1][j-1] - tabla[i][j-1]) / denominador
    
    return tabla

def interpolate_newton(x_values, y_values, var='x'):
    """
    Versión mejorada con manejo de errores
    :return: (polinomio_simplificado, función_numpy)
    :raises: ValidationError si hay problemas
    """
    try:
        # Validación
        if len(x_values) != len(y_values):
            raise ValidationError("x e y deben tener igual longitud")
        if len(x_values) < 2:
            raise ValidationError("Mínimo 2 puntos requeridos")
        
        x = sp.symbols(var)
        tabla = calcular_diferencias_divididas(x_values, y_values)
        
        polinomio = termino = tabla[0][0]
        for i in range(1, len(x_values)):
            termino *= (x - x_values[i-1])
            polinomio += tabla[0][i] * termino
        
        return sp.simplify(polinomio), sp.lambdify(x, polinomio, 'numpy')
    
    except ZeroDivisionError:
        raise ValidationError("División por cero - valores de x repetidos")
    except Exception as e:
        raise ValidationError(f"Error en Newton: {str(e)}")