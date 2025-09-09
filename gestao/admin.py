from django.contrib import admin
from .models import Cliente #importa o modelo Cliente

admin.site.register(Cliente) #Registra o modelo no admin
