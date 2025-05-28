import pytest
import json
from django.urls import reverse
from backend.api.models import Usuario, Camera, LogTransacao 

@pytest.fixture
def test_user(db):
    user = Usuario.objects.create(
        nome='Usuario Comum Teste',
        email='comum@example.com',
        senha='password123'
    )
    return user

@pytest.fixture
def admin_user(db):
    """Cria um usuário "administrador" para testes (baseado no nome, não em um campo booleano de superuser)."""
    user = Usuario.objects.create(
        nome='Admin Teste API',
        email='admintest@example.com',
        senha='adminpassword',
    )
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

@pytest.mark.django_db
def test_criar_usuario_modelo():
    usuario = Usuario.objects.create(
        nome='Teste Usuario Modelo Direto',
        email='teste.modelo.direto@example.com',
        senha='testpassword123'
    )
    assert usuario.email == 'teste.modelo.direto@example.com'
    assert usuario.nome == 'Teste Usuario Modelo Direto'

@pytest.mark.django_db
def test_api_home_view(client):
    url = reverse('api_home')
    response = client.get(url)
    assert response.status_code == 200
    assert response.json() == {"mensagem": "API está rodando!"}

@pytest.mark.django_db
def test_login_api_view_sucesso(client, test_user):
    url = reverse('api_login') 
    data = {
        'email': test_user.email,
        'senha': 'password123' 
    }
    response = client.post(url, data=json.dumps(data), content_type='application/json') 
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['id'] == test_user.id
    assert response_data['nome'] == test_user.nome
    assert client.session.get('usuario_id') == test_user.id

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


@pytest.mark.django_db
def test_listar_usuarios_view_vazia(client, admin_user): 
    session = client.session
    session['usuario_id'] = admin_user.id
    session.save()

    url = reverse('listar_usuarios')
    response = client.get(url)
    assert response.status_code == 200
    response_data = response.json()
    assert 'usuarios' in response_data
    assert isinstance(response_data['usuarios'], list)

@pytest.mark.django_db
def test_adicionar_usuario_view_sucesso(client, admin_user):
    session = client.session
    session['usuario_id'] = admin_user.id
    session.save()

    url = reverse('adicionar_usuario')
    user_data = {
        'nome': 'Novo Usuario View Teste',
        'email': 'novo.view.teste@example.com',
        'senha': 'novasenha123',
    }
    response = client.post(url, data=user_data)
    assert response.status_code == 201
    assert response.json().get('message') == 'Usuário adicionado com sucesso!' or \
           response.json().get('mensagem') == 'Usuário adicionado com sucesso!'
    assert Usuario.objects.filter(email='novo.view.teste@example.com').exists()

@pytest.mark.django_db
def test_editar_usuario_view_sucesso(client, admin_user, test_user):
    session = client.session
    session['usuario_id'] = admin_user.id
    session.save()

    url = reverse('editar_usuario', kwargs={'usuario_id': test_user.id})
    update_data = {
        'nome': 'Usuario Comum Editado Pela View',
        'email': 'comum.editado.view@example.com',
    }
    response = client.put(url, data=update_data) 
    assert response.status_code == 200
    assert response.json().get('message') == 'Usuário atualizado com sucesso!' or \
           response.json().get('mensagem') == 'Usuário atualizado com sucesso!'
    test_user.refresh_from_db()
    assert test_user.nome == 'Usuario Comum Editado Pela View'
    assert test_user.email == 'comum.editado.view@example.com'

@pytest.mark.django_db
def test_excluir_usuario_view_sucesso(client, admin_user, test_user):
    session = client.session
    session['usuario_id'] = admin_user.id
    session.save()

    url = reverse('excluir_usuario', kwargs={'usuario_id': test_user.id})
    response = client.delete(url)
    assert response.status_code == 200
    assert response.json().get('message') == 'Usuário excluído com sucesso!' or \
           response.json().get('mensagem') == 'Usuário excluído com sucesso!'
    assert not Usuario.objects.filter(id=test_user.id).exists()


@pytest.mark.django_db
def test_adicionar_camera_view_sucesso(client, test_user):

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
    assert response.status_code == 500
    assert response.json()['error'].startswith('Erro ao adicionar câmera:')

@pytest.mark.django_db
def test_editar_camera_view_sucesso(client, test_user, test_camera):

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
    url = reverse('editar_camera', kwargs={'camera_id': 99999})
    dados_atualizados = {
        'nome': 'Tentativa Edicao Inexistente View',
        'usuario_id': str(test_user.id)
    }
    response = client.put(url, data=dados_atualizados)
    assert response.status_code == 404
    assert response.json() == {'error': 'Câmera não encontrada'}

@pytest.mark.django_db
def test_excluir_camera_view_sucesso(client, test_user, test_camera):

    url = reverse('excluir_camera', kwargs={'camera_id': test_camera.id})
    response = client.delete(url)
    assert response.status_code == 200
    assert response.json().get('message') == 'Câmera excluída com sucesso!' or \
           response.json().get('mensagem') == 'Câmera excluída com sucesso!'
    assert not Camera.objects.filter(id=test_camera.id).exists()

@pytest.mark.django_db
def test_listar_cameras_view_com_cameras_existentes(client, test_user, test_camera):
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
    Camera.objects.all().delete()
    url = reverse('listar_cameras')
    response = client.get(url)
    assert response.status_code == 200
    response_data = response.json()
    assert 'cameras' in response_data
    assert response_data['cameras'] == []




  