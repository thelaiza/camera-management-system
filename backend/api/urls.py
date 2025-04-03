from django.urls import path
from .views import api_home, api_login, adicionar_usuario, adicionar_camera

urlpatterns = [
    path("", api_home, name="api_home"),
    path("api/", api_home, name="api_home"),
    path("login/", api_login, name="api_login"),
    path("usuarios/adicionar/", adicionar_usuario, name="adicionar_usuario"),
    path("cameras/adicionar/", adicionar_camera, name="adicionar_camera"),
]
