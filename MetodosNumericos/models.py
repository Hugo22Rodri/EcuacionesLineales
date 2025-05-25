from django.db import models

class SistemaEcuaciones(models.Model):
    ecuaciones = models.TextField()
    metodo = models.CharField(max_length=20)
    fecha_calculo = models.DateTimeField(auto_now_add=True)
    solucion = models.JSONField()

    def __str__(self):
        return f"{self.metodo} - {self.fecha_calculo}"