from django.db import models

class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100, null=False)
    email = models.CharField(max_length=100, unique=True, null=False)
    senha = models.CharField(max_length=255, null=False)

    class Meta:
        managed = False  # ⚠️ Isso impede o Django de criar/modificar a tabela no banco
        db_table = "usuarios"

class Camera(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100, null=False)
    localizacao = models.CharField(max_length=150, null=False)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True),
    status = models.CharField(max_length=20, default='pendente')  


    class Meta:
        managed = False
        db_table = "cameras"

class LogTransacao(models.Model):
    id = models.AutoField(primary_key=True)
    acao = models.CharField(max_length=100, null=False)
    data_hora = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True)
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        managed = False
        db_table = "logs_transacoes"
