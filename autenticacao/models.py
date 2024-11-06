from django.db import models

class Estabelecimento(models.Model):
    nome = models.CharField(max_length=100)
    endereco = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.nome


# autenticacao/models.py

from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    estabelecimento = models.ForeignKey(
        Estabelecimento, null=True, blank=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.user.username

