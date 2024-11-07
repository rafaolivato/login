# models.py (app autenticacao)
from django.db import models
from django.contrib.auth.models import User

class Estabelecimento(models.Model):
    nome = models.CharField(max_length=100)
    endereco = models.CharField(max_length=200)
    

    def __str__(self):
        return self.nome

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    estabelecimento = models.ForeignKey(Estabelecimento, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.user.username} - {self.estabelecimento if self.estabelecimento else "Sem Estabelecimento"}'


