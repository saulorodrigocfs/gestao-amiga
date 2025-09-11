from django.urls import path
from . import views

urlpatterns = [
    path('painel-loja/', views.painel_loja, name='painel_loja'),
]
