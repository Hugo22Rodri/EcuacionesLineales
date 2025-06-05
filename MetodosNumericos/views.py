import numpy as np
import matplotlib.pyplot as plt
import io
import base64
from django.shortcuts import render
from .forms import MetodoForm 
from .metodos.gauss import eliminacion_gaussiana
from .metodos.gauss_jordan import gauss_jordan


def resolver_sistema(request):
    if request.method == 'POST':
        form = MetodoForm(request.POST)
        if form.is_valid():
            try:
                # Parsear ecuaciones
                ecuaciones = form.cleaned_data['ecuaciones']
                rows = [line.strip() for line in ecuaciones.split('\n') if line.strip()]
                A, b = [], []
                for row in rows:
                    coeffs = list(map(float, row.split()))
                    A.append(coeffs[:-1])
                    b.append(coeffs[-1])
                A = np.array(A, dtype=float)
                b = np.array(b, dtype=float)
                n = A.shape[0]
                
                # Procesar según método
                metodo = form.cleaned_data['metodo']
                contexto = {'form': form, 'metodo': metodo}
                
                if metodo == 'gauss':
                    sol, pasos = eliminacion_gaussiana(A.copy(), b.copy())
                    contexto['pasos'] = [p.tolist() for p in pasos]
                elif metodo == 'gauss_jordan':
                    sol, pasos = gauss_jordan(A.copy(), b.copy())
                    contexto['pasos'] = [p.tolist() for p in pasos]
                
                solucion_python = [float(x) for x in sol]
                
                # Comparación con solución exacta
                try:
                    x_exacta = np.linalg.solve(A, b)
                    plt.bar(range(n), sol, alpha=0.5, label='Numérica')
                    plt.bar(range(n), x_exacta, alpha=0.5, label='Exacta')
                    plt.legend()
                    buf = io.BytesIO()
                    plt.savefig(buf, format='png')
                    contexto['grafico_comparacion'] = base64.b64encode(buf.getvalue()).decode('utf-8')
                    plt.close()
                except:
                    pass
                
                # Usar la solución convertida a float nativo
                contexto['solucion'] = solucion_python
                return render(request, 'MetodosNumericos/resultados.html', contexto)
            except Exception as e:
                form.add_error(None, str(e))
    else:
        form = MetodoForm()
    return render(request, 'MetodosNumericos/resolver.html', {'form': form})