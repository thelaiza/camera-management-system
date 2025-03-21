# Lógica de requisições HTTP (tipo os controllers do Express)

from django.http import JsonResponse

def listar_cameras(request):
    return JsonResponse({"message": "Listando câmeras"})

def listar_usuarios(request):
    return JsonResponse({"message": "Listando usuários"})
