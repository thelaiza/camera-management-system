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
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        senha = data.get('senha')

        try:
            usuario = Usuario.objects.get(email=email, senha=senha)
            return JsonResponse({
                'status': 'sucesso',
                'id': usuario.id,
                'nome': usuario.nome
            })
        except Usuario.DoesNotExist:
            return JsonResponse({'status': 'erro', 'mensagem': 'Credenciais inválidas'}, status=401)

# ========================================
# Funções para CRUD de Usuários e Câmeras
# ========================================

def listar_usuarios(request):
    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT u.id, u.nome, u.email, COUNT(c.id) AS quantidade_cameras
                FROM usuarios u
                LEFT JOIN cameras c ON u.id = c.usuario_id
                GROUP BY u.id
            """)
            colunas = [col[0] for col in cursor.description]
            usuarios = [dict(zip(colunas, linha)) for linha in cursor.fetchall()]
        return JsonResponse({'usuarios': usuarios})


@csrf_exempt
def listar_cameras(request):
    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, nome, localizacao, usuario_id, status FROM cameras")
            rows = cursor.fetchall()

        cameras = []
        for row in rows:
            cameras.append({
                'id': row[0],
                'nome': row[1],
                'localizacao': row[2],
                'usuario_id': row[3],
                'status': row[4]
            })

        return JsonResponse(cameras, safe=False)


@csrf_exempt
def adicionar_usuario(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            nome = data.get("nome")
            email = data.get("email")
            senha = data.get("senha")  

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
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nome = data.get('nome')
            localizacao = data.get('localizacao')
            status = data.get('status', 'pendente')
            usuario_id = data.get('usuario_id')

            if not nome or not localizacao or not usuario_id:
                return JsonResponse({'error': 'Todos os campos são obrigatórios'}, status=400)

            camera = Camera.objects.create(
                nome=nome,
                localizacao=localizacao,
                status=status,
                usuario_id=usuario_id
            )
            return JsonResponse({'success': True, 'id': camera.id}, status=201)
        except Exception as e:
            print("Erro ao adicionar câmera:", e)
            return JsonResponse({'error': 'Erro ao adicionar câmera'}, status=500)


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
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            usuario_id = data.get('usuario_id')
            nome = data.get('nome')
            localizacao = data.get('localizacao')
            status = data.get('status', 'pendente')

            if not usuario_id or not nome or not localizacao:
                return JsonResponse({'error': 'Usuário, nome e localização são obrigatórios'}, status=400)

            camera = Camera.objects.get(id=camera_id)
            camera.nome = nome
            camera.localizacao = localizacao
            camera.status = status
            camera.usuario_id = usuario_id
            camera.save()

            return JsonResponse({'success': True})
        except Camera.DoesNotExist:
            return JsonResponse({'error': 'Câmera não encontrada'}, status=404)
        except Exception as e:
            print("Erro ao editar câmera:", e)
            return JsonResponse({'error': 'Erro ao editar câmera'}, status=500)


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
