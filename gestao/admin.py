from django.contrib import admin
from .models import Cliente, PerfilUsuario, Produto, Venda #importa o modelo Cliente

#Registrar o modelo no admin
admin.site.register(Cliente) 
admin.site.register(PerfilUsuario)
admin.site.register(Produto)
admin.site.register(Venda)
