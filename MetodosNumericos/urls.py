# MetodosNumericos/urls.py

from django.urls import path
from django.views.generic.base import RedirectView
from MetodosNumericos.biseccion_views.w_views import calcular
from MetodosNumericos.biseccion_views.a_views import BiseccionAPI
from MetodosNumericos import views
from MetodosNumericos import views_int
 
app_name = 'MetodosNumericos'

urlpatterns = [
    #Paginas de inicio
    path('', views.presentacion, name='portada'),
    path('principal', views.frontPage, name='frontPage'), 

    # Paginas de metodos numericos
    path('resolver/', views.resolver_sistema, name='resolver'),
    path('Interpolaciones', views_int.index, name='interpolaciones'),
    path('calculo_biseccion/', calcular, name='calculo_B'),
    
    # APIs
    path('api/biseccion/', BiseccionAPI.as_view(), name='biseccion_api'),
]