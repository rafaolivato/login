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

class Medicamento(models.Model):
    nome = models.CharField(max_length=100)
    quantidade = models.IntegerField()
    validade = models.DateField()
    estabelecimento = models.ForeignKey(Estabelecimento, on_delete=models.CASCADE)
    registrado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Usuário que registrou


    def __str__(self):
        return self.nome
    
   
from django.db import models
from django.contrib.auth import get_user_model
from .models import Medicamento, Estabelecimento

User = get_user_model()

class Transferencia(models.Model):
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE)
    origem = models.ForeignKey(Estabelecimento, related_name='transferencias_saida', on_delete=models.CASCADE)
    destino = models.ForeignKey(Estabelecimento, related_name='transferencias_entrada', on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    data_transferencia = models.DateTimeField(auto_now_add=True)
    registrado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'Transferência de {self.quantidade} {self.medicamento.nome} de {self.origem.nome} para {self.destino.nome}'

# ISSO É O QUE VAI INTERMEDIAR OS ESTOQUES DE DIFERENTES ESTABELECIMENTOS, GARANTE QUE CADA ESTABELECIMENTO TENHA SEU PRÓPRIO ESTOQUE
class Estoque(models.Model):
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE)
    estabelecimento = models.ForeignKey(Estabelecimento, on_delete=models.CASCADE)
    estoque = models.IntegerField()

    def __str__(self):
        return f"{self.medicamento.nome} - {self.estabelecimento.nome}"
