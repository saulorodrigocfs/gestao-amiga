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
    path('<int:loja_id>/fornecedores/', views.lista_fornecedores, name="lista_fornecedores"),
    path('<int:loja_id>/fornecedores/novo/', views.cadastrar_fornecedor, name="cadastrar_fornecedor"),
    path('<int:loja_id>/fornecedores/<int:pk>/editar/', views.editar_fornecedor, name="editar_fornecedor"),
    path('<int:loja_id>/fornecedores/<int:pk>/deletar/', views.deletar_fornecedor, name="deletar_fornecedor"),
    path('<int:loja_id>/vendas/', views.lista_vendas, name="lista_vendas"),
    path('<int:loja_id>/vendas/novo/', views.cadastrar_venda, name="cadastrar_venda"),
    path('<int:loja_id>/vendas/<int:pk>/editar/', views.editar_venda, name="editar_venda"),
    path('<int:loja_id>/vendas/<int:pk>/deletar/', views.deletar_venda, name="deletar_venda"),
    path('<int:loja_id>despesas/', views.lista_despesas, name='lista_despesas'),
    path('<int:loja_id>despesas/cadastrar/', views.cadastrar_despesa, name='cadastrar_despesa'),
    path('<int:loja_id>despesas/editar/<int:id>/', views.editar_despesa, name='editar_despesa'),
    path('<int:loja_id>despesas/deletar/<int:id>/', views.deletar_despesa, name='deletar_despesa'),
    path('loja/<int:loja_id>/relatorio_lucros/', views.relatorio_lucros, name='relatorio_lucros'),
]
