from django.urls import path
from .token import CustomLoginView
from .views import (api_home, api_login, adicionar_usuario, adicionar_camera, excluir_usuario, excluir_camera, listar_cameras, 
                    listar_usuarios, editar_camera, editar_usuario)

urlpatterns = [
    path("api/", api_home, name="api_home"),
    path("login/", api_login, name="api_login"),
    path("usuarios/", listar_usuarios, name="listar_usuarios"),
    path("cameras/", listar_cameras, name="listar_cameras"),
    path("usuarios/adicionar/", adicionar_usuario, name="adicionar_usuario"),
    path("cameras/adicionar/", adicionar_camera, name="adicionar_camera"),
    path("usuarios/excluir/<int:id>/", excluir_usuario, name="excluir_usuario"),
    path("cameras/excluir/<int:id>/", excluir_camera, name="excluir_camera"),
    path("usuarios/<int:usuario_id>/editar/", editar_usuario, name="editar_usuario"),
    path("cameras/<int:camera_id>/editar/", editar_camera, name="editar_camera"),
    path("login/", CustomLoginView.as_view(), name="token_login"),
]
