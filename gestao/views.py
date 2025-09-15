from django.shortcuts import render, redirect, get_object_or_404
from .models import Loja, Produto
from .forms import LojaForm, ProdutoForm
from django.contrib.auth.decorators import login_required

@login_required
def painel_loja(request):
    user = request.user
    lojas = user.lojas.all() #lista de lojas do usuário

    if request.method == "POST":
        form = LojaForm(request.POST)
        if form.is_valid():
            nova_loja = form.save(commit=False)
            nova_loja.dono = user
            nova_loja.save()
            return redirect('dashboard_loja', pk=nova_loja.pk) #atualiza a página
    else:
        form = LojaForm()
    return render(request, 'painel_loja.html', {'lojas': lojas, 'form': form})

@login_required
def dashboard_loja(request, loja_id):
    user = request.user
    try:
        loja = user.lojas.get(id=loja_id)
    except Loja.DoesNotExist:
        return redirect('painel_loja')
    return render(request, 'dashboard_loja.html', {'loja': loja})

@login_required
def lista_produtos(request, loja_id):
    loja = get_object_or_404(Loja, id=loja_id, dono=request.user)
    produtos = loja.produtos.all()
    return render(request, 'produtos/lista_produtos.html', {'loja': loja, 'produtos': produtos} )

@login_required
def cadastro_produto(request, loja_id):
    loja = get_object_or_404(Loja, id=loja_id, dono=request.user)
    if request.method == "POST":
        form = ProdutoForm(request.POST)
        if form.is_valid():
            produto = form.save(commit=False)
            produto.loja = loja
            produto.save()
            return redirect('lista_produtos', loja_id=loja.id)
    else:
        form = ProdutoForm()

    return render(request, 'produtos/cadastro_produto.html', {'loja': loja, 'form': form})

@login_required
def editar_produto(request, loja_id, produto_id):
    loja = get_object_or_404(Loja, id=loja_id, dono=request.user)
    produto = get_object_or_404(Produto, id=produto_id, loja=loja)
    if request.method == "POST":
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('lista_produtos', loja_id=loja.id)
    else:
        form = ProdutoForm(instance=produto)
    return render(request, 'produtos/cadastro_produto.html', {'loja': loja, 'form': form, 'produto': produto})

@login_required
def deletar_produto(request, loja_id, produto_id):
    loja = get_object_or_404(Loja, id=loja_id, dono=request.user)
    produto = get_object_or_404(Produto, id=produto_id, loja=loja)
    produto.delete()
    return redirect('lista_produtos', loja_id=loja.id)

@login_required
def cadastro_cliente(request, loja_id):
    return render(request, 'financeiro/cadastro_cliente.html', {'loja_id': loja_id})

@login_required
def cadastro_fornecedor(request, loja_id):
    return render(request, 'financeiro/cadastro_fornecedor.html', {'loja_id': loja_id})

@login_required
def cadastro_venda(request, loja_id):
    return render(request, 'financeiro/cadastro_venda.html', {'loja_id': loja_id})
