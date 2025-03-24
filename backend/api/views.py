# Lógica de requisições HTTP (tipo os controllers do Express)

from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.decorators import api_view

def listar_cameras(request):
    return JsonResponse({"message": "Listando câmeras"})

def listar_usuarios(request):
    return JsonResponse({"message": "Listando usuários"})

def home(request):
    return HttpResponse("Bem-vindo ao CamIA Manager!")

from django.shortcuts import render

def home(request):
    return render(request, "home.html")

@api_view(["POST"])
def api_login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(username=username, password=password)
    if user:
        return Response({"message": "Login bem-sucedido!"})
    return Response({"message": "Credenciais inválidas"}, status=401)
