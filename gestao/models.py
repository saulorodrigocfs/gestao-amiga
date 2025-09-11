from django.db import models
from django.contrib.auth.models import User

#Cliente que cada usuário vai cadastrar
class Cliente(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    telefone = models.CharField(max_length=20, blank = True)
    endereco = models.CharField(max_length=200, blank = True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

#Perfil estendido usuário
class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    telefone = models.CharField(max_length=20, blank = True)
    endereco = models.CharField(max_length=200, blank = True)

    def __str__(self):
        return self.usuario.username
    
#Produto do usuário/loja
class Produto(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    estoque = models.IntegerField(default=0)

    def __str__(self):
        return self.nome
    
#Venda realizada
class Venda(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.produto.nome} - {self.quantidade}"

class Loja(models.Model):
    nome = models.CharField(max_length=100)
    endereco = models.CharField(max_length=200, blank=True)
    dono = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lojas')
    criada_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome
    