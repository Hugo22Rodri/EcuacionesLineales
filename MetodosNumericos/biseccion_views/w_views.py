from django.shortcuts import render
from MetodosNumericos.forms import BiseccionForm
from MetodosNumericos.utils.calculations import biseccion
from MetodosNumericos.utils.plotting import graficar_convergencia
from MetodosNumericos.models import CalculoBiseccion
import json

def calcular(request):
    pasos = []
    error = None
    if request.method == "POST":
        form = BiseccionForm(request.POST)
        if form.is_valid():
            datos = form.cleaned_data
            resultado = biseccion(datos)

            if "error" in resultado:
                error = resultado["error"]
            else:
                pasos = resultado.get("pasos", [])  # Extrae solo los pasos

            # Guardar en la base de datos
            CalculoBiseccion.objects.create(
                ecuacion=datos["ecuacion"],
                a=datos["a"],
                b=datos["b"],
                tolerancia=datos["tolerancia"],
                resultado=json.dumps(pasos)  # Guarda los pasos como JSON
            )

            # Genera la gráfica
            graficar_convergencia(pasos)

    else:
        form = BiseccionForm()

    return render(request, "MetodosNumericos/calculo_B.html", {"form": form, "pasos": pasos, "grafica_url": "/static/biseccion.png", "error": error})