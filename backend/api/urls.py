# Rotas específicas dessa API (tipo os routes do Express)

from django.urls import path
from . import views
from django.urls import path
from .views import home

urlpatterns = [
    path('cameras/', views.listar_cameras, name='listar_cameras'),
    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
]


urlpatterns = [
    path("", home, name="home"),  
]
