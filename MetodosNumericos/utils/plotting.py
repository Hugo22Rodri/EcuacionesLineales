import matplotlib.pyplot as plt
import os
from django.conf import settings

def graficar_convergencia(pasos):
    """ Genera y guarda la gráfica de convergencia en static/biseccion.png """
    iteraciones = range(len(pasos))
    valores_c = [p[2] for p in pasos]

    plt.figure()
    plt.plot(iteraciones, valores_c, marker='o', linestyle='--', color='blue')
    plt.xlabel("Iteración")
    plt.ylabel("Valor de c")
    plt.title("Convergencia del Método de Bisección")
    plt.grid()

    ruta_static = os.path.join(settings.BASE_DIR, "static", "biseccion.png")
    plt.savefig(ruta_static)