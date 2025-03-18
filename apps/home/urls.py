# apps/home/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('home', views.index, name='home'),  # Rota para a página inicial do app home
]
