from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from .models import Usuario, Camera
import json
from django.db import connection

# ========================================
# Função de login 
# ========================================
@csrf_exempt
def api_login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")
        senha = data.get("senha")

        try:
            usuario = Usuario.objects.get(email=email, senha=senha)
            return JsonResponse({"mensagem": "Login bem-sucedido!", "usuario_id": usuario.id}, status=200)
        except ObjectDoesNotExist:
            return JsonResponse({"erro": "Credenciais inválidas."}, status=401)

# ========================================
# Funções para CRUD de Usuários e Câmeras
# ========================================


@csrf_exempt
def adicionar_usuario(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            nome = data.get("nome")
            email = data.get("email")
            senha = data.get("senha")  # Aqui você pode adicionar um hash na senha

            if not nome or not email or not senha:
                return JsonResponse({"erro": "Todos os campos são obrigatórios!"}, status=400)

            usuario = Usuario(nome=nome, email=email, senha=senha)
            usuario.save()

            return JsonResponse({"mensagem": "Usuário cadastrado com sucesso!", "usuario_id": usuario.id}, status=201)
        except IntegrityError:
            return JsonResponse({"erro": "O e-mail já está cadastrado!"}, status=400)
        except Exception as e:
            return JsonResponse({"erro": str(e)}, status=500)
    else:
        return JsonResponse({"erro": "Método não permitido!"}, status=405)


@csrf_exempt
def adicionar_camera(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            nome = data.get("nome")
            localizacao = data.get("localizacao")
            usuario_id = data.get("usuario_id")  
            if not nome or not localizacao:
                return JsonResponse({"erro": "Nome e localização são obrigatórios!"}, status=400)
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO cameras (nome, localizacao, usuario_id) VALUES (%s, %s, %s)",
                    [nome, localizacao, usuario_id],
                )
            return JsonResponse({"mensagem": "Câmera adicionada com sucesso!"}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"erro": "JSON inválido!"}, status=400)
        except Exception as e:
            return JsonResponse({"erro": str(e)}, status=500)
    return JsonResponse({"erro": "Método não permitido!"}, status=405)

# ========================================
# Função de verificação da API 
# ========================================
def api_home(request):
    return JsonResponse({"mensagem": "API está rodando!"})
