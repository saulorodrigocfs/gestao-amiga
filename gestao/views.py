from django.shortcuts import render, redirect, get_object_or_404
from .models import Loja, Produto, Cliente, Fornecedor
from .forms import LojaForm, ProdutoForm, ClienteForm, FornecedorForm
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
def lista_clientes(request, loja_id):
    clientes = Cliente.objects.filter(usuario=request.user, loja_id=loja_id)
    return render(request, 'financeiro/lista_clientes.html', {'clientes': clientes, 'loja_id': loja_id} )

@login_required
def cadastrar_cliente(request, loja_id):
    form = ClienteForm(request.POST or None)
    if form.is_valid():
        cliente = form.save(commit=False)
        cliente.usuario = request.user
        cliente.loja_id = loja_id
        cliente.save()
        return redirect('lista_clientes', loja_id=loja_id)
    return render(request, 'financeiro/cadastrar_cliente.html', {'loja_id': loja_id, 'form': form})

@login_required
def editar_cliente(request, loja_id, pk):
    cliente = get_object_or_404(Cliente, pk=pk, usuario=request.user, loja_id=loja_id)
    form = ClienteForm(request.POST or None, instance=cliente)
    if form.is_valid():
        form.save()
        return redirect('lista_clientes', loja_id=loja_id)
    return render(request, 'financeiro/cadastrar_cliente.html', {'loja_id': loja_id, 'form': form})

@login_required
def deletar_cliente(request, loja_id, pk):
    cliente = get_object_or_404(Cliente, pk=pk, usuario=request.user, loja_id=loja_id)
    cliente.delete()
    return redirect('lista_clientes', loja_id=loja_id)


@login_required
def lista_fornecedores(request, loja_id):
    fornecedores = Fornecedor.objects.filter(loja_id=loja_id)
    return render(request, 'financeiro/lista_fornecedores.html', {'fornecedores': fornecedores, 'loja_id': loja_id} )

@login_required
def cadastrar_fornecedor(request, loja_id):
    if request.method == "POST":
        form = FornecedorForm(request.POST)
        if form.is_valid():
            fornecedor = form.save(commit=False)
            fornecedor.loja_id = loja_id
            fornecedor.save()
            return redirect('lista_fornecedores', loja_id=loja_id)
    else:
        form = FornecedorForm()
    return render(request, 'financeiro/cadastrar_fornecedor.html', {'loja_id': loja_id, 'form': form})

@login_required
def editar_fornecedor(request, loja_id, pk):
    fornecedor = get_object_or_404(Fornecedor, pk=pk, loja_id=loja_id)
    if request.method == "POST":
        form = FornecedorForm(request.POST, instance=fornecedor)
        if form.is_valid():
            form.save()
            return redirect('lista_fornecedores', loja_id=loja_id)
    else:
        form = FornecedorForm(instance=fornecedor)
    return render(request, 'financeiro/cadastrar_fornecedor.html', {'loja_id': loja_id, 'form': form})

@login_required
def deletar_fornecedor(request, loja_id, pk):
    fornecedor = get_object_or_404(Fornecedor, pk=pk, loja_id=loja_id)
    if request.method == "POST":
        fornecedor.delete()
        return redirect('lista_fornecedores', loja_id=loja_id)
    return render(request, 'financeiro/deletar_fornecedor.html', {'fornecedor': fornecedor, 'loja_id': loja_id})


@login_required
def cadastro_venda(request, loja_id):
    return render(request, 'financeiro/cadastro_venda.html', {'loja_id': loja_id})
