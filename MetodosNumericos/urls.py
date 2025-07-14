# MetodosNumericos/urls.py

from django.urls import path
from django.views.generic.base import RedirectView
from MetodosNumericos.biseccion_views.w_views import calcular
from MetodosNumericos.biseccion_views.a_views import BiseccionAPI
from MetodosNumericos import views
from MetodosNumericos import views_int
 
app_name = 'MetodosNumericos'

urlpatterns = [
    path('', views.presentacion, name='portada'),
    path('calculo_B/', calcular, name='calculo_B'),
    path('api/biseccion/', BiseccionAPI.as_view(), name='biseccion_api'),
    path('resolver/', views.resolver_sistema, name='resolver'),
    path('Int', views_int.index, name='interpolaciones'),
    path('Principal', views.frontPage, name='frontPage'),  
]