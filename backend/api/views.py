from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
import json
from django.contrib.auth.hashers import make_password, check_password
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
            if check_password(senha, usuario.senha):
                return JsonResponse({
                    'status': 'sucesso',
                    'id': usuario.id,
                    'nome': usuario.nome
                })
            else:
                return JsonResponse({'status': 'erro', 'mensagem': 'Credenciais inválidas'}, status=401)
        except Usuario.DoesNotExist:
            return JsonResponse({'status': 'erro', 'mensagem': 'Credenciais inválidas'}, status=401)

@csrf_exempt
def adicionar_usuario(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            nome = data.get("nome")
            email = data.get("email")
            senha_pura = data.get("senha")
            autor_id = data.get("autor_id")
            
            if not nome or not email or not senha_pura or not autor_id:
                return JsonResponse({"erro": "Todos os campos são obrigatórios!"}, status=400)
            
            autor_acao = Usuario.objects.get(id=autor_id)
            senha_criptografada = make_password(senha_pura)
            usuario_criado = Usuario(nome=nome, email=email, senha=senha_criptografada)
            usuario_criado.save()

            LogTransacao.objects.create(
                usuario_id=autor_acao.id,
                acao=f"Usuário '{autor_acao.nome}' cadastrou o novo usuário '{usuario_criado.nome}'."
            )

            return JsonResponse({"mensagem": "Usuário cadastrado com sucesso!", "usuario_id": usuario_criado.id}, status=201)
        except IntegrityError:
            return JsonResponse({"erro": "O e-mail já está cadastrado!"}, status=400)
        except Exception as e:
            return JsonResponse({"erro": str(e)}, status=500)
    else:
        return JsonResponse({"erro": "Método não permitido!"}, status=405)

@csrf_exempt
def editar_usuario(request, usuario_id):
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            usuario = Usuario.objects.get(id=usuario_id)
            autor_id = data.get('autor_id', usuario_id) 
            autor_acao = Usuario.objects.get(id=autor_id)

            if "nome" in data:
                usuario.nome = data.get("nome")
            if "email" in data:
                usuario.email = data.get("email")
            if "senha" in data and data.get("senha"):
                usuario.senha = make_password(data.get("senha"))
            
            usuario.save()

            LogTransacao.objects.create(
                usuario_id=autor_acao.id,
                acao=f"Usuário '{autor_acao.nome}' atualizou os dados do usuário '{usuario.nome}'."
            )

            return JsonResponse({"mensagem": "Usuário atualizado com sucesso!"}, status=200)
        except Usuario.DoesNotExist:
            return JsonResponse({"erro": "Usuário não encontrado"}, status=404)
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

@csrf_exempt
def listar_cameras(request):
    if request.method == 'GET':
        cameras = list(Camera.objects.values('id', 'nome', 'localizacao', 'usuario_id', 'status'))
        return JsonResponse(cameras, safe=False)

@csrf_exempt
def adicionar_camera(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            usuario_id = data.get('usuario_id')

            autor_acao = Usuario.objects.get(id=usuario_id)
            camera = Camera.objects.create(
                nome=data.get('nome'),
                localizacao=data.get('localizacao'),
                status=data.get('status', 'pendente'),
                usuario_id=usuario_id
            )

            LogTransacao.objects.create(
                usuario_id=autor_acao.id,
                camera_id=camera.id,
                acao=f"Usuário '{autor_acao.nome}' cadastrou a câmera '{camera.nome}'."
            )

            return JsonResponse({'success': True, 'id': camera.id}, status=201)
        except Exception as e:
            return JsonResponse({'error': f'Erro ao adicionar câmera: {str(e)}'}, status=500)

@csrf_exempt
def excluir_usuario(request, id):
    if request.method == "DELETE":
        try:
            data = json.loads(request.body)
            autor_id = data.get('autor_id')
            autor_acao = Usuario.objects.get(id=autor_id)

            usuario_a_excluir = Usuario.objects.get(id=id)
            nome_usuario_excluido = usuario_a_excluir.nome
            
            usuario_a_excluir.delete()
            
            LogTransacao.objects.create(
                usuario_id=autor_acao.id,
                acao=f"Usuário '{autor_acao.nome}' excluiu o usuário '{nome_usuario_excluido}' do sistema."
            )

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
            data = json.loads(request.body)
            autor_id = data.get('autor_id')
            autor_acao = Usuario.objects.get(id=autor_id)
            
            camera = Camera.objects.get(id=id)
            nome_camera_excluida = camera.nome
            
            camera.delete()

            LogTransacao.objects.create(
                usuario_id=autor_acao.id,
                acao=f"Usuário '{autor_acao.nome}' excluiu a câmera '{nome_camera_excluida}'."
            )
            
            return JsonResponse({"mensagem": "Câmera excluída com sucesso!"}, status=200)
        except Camera.DoesNotExist:
            return JsonResponse({"erro": "Câmera não encontrada."}, status=404)
        except Usuario.DoesNotExist:
            return JsonResponse({"erro": "Autor da ação não encontrado."}, status=404)
        except Exception as e:
            return JsonResponse({"erro": str(e)}, status=500)
    return JsonResponse({"erro": "Método não permitido!"}, status=405)


@csrf_exempt
def editar_camera(request, camera_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            camera = Camera.objects.get(id=camera_id)
            autor_id = data.get('usuario_id')
            autor_acao = Usuario.objects.get(id=autor_id)

            camera.nome = data.get('nome', camera.nome)
            camera.localizacao = data.get('localizacao', camera.localizacao)
            camera.status = data.get('status', camera.status)
            camera.usuario_id = autor_id
            camera.save()

            LogTransacao.objects.create(
                usuario_id=autor_acao.id,
                camera_id=camera.id,
                acao=f"Usuário '{autor_acao.nome}' editou a câmera '{camera.nome}'."
            )

            return JsonResponse({'success': True})
        except Camera.DoesNotExist:
            return JsonResponse({'error': 'Câmera não encontrada'}, status=404)
        except Exception as e:
            return JsonResponse({'error': f'Erro ao editar câmera: {str(e)}'}, status=500)

def api_home(request):
    return JsonResponse({"mensagem": "API está rodando!"})

def listar_logs(request):
    if request.method == 'GET':
        logs = LogTransacao.objects.all().order_by('-data_hora')
        logs_list = list(logs.values('id', 'acao', 'data_hora', 'usuario_id', 'camera_id'))
        return JsonResponse(logs_list, safe=False)
    return JsonResponse({"erro": "Método não permitido!"}, status=405)
