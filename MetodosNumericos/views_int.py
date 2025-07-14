from django.shortcuts import render
from .forms import PuntosForm
from .metodos.lagrange import interpolate_lagrange
from .metodos.newton import interpolate_newton
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr
import io
import base64
from sympy import latex
from django.core.exceptions import ValidationError

def index(request):
    if request.method == 'POST':
        form = PuntosForm(request.POST)
        if form.is_valid():
            try:
                # Procesar datos del formulario
                metodo = form.cleaned_data['metodo']
                puntos = form.cleaned_data['puntos']
                funcion_real = form.cleaned_data['funcion_real']
                rango_grafico = form.cleaned_data['rango_grafico']
                
                x_values = [p[0] for p in puntos]
                y_values = [p[1] for p in puntos]
                
                pasos = []
                graphs = []

                # Aplicar método seleccionado
                if metodo == 'lagrange':
                    polinomio, f = interpolate_lagrange(x_values, y_values)
                    
                    # Registrar pasos de Lagrange
                    x = sp.symbols('x')
                    n = len(x_values)
                    for i in range(n):
                        term_str = [f"{y_values[i]:.4f}"]
                        for j in range(n):
                            if j != i:
                                term_str.append(
                                    f"\\frac{{x - {x_values[j]:.4f}}}"
                                    f"{{{x_values[i]:.4f} - {x_values[j]:.4f}}}"
                                )
                        pasos.append(f"$L_{i}(x) = {' \\cdot '.join(term_str)}$")
                
                else:  # Newton
                    polinomio, f = interpolate_newton(x_values, y_values)
                    
                    # Registrar pasos de Newton
                    n = len(x_values)
                    dd_table = [y_values.copy()]
                    pasos = [f"y[{i}] = {y_values[i]:.4f}" for i in range(n)]
                    
                    for j in range(1, n):
                        columna = []
                        for i in range(n - j):
                            numerador = dd_table[j-1][i+1] - dd_table[j-1][i]
                            denominador = x_values[i+j] - x_values[i]
                            valor = numerador / denominador
                            columna.append(valor)
                            pasos.append(
                                f"f[x_{i},...,x_{i+j}] = "
                                f"({dd_table[j-1][i+1]:.4f} - {dd_table[j-1][i]:.4f}) / "
                                f"({x_values[i+j]:.4f} - {x_values[i]:.4f}) = {valor:.4f}"
                            )
                        dd_table.append(columna)
                
                # Generar gráficos
                graphs = generar_graficos(x_values, y_values, f, funcion_real, rango_grafico)
                
                return render(request, 'MetodosNumericos/Intresultados.html', {
                    'polinomio_latex': latex(sp.simplify(polinomio)),
                    'polinomio_texto': str(sp.simplify(polinomio)).replace('**', '^'),
                    'metodo': metodo,
                    'graphs': graphs,
                    'pasos_latex': [paso.replace('$', '') for paso in pasos],
                    'puntos': puntos,
                    'funcion_real': funcion_real
                })
            
            except ValidationError as e:
                form.add_error(None, e)
            except Exception as e:
                form.add_error(None, f"Error inesperado: {str(e)}")
    
    else:
        form = PuntosForm()
    
    return render(request, 'MetodosNumericos/Intresolver.html', {
        'form': form,
        'title': 'Interpolación Polinomial'
    })

def generar_graficos(x_values, y_values, f_interpolacion, funcion_real=None, rango=None):
    """Genera los gráficos de interpolación"""
    graphs = []
    
    # Determinar rango para gráfico
    x_min, x_max = (rango if rango else 
                    (min(x_values) - 1, max(x_values) + 1))
    
    x_plot = np.linspace(x_min, x_max, 400)
    y_interp = f_interpolacion(x_plot)
    
    # Gráfico 1: Puntos y curva interpolada
    plt.figure(figsize=(10, 6))
    plt.scatter(x_values, y_values, color='red', label='Puntos dados', zorder=5)
    plt.plot(x_plot, y_interp, label='Polinomio interpolado')
    plt.title('Interpolación Polinomial')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.grid(True)
    graphs.append(guardar_grafico())
    plt.close()
    
    # Gráfico 2: Comparación con función real (si se proporciona)
    if funcion_real:
        try:
            x = sp.symbols('x')
            f_real = sp.lambdify(x, parse_expr(funcion_real), 'numpy')
            y_real = f_real(x_plot)
            
            plt.figure(figsize=(10, 6))
            plt.plot(x_plot, y_real, label='Función real')
            plt.plot(x_plot, y_interp, '--', label='Aproximación')
            plt.scatter(x_values, y_values, color='red', zorder=5)
            plt.title('Comparación con Función Real')
            plt.xlabel('x')
            plt.ylabel('y')
            plt.legend()
            plt.grid(True)
            graphs.append(guardar_grafico())
            plt.close()
            
            # Gráfico 3: Error
            error = np.abs(y_real - y_interp)
            plt.figure(figsize=(10, 6))
            plt.plot(x_plot, error, color='orange', label='Error absoluto')
            plt.title('Error de Aproximación')
            plt.xlabel('x')
            plt.ylabel('Error')
            plt.legend()
            plt.grid(True)
            graphs.append(guardar_grafico())
            plt.close()
        
        except Exception as e:
            print(f"Error al graficar función real: {str(e)}")
    
    return graphs

def guardar_grafico():
    """Convierte el gráfico matplotlib a imagen base64"""
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', dpi=100)
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    return base64.b64encode(image_png).decode('utf-8')