import numpy as np
import matplotlib.pyplot as plt
import io
import base64
from django.shortcuts import render
from .forms import MetodoForm
from .metodos.gauss import eliminacion_gaussiana
from .metodos.gauss_jordan import gauss_jordan
from .utils_Chat import get_explanation_from_openai, formatear_steps_para_ia

# Vista para la página de presentación
def presentacion(request):
    """
    Muestra la página de presentación con los botones de navegación.
    """
    return render(request, 'MetodosNumericos/frontPage.html')

def frontPage(request):
    return render(request, 'MetodosNumericos/frontPage.html')

def resolver_sistema(request):
    if request.method == 'POST':
        form = MetodoForm(request.POST)
        if form.is_valid():
            try:
                # --- PARSEAR ECUACIONES ---
                ecuaciones = form.cleaned_data['ecuaciones']
                filas = [line.strip() for line in ecuaciones.split('\n') if line.strip()]
                A, b = [], []
                for fila in filas:
                    coef = list(map(float, fila.split()))
                    A.append(coef[:-1])
                    b.append(coef[-1])
                A = np.array(A, dtype=float)
                b = np.array(b, dtype=float)
                n = A.shape[0]

                # --- SELECCIÓN DE MÉTODO ---
                metodo = form.cleaned_data['metodo']
                contexto = {'form': form, 'metodo': metodo}
                sol = None
                pasos = []

                if metodo == 'gauss':
                    sol, pasos = eliminacion_gaussiana(A.copy(), b.copy())
                    metodo_nombre = "eliminación Gaussiana"
                elif metodo == 'gauss_jordan':
                    sol, pasos = gauss_jordan(A.copy(), b.copy())
                    metodo_nombre = "Gauss-Jordan"
                else:
                    raise ValueError("Método no válido.")

                # --- PREPARAR MATRICES Y EXPLICACIÓN DE IA ---
                contexto['pasos'] = [p.tolist() for p in pasos]  # Para mostrar matrices si lo deseas
                pasos_formateados = formatear_steps_para_ia(pasos)
                explicacion = get_explanation_from_openai(metodo_nombre, pasos_formateados)
                contexto['explicacion_ia'] = explicacion

                # --- RESULTADO DE LA SOLUCIÓN ---
                solucion_python = [float(x) for x in sol]
                contexto['solucion'] = solucion_python

                # --- COMPARACIÓN CON SOLUCIÓN EXACTA (gráfico) ---
                try:
                    x_exacta = np.linalg.solve(A, b)
                    plt.bar(range(n), sol, alpha=0.5, label='Numérica')
                    plt.bar(range(n), x_exacta, alpha=0.5, label='Exacta')
                    plt.xticks(range(n), [f'x{i+1}' for i in range(n)])
                    plt.ylabel('Valor')
                    plt.title('Comparación de soluciones')
                    plt.legend()
                    buf = io.BytesIO()
                    plt.savefig(buf, format='png')
                    contexto['grafico_comparacion'] = base64.b64encode(buf.getvalue()).decode('utf-8')
                    plt.close()
                except:
                    pass

                return render(request, 'MetodosNumericos/resultados.html', contexto)
            except Exception as e:
                form.add_error(None, str(e))
    else:
        form = MetodoForm()
    return render(request, 'MetodosNumericos/resolver.html', {'form': form})