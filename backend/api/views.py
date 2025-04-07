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

def listar_usuarios(request):
    if request.method == "GET":
        try:
            usuarios = Usuario.objects.all().values("id", "nome", "email")
            return JsonResponse(list(usuarios), safe=False, status=200)
        except Exception as e:
            return JsonResponse({"erro": str(e)}, status=500)
    return JsonResponse({"erro": "Método não permitido!"}, status=405)


def listar_cameras(request):
    if request.method == "GET":
        try:
            cameras = Camera.objects.all().values("id", "nome", "localizacao", "usuario_id", "data_criacao")
            return JsonResponse(list(cameras), safe=False, status=200)
        except Exception as e:
            return JsonResponse({"erro": str(e)}, status=500)
    return JsonResponse({"erro": "Método não permitido!"}, status=405)

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

@csrf_exempt
def excluir_usuario(request, id):
    if request.method == "DELETE":
        try:
            usuario = Usuario.objects.get(id=id)
            usuario.delete()
            return JsonResponse({"mensagem": "Usuário excluído com sucesso!"}, status=200)
        except Usuario.DoesNotExist:
            return JsonResponse({"erro": "Usuário não encontrado."}, status=404)
        except Exception as e:
            return JsonResponse({"erro": str(e)}, status=500)
    return JsonResponse({"erro": "Método não permitido!"}, status=405)


@csrf_exempt
def excluir_camera(request, id):
    if request.method == "DELETE":
        try:
            camera = Camera.objects.get(id=id)
            camera.delete()
            return JsonResponse({"mensagem": "Câmera excluída com sucesso!"}, status=200)
        except Camera.DoesNotExist:
            return JsonResponse({"erro": "Câmera não encontrada."}, status=404)
        except Exception as e:
            return JsonResponse({"erro": str(e)}, status=500)
    return JsonResponse({"erro": "Método não permitido!"}, status=405)

@csrf_exempt
def editar_camera(request, camera_id):
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            nome = data.get("nome")
            localizacao = data.get("localizacao")
            usuario_id = data.get("usuario_id")
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE cameras
                    SET nome = %s, localizacao = %s, usuario_id = %s
                    WHERE id = %s
                    """,
                    [nome, localizacao, usuario_id, camera_id]
                )

            return JsonResponse({"mensagem": "Câmera atualizada com sucesso!"}, status=200)
        except Exception as e:
            return JsonResponse({"erro": str(e)}, status=500)
    return JsonResponse({"erro": "Método não permitido!"}, status=405)

@csrf_exempt
def editar_usuario(request, usuario_id):
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            nome = data.get("nome")
            email = data.get("email")
            senha = data.get("senha")
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE usuarios
                    SET nome = %s, email = %s, senha = %s
                    WHERE id = %s
                    """,
                    [nome, email, senha, usuario_id]
                )

            return JsonResponse({"mensagem": "Usuário atualizado com sucesso!"}, status=200)
        except Exception as e:
            return JsonResponse({"erro": str(e)}, status=500)
    return JsonResponse({"erro": "Método não permitido!"}, status=405)

# ========================================
# Função de verificação da API 
# ========================================
def api_home(request):
    return JsonResponse({"mensagem": "API está rodando!"})
