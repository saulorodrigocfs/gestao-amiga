from django.urls import path
from . import views

urlpatterns = [
    path('painel-loja/', views.painel_loja, name='painel_loja'),
    path('loja/<int:loja_id>/dashboard/', views.dashboard_loja, name="dashboard_loja"),
    path('loja/<int:loja_id>/produtos/', views.lista_produtos, name="lista_produtos"),
    path('loja/<int:loja_id>/produto/cadastrar/', views.cadastro_produto, name="cadastro_produto"),
    path('loja/<int:loja_id>/produto/<int:produto_id>/editar/', views.editar_produto, name="editar_produto"),
    path('loja/<int:loja_id>/produto/<int:produto_id>/deletar/', views.deletar_produto, name="deletar_produto"),
    path('clientes/<int:loja_id>/', views.lista_clientes, name='lista_clientes'),
    path('clientes/<int:loja_id>/cadastrar/', views.cadastrar_cliente, name='cadastrar_cliente'),
    path('clientes/<int:loja_id>/editar/<int:pk>/', views.editar_cliente, name='editar_cliente'),
    path('clientes/<int:loja_id>/deletar/<int:pk>/', views.deletar_cliente, name='deletar_cliente'),
    path('loja/<int:loja_id>/fornecedor/cadastrar/', views.cadastro_fornecedor, name="cadastro_fornecedor"),
    path('loja/<int:loja_id>/venda/cadastrar/', views.cadastro_venda, name="cadastro_venda"),
]
