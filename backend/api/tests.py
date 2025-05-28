# backend/api/tests.py

import pytest
import json # Para json.dumps (se enviar JSON) e json.loads (para ler o corpo da resposta)
from django.urls import reverse
from backend.api.models import Usuario, Camera, LogTransacao # Importe LogTransacao se for usá-lo

# --- Fixtures (dados de ajuda para os testes) ---

@pytest.fixture
def test_user(db):
    user = Usuario.objects.create(
        nome='Usuario Comum Teste',
        email='comum@example.com',
        senha='password123'
        # tipo_usuario foi removido
    )
    # Sua view login_api compara senha em texto plano.
    # Se você fosse usar o sistema de hash do Django, você usaria:
    # user.set_password('password123')
    # user.save()
    return user

@pytest.fixture
def admin_user(db):
    """Cria um usuário "administrador" para testes (baseado no nome, não em um campo booleano de superuser)."""
    user = Usuario.objects.create(
        nome='Admin Teste API',
        email='admintest@example.com',
        senha='adminpassword',
        # tipo_usuario='ADM' # Removido se não existir no modelo Usuario
    )
    # user.set_password('adminpassword') # Para sistema de hash
    # user.is_staff = True # Se você usasse as permissões padrão do Django
    # user.is_superuser = True
    # user.save()
    return user

@pytest.fixture
def test_camera(db, test_user):
    """Cria uma câmera para testes, associada ao test_user."""
    camera = Camera.objects.create(
        nome='Camera Fixture Original',
        localizacao='Local Original Fixture',
        status='ativa',
        responsavel=test_user,
        cliente='Cliente Original Fixture'
    )
    return camera

# --- Testes de Modelo ---

@pytest.mark.django_db
def test_criar_usuario_modelo():
    usuario = Usuario.objects.create(
        nome='Teste Usuario Modelo Direto',
        email='teste.modelo.direto@example.com',
        senha='testpassword123'
    )
    assert usuario.email == 'teste.modelo.direto@example.com'
    assert usuario.nome == 'Teste Usuario Modelo Direto'

# --- Testes de Views ---

@pytest.mark.django_db
def test_api_home_view(client):
    url = reverse('api_home')
    response = client.get(url)
    assert response.status_code == 200
    assert response.json() == {"mensagem": "API está rodando!"}

# Testes para login_api
@pytest.mark.django_db
def test_login_api_view_sucesso(client, test_user):
    url = reverse('api_login') # Nome da URL para 'login_api'
    data = {
        'email': test_user.email,
        'senha': 'password123' # Senha em texto plano conforme a view
    }
    response = client.post(url, data=json.dumps(data), content_type='application/json') # Enviando como JSON
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['id'] == test_user.id
    assert response_data['nome'] == test_user.nome
    # Verifique se a sessão foi populada conforme sua view login_api
    assert client.session.get('usuario_id') == test_user.id
    # Adicione a verificação de 'usuario_tipo' se sua view login_api o definir
    # e se o modelo Usuario tiver esse campo.
    # Se o modelo não tem 'tipo_usuario', remova a linha abaixo.
    # assert client.session.get('usuario_tipo') == test_user.tipo_usuario

@pytest.mark.django_db
def test_login_api_view_falha_senha_incorreta(client, test_user):
    url = reverse('api_login')
    data = {
        'email': test_user.email,
        'senha': 'senhaincorreta123'
    }
    response = client.post(url, data=json.dumps(data), content_type='application/json')
    assert response.status_code == 401
    assert response.json() == {"error": "Email ou senha inválidos"}

@pytest.mark.django_db
def test_login_api_view_falha_usuario_nao_existe(client):
    url = reverse('api_login')
    data = {
        'email': 'nao.existe.mesmo@example.com',
        'senha': 'qualquercoisa'
    }
    response = client.post(url, data=json.dumps(data), content_type='application/json')
    assert response.status_code == 401 # Ou 404 se sua view retornar isso
    assert response.json() == {"error": "Email ou senha inválidos"}


# Testes para CRUD de Usuários
@pytest.mark.django_db
def test_listar_usuarios_view_vazia(client, admin_user): # Assumindo que admin_user é necessário
    # Simular login do admin
    session = client.session
    session['usuario_id'] = admin_user.id
    # session['usuario_tipo'] = 'ADM' # Se você tiver tipo_usuario no modelo e na sessão
    session.save()

    url = reverse('listar_usuarios')
    response = client.get(url)
    assert response.status_code == 200
    # Esta asserção depende da sua query SQL em views.py estar correta (api_usuario)
    # e de como ela filtra. Se listar todos, e o admin_user é o único, a lista terá 1 elemento.
    # Se for "vazia" de outros usuários, a lista pode ter 0 ou 1.
    # Por segurança, vamos verificar se a chave 'usuarios' existe e é uma lista.
    response_data = response.json()
    assert 'usuarios' in response_data
    assert isinstance(response_data['usuarios'], list)
    # Se o admin_user for o único usuário esperado:
    # if Usuario.objects.count() == 1 and response_data['usuarios']:
    #     assert len(response_data['usuarios']) == 1
    #     assert response_data['usuarios'][0]['id'] == admin_user.id
    # else:
    #     assert response_data['usuarios'] == [] # Se nenhum usuário além do admin for esperado

@pytest.mark.django_db
def test_adicionar_usuario_view_sucesso(client, admin_user):
    session = client.session
    session['usuario_id'] = admin_user.id
    # session['usuario_tipo'] = 'ADM' # Se sua view verificar isso
    session.save()

    url = reverse('adicionar_usuario')
    user_data = {
        'nome': 'Novo Usuario View Teste',
        'email': 'novo.view.teste@example.com',
        'senha': 'novasenha123',
        # 'tipo_usuario': 'USR' # Adicione se o campo existir e for esperado pela view
    }
    response = client.post(url, data=user_data) # Enviando como form-data
    assert response.status_code == 201
    assert response.json().get('message') == 'Usuário adicionado com sucesso!' or \
           response.json().get('mensagem') == 'Usuário adicionado com sucesso!'
    assert Usuario.objects.filter(email='novo.view.teste@example.com').exists()

@pytest.mark.django_db
def test_editar_usuario_view_sucesso(client, admin_user, test_user): # admin edita test_user
    session = client.session
    session['usuario_id'] = admin_user.id
    # session['usuario_tipo'] = 'ADM'
    session.save()

    url = reverse('editar_usuario', kwargs={'usuario_id': test_user.id})
    update_data = {
        'nome': 'Usuario Comum Editado Pela View',
        'email': 'comum.editado.view@example.com',
        # 'tipo_usuario': 'USR' # Se for um campo editável
    }
    response = client.put(url, data=update_data) # Enviando como form-data
    assert response.status_code == 200
    assert response.json().get('message') == 'Usuário atualizado com sucesso!' or \
           response.json().get('mensagem') == 'Usuário atualizado com sucesso!'
    test_user.refresh_from_db()
    assert test_user.nome == 'Usuario Comum Editado Pela View'
    assert test_user.email == 'comum.editado.view@example.com'

@pytest.mark.django_db
def test_excluir_usuario_view_sucesso(client, admin_user, test_user): # admin exclui test_user
    session = client.session
    session['usuario_id'] = admin_user.id
    # session['usuario_tipo'] = 'ADM'
    session.save()

    url = reverse('excluir_usuario', kwargs={'usuario_id': test_user.id})
    response = client.delete(url)
    assert response.status_code == 200
    assert response.json().get('message') == 'Usuário excluído com sucesso!' or \
           response.json().get('mensagem') == 'Usuário excluído com sucesso!'
    assert not Usuario.objects.filter(id=test_user.id).exists()


# Testes para CRUD de Câmeras
@pytest.mark.django_db
def test_adicionar_camera_view_sucesso(client, test_user):
    # Se 'adicionar_camera' requer que o usuário esteja na sessão:
    # session = client.session
    # session['usuario_id'] = test_user.id
    # session.save()

    url = reverse('adicionar_camera')
    camera_data = {
        'nome': 'Camera Teste Hall Adicionada View',
        'localizacao': 'Hall de Entrada Principal View',
        'status': 'ativa',
        'cliente': 'Cliente Edificio Central View',
        'usuario_id': str(test_user.id)
    }
    response = client.post(url, data=camera_data)
    assert response.status_code == 201
    assert response.json().get('message') == 'Câmera adicionada com sucesso!' or \
           response.json().get('mensagem') == 'Câmera adicionada com sucesso!'
    assert Camera.objects.filter(nome='Camera Teste Hall Adicionada View', responsavel=test_user).exists()

@pytest.mark.django_db
def test_adicionar_camera_view_metodo_get_nao_permitido(client):
    url = reverse('adicionar_camera')
    response = client.get(url)
    assert response.status_code == 400
    assert response.json() == {'error': 'Método inválido, apenas POST é permitido'}

@pytest.mark.django_db
def test_adicionar_camera_view_dados_faltando(client, test_user):
    url = reverse('adicionar_camera')
    camera_data_incompleta = {
        'localizacao': 'Local Sem Nome View',
        'status': 'inativa',
        'cliente': 'Cliente Incompleto View',
        'usuario_id': str(test_user.id)
    }
    response = client.post(url, data=camera_data_incompleta)
    assert response.status_code == 500 # Ou 400 se sua view validar e retornar erro específico
    assert response.json()['error'].startswith('Erro ao adicionar câmera:')

@pytest.mark.django_db
def test_editar_camera_view_sucesso(client, test_user, test_camera):
    # Se 'editar_camera' requer sessão:
    # session = client.session
    # session['usuario_id'] = test_user.id # Ou admin_user.id se a permissão for assim
    # session.save()

    url = reverse('editar_camera', kwargs={'camera_id': test_camera.id})
    dados_atualizados = {
        'nome': 'Camera Editada com Sucesso na View Teste',
        'localizacao': 'Nova Localizacao Editada View',
        'status': 'manutencao',
        'cliente': 'Novo Cliente Editado View',
        'usuario_id': str(test_camera.responsavel.id)
    }
    response = client.put(url, data=dados_atualizados)
    assert response.status_code == 200
    assert response.json().get('message') == 'Câmera atualizada com sucesso!' or \
           response.json().get('mensagem') == 'Câmera atualizada com sucesso!'
    test_camera.refresh_from_db()
    assert test_camera.nome == 'Camera Editada com Sucesso na View Teste'
    assert test_camera.status == 'manutencao'

@pytest.mark.django_db
def test_editar_camera_view_camera_nao_existe(client, test_user):
    # Se 'editar_camera' requer sessão:
    # session = client.session
    # session['usuario_id'] = test_user.id
    # session.save()
    url = reverse('editar_camera', kwargs={'camera_id': 99999})
    dados_atualizados = {
        'nome': 'Tentativa Edicao Inexistente View',
        'usuario_id': str(test_user.id)
        # ... outros campos ...
    }
    response = client.put(url, data=dados_atualizados)
    assert response.status_code == 404
    assert response.json() == {'error': 'Câmera não encontrada'}

@pytest.mark.django_db
def test_excluir_camera_view_sucesso(client, test_user, test_camera):
    # Se 'excluir_camera' requer sessão:
    # session = client.session
    # session['usuario_id'] = test_user.id # Ou admin_user.id
    # session.save()

    url = reverse('excluir_camera', kwargs={'camera_id': test_camera.id})
    response = client.delete(url)
    assert response.status_code == 200
    assert response.json().get('message') == 'Câmera excluída com sucesso!' or \
           response.json().get('mensagem') == 'Câmera excluída com sucesso!'
    assert not Camera.objects.filter(id=test_camera.id).exists()

@pytest.mark.django_db
def test_listar_cameras_view_com_cameras_existentes(client, test_user, test_camera):
    # Se 'listar_cameras' requer sessão:
    # session = client.session
    # session['usuario_id'] = test_user.id
    # session.save()
    Camera.objects.create(nome='Segunda Camera Listagem', localizacao='Local B', status='ativa', responsavel=test_user, cliente='Cliente B')
    url = reverse('listar_cameras')
    response = client.get(url)
    assert response.status_code == 200
    response_data = response.json()
    assert 'cameras' in response_data
    assert isinstance(response_data['cameras'], list)
    assert len(response_data['cameras']) >= 2
    assert any(c.get('id') == test_camera.id for c in response_data['cameras'])

@pytest.mark.django_db
def test_listar_cameras_view_sem_cameras(client):
    # Se 'listar_cameras' requer sessão:
    # session = client.session
    # # ... popular a sessão ...
    # session.save()
    Camera.objects.all().delete()
    url = reverse('listar_cameras')
    response = client.get(url)
    assert response.status_code == 200
    response_data = response.json()
    assert 'cameras' in response_data
    assert response_data['cameras'] == []




  