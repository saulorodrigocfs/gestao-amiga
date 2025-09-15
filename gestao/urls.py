from django.urls import path
from . import views

urlpatterns = [
    path('painel-loja/', views.painel_loja, name='painel_loja'),
    path('loja/<int:loja_id>/dashboard/', views.dashboard_loja, name="dashboard_loja"),
    path('loja/<int:loja_id>/produto/cadastrar/', views.cadastro_produto, name="cadastro_produto"),
    path('loja/<int:loja_id>/cliente/cadastrar/', views.cadastro_cliente, name="cadastro_cliente"),
    path('loja/<int:loja_id>/fornecedor/cadastrar/', views.cadastro_fornecedor, name="cadastro_fornecedor"),
    path('loja/<int:loja_id>/venda/cadastrar/', views.cadastro_venda, name="cadastro_venda"),
]
