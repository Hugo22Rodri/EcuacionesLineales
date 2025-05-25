from django.urls import path
from . import views

app_name = 'MetodosNumericos'

urlpatterns = [
    path('', views.resolver_sistema, name='resolver'),
]