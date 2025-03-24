# Lógica de requisições HTTP (tipo os controllers do Express)

from django.http import JsonResponse
from django.http import HttpResponse

def listar_cameras(request):
    return JsonResponse({"message": "Listando câmeras"})

def listar_usuarios(request):
    return JsonResponse({"message": "Listando usuários"})

def home(request):
    return HttpResponse("Bem-vindo ao CamIA Manager!")

from django.shortcuts import render

def home(request):
    return render(request, "home.html")
