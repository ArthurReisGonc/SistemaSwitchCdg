# apps/home/views.py
from django.shortcuts import render

def index(request):
    return render(request, 'home/index.html')  # Certifique-se de que o caminho está correto
