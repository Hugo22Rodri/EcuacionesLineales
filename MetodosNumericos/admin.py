from django.contrib import admin
from .models import SistemaEcuaciones

@admin.register(SistemaEcuaciones)
class SistemaEcuacionesAdmin(admin.ModelAdmin):
    list_display = ('id', 'metodo', 'fecha_calculo')
    search_fields = ('metodo',)
    list_filter = ('metodo', 'fecha_calculo')