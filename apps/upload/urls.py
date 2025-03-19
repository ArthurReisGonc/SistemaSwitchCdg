from django.urls import path
from . import views

urlpatterns = [
    path('', views.formulario_padrao, name='formulario_padrao'),
    path('formulario_rapido', views.formulario_rapido, name='formulario_rapido'),
    path('formulario_completo', views.formulario_completo, name='formulario_completo'),
]