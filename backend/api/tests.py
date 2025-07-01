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
    user = Usuario.objects.create(
        nome='Admin Teste API',
        email='admintest@example.com',
        senha='adminpassword',
    )
    return user

@pytest.fixture
def test_camera(db, test_user):
    camera = Camera.objects.create(
        nome='Camera Fixture Original',
        localizacao='Local Original Fixture',
        status='ativa',
        usuario=test_user
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
    assert response.json()['status'] == 'sucesso'

@pytest.mark.django_db
def test_login_api_view_falha_senha_incorreta(client, test_user):
    url = reverse('api_login')
    data = {
        'email': test_user.email,
        'senha': 'senhaincorreta123'
    }
    response = client.post(url, data=json.dumps(data), content_type='application/json')
    assert response.status_code == 401
    assert response.json() == {"status": "erro", "mensagem": "Email ou senha inválidos"}

@pytest.mark.django_db
def test_login_api_view_falha_usuario_nao_existe(client):
    url = reverse('api_login')
    data = {
        'email': 'nao.existe.mesmo@example.com',
        'senha': 'qualquercoisa'
    }
    response = client.post(url, data=json.dumps(data), content_type='application/json')
    assert response.status_code == 401
    assert response.json() == {"status": "erro", "mensagem": "Email ou senha inválidos"}

@pytest.mark.django_db
def test_listar_usuarios_view_vazia(client):
    Usuario.objects.all().delete()
    url = reverse('listar_usuarios')
    response = client.get(url)
    assert response.status_code == 200
    assert response.json() == {'usuarios': []}

@pytest.mark.django_db
def test_adicionar_usuario_view_sucesso(client):
    url = reverse('adicionar_usuario')
    user_data = {
        'nome': 'Novo Usuario View Teste',
        'email': 'novo.view.teste@example.com',
        'senha': 'novasenha123',
    }
    response = client.post(url, data=user_data)
    assert response.status_code == 201
    assert Usuario.objects.filter(email='novo.view.teste@example.com').exists()

@pytest.mark.django_db
def test_editar_usuario_view_sucesso(client, test_user):
    url = reverse('editar_usuario', kwargs={'usuario_id': test_user.id})
    update_data = {
        'nome': 'Usuario Comum Editado Pela View',
        'email': 'comum.editado.view@example.com',
    }
    response = client.put(url, data=json.dumps(update_data), content_type='application/json')
    assert response.status_code == 200
    test_user.refresh_from_db()
    assert test_user.nome == 'Usuario Comum Editado Pela View'
    assert test_user.email == 'comum.editado.view@example.com'

@pytest.mark.django_db
def test_excluir_usuario_view_sucesso(client, test_user):
    url = reverse('excluir_usuario', kwargs={'id': test_user.id})
    response = client.delete(url)
    assert response.status_code == 200
    assert not Usuario.objects.filter(id=test_user.id).exists()

@pytest.mark.django_db
def test_adicionar_camera_view_sucesso(client, test_user):
    url = reverse('adicionar_camera')
    camera_data = {
        'nome': 'Camera Teste Hall Adicionada View',
        'localizacao': 'Hall de Entrada Principal View',
        'status': 'ativa',
        'usuario_id': str(test_user.id)
    }
    response = client.post(url, data=json.dumps(camera_data), content_type='application/json')
    assert response.status_code == 201
    assert response.json()['status'] == 'sucesso'

@pytest.mark.django_db
def test_adicionar_camera_view_metodo_get_nao_permitido(client):
    url = reverse('adicionar_camera')
    response = client.get(url)
    assert response.status_code == 405

@pytest.mark.django_db
def test_adicionar_camera_view_dados_faltando(client, test_user):
    url = reverse('adicionar_camera')
    camera_data_incompleta = {
        'localizacao': 'Local Sem Nome View',
        'usuario_id': str(test_user.id)
    }
    response = client.post(url, data=json.dumps(camera_data_incompleta), content_type='application/json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_editar_camera_view_sucesso(client, test_camera):
    url = reverse('editar_camera', kwargs={'camera_id': test_camera.id})
    dados_atualizados = {
        'nome': 'Camera Editada com Sucesso na View Teste',
        'status': 'manutencao',
    }
    response = client.put(url, data=json.dumps(dados_atualizados), content_type='application/json')
    assert response.status_code == 200
    test_camera.refresh_from_db()
    assert test_camera.nome == 'Camera Editada com Sucesso na View Teste'

@pytest.mark.django_db
def test_editar_camera_view_camera_nao_existe(client, test_user):
    url = reverse('editar_camera', kwargs={'camera_id': 99999})
    dados_atualizados = {'nome': 'Inexistente'}
    response = client.put(url, data=json.dumps(dados_atualizados), content_type='application/json')
    assert response.status_code == 404

@pytest.mark.django_db
def test_excluir_camera_view_sucesso(client, test_camera):
    url = reverse('excluir_camera', kwargs={'id': test_camera.id})
    response = client.delete(url)
    assert response.status_code == 200
    assert not Camera.objects.filter(id=test_camera.id).exists()

@pytest.mark.django_db
def test_listar_cameras_view_com_cameras_existentes(client, test_camera):
    url = reverse('listar_cameras')
    response = client.get(url)
    assert response.status_code == 200
    response_data = response.json()
    assert 'cameras' in response_data
    assert len(response_data['cameras']) >= 1

@pytest.mark.django_db
def test_listar_cameras_view_sem_cameras(client):
    Camera.objects.all().delete()
    url = reverse('listar_cameras')
    response = client.get(url)
    assert response.status_code == 200
    response_data = response.json()
    assert 'cameras' in response_data
    assert response_data['cameras'] == []