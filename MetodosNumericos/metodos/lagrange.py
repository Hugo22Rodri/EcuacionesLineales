import numpy as np
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr
from django.core.exceptions import ValidationError

def validate_input(x_values, y_values):
    """Valida los puntos de entrada para la interpolación"""
    if len(x_values) != len(y_values):
        raise ValidationError("La cantidad de valores x e y no coincide")
    
    if len(x_values) < 2:
        raise ValidationError("Se requieren al menos 2 puntos para interpolación")
    
    if len(x_values) != len(set(x_values)):
        raise ValidationError("Los valores de x deben ser distintos")

def interpolate_lagrange(x_values, y_values, var='x'):
    """
    Interpolación por el método de Lagrange
    
    Args:
        x_values: Lista de valores x (deben ser distintos)
        y_values: Lista de valores y correspondientes
        var: Variable para la expresión simbólica
    
    Returns:
        tuple: (polinomio_simplificado, función numérica)
    
    Raises:
        ValidationError: Si los puntos no son válidos para interpolación
    """
    try:
        # Validar entrada
        validate_input(x_values, y_values)
        
        x = sp.symbols(var)
        n = len(x_values)
        polinomio = 0
        
        # Construir polinomio de Lagrange
        for i in range(n):
            termino = y_values[i]
            for j in range(n):
                if j != i:
                    termino *= (x - x_values[j]) / (x_values[i] - x_values[j])
            polinomio += termino
        
        # Simplificar y convertir a función
        polinomio_simplificado = sp.simplify(polinomio)
        f = sp.lambdify(x, polinomio_simplificado, 'numpy')
        
        return polinomio_simplificado, f
    
    except ZeroDivisionError:
        raise ValidationError("División por cero - verifique valores de x")
    except Exception as e:
        raise ValidationError(f"Error en interpolación: {str(e)}")