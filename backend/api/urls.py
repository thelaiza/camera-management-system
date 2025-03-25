from django.urls import path
from .views import listar_cameras, listar_usuarios, api_login, api_home

urlpatterns = [
    path('cameras/', listar_cameras, name='listar_cameras'),
    path('usuarios/', listar_usuarios, name='listar_usuarios'),
    path("login/", api_login, name="api_login"),
    path("api/", api_home, name="api_home"),
]
