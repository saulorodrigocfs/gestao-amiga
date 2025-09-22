from django.db import models
from django.contrib.auth.models import User
from django.conf import settings



#Perfil estendido usuário
class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    telefone = models.CharField(max_length=20, blank = True)
    endereco = models.CharField(max_length=200, blank = True)

    def __str__(self):
        return self.usuario.username
class Loja(models.Model):
    nome = models.CharField(max_length=100)
    endereco = models.CharField(max_length=200, blank=True)
    dono = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='lojas', on_delete=models.CASCADE)
    criada_em = models.DateTimeField(auto_now_add=True)  

#Produto do usuário/loja
class Produto(models.Model):
    loja = models.ForeignKey(Loja, related_name='produtos', on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    preco_compra = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    preco_venda = models.DecimalField(max_digits=8, decimal_places=2, default=1)
    estoque = models.IntegerField()

    def __str__(self):
        return self.nome
    
#Cliente que cada usuário vai cadastrar
class Cliente(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    loja = models.ForeignKey(Loja, on_delete=models.CASCADE, default=1)
    nome = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    telefone = models.CharField(max_length=20, blank = True, null=True)
    endereco = models.TextField(blank = True, null=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    total_compras = models.IntegerField(default=0)

    def __str__(self):
        return self.nome
    
class Fornecedor(models.Model):
    loja = models.ForeignKey(Loja, on_delete=models.CASCADE, related_name="fornecedores")
    nome = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    telefone = models.CharField(max_length=20, blank = True, null=True)
    cnpj = models.CharField(max_length=200, blank=True, null=True)
    endereco = models.TextField(blank = True, null=True)

    def __str__(self):
        return f"{self.nome} ({self.loja.nome})"
    
#Venda realizada
class Venda(models.Model):
    loja = models.ForeignKey(Loja, on_delete=models.CASCADE, related_name="vendas", default=1)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name="vendas_produto")
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="vendas_cliente", null = True)
    quantidade = models.PositiveIntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    data = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.valor_total = self.quantidade * self.preco_unitario
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.produto.nome} - {self.quantidade} unidades"

class Despesa(models.Model):
    loja = models.ForeignKey(Loja, on_delete=models.CASCADE)
    descricao = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField(auto_now_add=True)
    categoria = models.CharField(max_length=100, blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.descricao} - {self.valor} ({self.loja})"
    