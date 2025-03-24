# Rotas específicas dessa API (tipo os routes do Express)

from django.urls import path
from .views import listar_cameras, listar_usuarios, home, api_login

urlpatterns = [
    path('cameras/', listar_cameras, name='listar_cameras'),
    path('usuarios/', listar_usuarios, name='listar_usuarios'),
    path("", home, name="home"),
    path("login/", api_login, name="api_login"),
]
