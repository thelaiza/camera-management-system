from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
import json
from django.contrib.auth.hashers import make_password
from django.db import connection
from .models import Usuario, Camera, LogTransacao

@csrf_exempt
def api_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        senha = data.get('senha')
        try:
            usuario = Usuario.objects.get(email=email)
            if usuario.senha == senha:
                return JsonResponse({'status': 'sucesso', 'mensagem': 'Login bem-sucedido', 'usuario_id': usuario.id}, status=200)
            else:
                return JsonResponse({'status': 'erro', 'mensagem': 'Email ou senha inválidos'}, status=401)
        except Usuario.DoesNotExist:
            return JsonResponse({'status': 'erro', 'mensagem': 'Email ou senha inválidos'}, status=401)
    return JsonResponse({'status': 'erro', 'mensagem': 'Método não permitido'}, status=405)

@csrf_exempt
def adicionar_usuario(request):
    if request.method == "POST":
        try:
            # CORREÇÃO: Usar request.POST para formulários, ou json.loads para JSON
            data = request.POST 
            nome = data.get("nome")
            email = data.get("email")
            senha_pura = data.get("senha")
            
            if not nome or not email or not senha_pura:
                return JsonResponse({"erro": "Nome, email e senha são obrigatórios!"}, status=400)
            
            senha_criptografada = make_password(senha_pura)
            usuario_criado = Usuario(nome=nome, email=email, senha=senha_criptografada)
            usuario_criado.save()

            return JsonResponse({"mensagem": "Usuário cadastrado com sucesso!", "usuario_id": usuario_criado.id}, status=201)
        except IntegrityError:
            return JsonResponse({"erro": "O e-mail já está cadastrado!"}, status=400)
        except Exception as e:
            return JsonResponse({"erro": str(e)}, status=500)
    return JsonResponse({"erro": "Método não permitido!"}, status=405)


@csrf_exempt
def editar_usuario(request, usuario_id):
    try:
        usuario = Usuario.objects.get(id=usuario_id)
    except Usuario.DoesNotExist:
        return JsonResponse({"erro": "Usuário não encontrado"}, status=404)

    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            usuario.nome = data.get("nome", usuario.nome)
            usuario.email = data.get("email", usuario.email)
            if "senha" in data and data.get("senha"):
                usuario.senha = make_password(data.get("senha"))
            usuario.save()
            return JsonResponse({"mensagem": "Usuário atualizado com sucesso!"})
        except Exception as e:
            return JsonResponse({"erro": str(e)}, status=500)
            
    return JsonResponse({"erro": "Método não permitido!"}, status=405)


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
    return JsonResponse({"erro": "Método não permitido!"}, status=405)


@csrf_exempt
def listar_cameras(request):
    if request.method == 'GET':
        cameras = list(Camera.objects.values('id', 'nome', 'localizacao', 'usuario_id', 'status'))
        # CORREÇÃO: Retornar um dicionário, não uma lista
        return JsonResponse({'cameras': cameras}, safe=False)
    return JsonResponse({"erro": "Método não permitido!"}, status=405)


@csrf_exempt
def adicionar_camera(request):
    if request.method == 'POST':
        try:
            # CORREÇÃO: Usar json.loads para receber JSON
            data = json.loads(request.body)
            usuario_id = data.get('usuario_id')
            usuario = Usuario.objects.get(id=usuario_id)
            
            camera = Camera.objects.create(
                nome=data['nome'],
                localizacao=data['localizacao'],
                status=data.get('status', 'pendente'),
                usuario=usuario
            )
            return JsonResponse({'status': 'sucesso', 'id': camera.id}, status=201)
        except (KeyError, Usuario.DoesNotExist):
            return JsonResponse({'erro': 'Dados inválidos ou usuário não encontrado.'}, status=400)
        except Exception as e:
            return JsonResponse({'erro': f'Erro ao adicionar câmera: {str(e)}'}, status=500)
    # CORREÇÃO: Adicionar resposta para GET e outros métodos
    return JsonResponse({'erro': 'Método não permitido!'}, status=405)


@csrf_exempt
def excluir_usuario(request, id):
    try:
        usuario_a_excluir = Usuario.objects.get(id=id)
    except Usuario.DoesNotExist:
        return JsonResponse({"erro": "Usuário não encontrado."}, status=404)

    if request.method == "DELETE":
        try:
            usuario_a_excluir.delete()
            return JsonResponse({"mensagem": "Usuário excluído com sucesso!"}, status=200)
        except Exception as e:
            return JsonResponse({"erro": str(e)}, status=500)
    return JsonResponse({"erro": "Método não permitido!"}, status=405)


@csrf_exempt
def excluir_camera(request, id):
    try:
        camera = Camera.objects.get(id=id)
    except Camera.DoesNotExist:
        return JsonResponse({"erro": "Câmera não encontrada."}, status=404)

    if request.method == "DELETE":
        try:
            camera.delete()
            return JsonResponse({"mensagem": "Câmera excluída com sucesso!"}, status=200)
        except Exception as e:
            return JsonResponse({"erro": str(e)}, status=500)
    return JsonResponse({"erro": "Método não permitido!"}, status=405)


@csrf_exempt
def editar_camera(request, camera_id):
    try:
        camera = Camera.objects.get(id=camera_id)
    except Camera.DoesNotExist:
        return JsonResponse({'erro': 'Câmera não encontrada'}, status=404)
        
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            camera.nome = data.get('nome', camera.nome)
            camera.localizacao = data.get('localizacao', camera.localizacao)
            camera.status = data.get('status', camera.status)
            if 'usuario_id' in data:
                camera.usuario = Usuario.objects.get(id=data['usuario_id'])
            camera.save()
            return JsonResponse({'success': True})
        except Usuario.DoesNotExist:
            return JsonResponse({'erro': 'Usuário responsável não encontrado'}, status=400)
        except Exception as e:
            return JsonResponse({'erro': f'Erro ao editar câmera: {str(e)}'}, status=500)
    return JsonResponse({"erro": "Método não permitido!"}, status=405)


def api_home(request):
    return JsonResponse({"mensagem": "API está rodando!"})


def listar_logs(request):
    if request.method == 'GET':
        logs = LogTransacao.objects.all().order_by('-data_hora')
        logs_list = list(logs.values('id', 'acao', 'data_hora', 'usuario_id', 'camera_id'))
        return JsonResponse(logs_list, safe=False)
    return JsonResponse({"erro": "Método não permitido!"}, status=405)