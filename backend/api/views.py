from django.http import JsonResponse
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.decorators import api_view

# API para verificar se o backend está rodando
def api_home(request):
    return JsonResponse({"message": "API está funcionando!"}, status=200)

# Rota para listar câmeras
def listar_cameras(request):
    return JsonResponse({"message": "Listando câmeras"}, status=200)

# Rota para listar usuários
def listar_usuarios(request):
    return JsonResponse({"message": "Listando usuários"}, status=200)

# Endpoint de login via API
@api_view(["POST"])
def api_login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response({"error": "Usuário e senha são obrigatórios"}, status=400)

    user = authenticate(username=username, password=password)
    
    if user and user.is_active:
        return Response({"message": "Login bem-sucedido!", "username": user.username}, status=200)

    return Response({"error": "Credenciais inválidas"}, status=401)
