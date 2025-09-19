from django.shortcuts import render, redirect, get_object_or_404
from .models import Loja, Produto, Cliente, Fornecedor, Venda, Despesa
from .forms import LojaForm, ProdutoForm, ClienteForm, FornecedorForm, VendaForm, DespesaForm
from django.contrib.auth.decorators import login_required
from django.db.models import Sum


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
    #Total de receitas
    total_receitas = loja.vendas.aggregate(total=Sum('valor_total'))['total'] or 0
    #Total despesas
    total_despesas = Despesa.objects.filter(loja=loja).aggregate(total=Sum('valor'))['total'] or 0
    #Saldo Atual
    saldo_atual = total_receitas - total_despesas
    #Últimas vendas (3 mais recentes)
    ultimas_vendas = loja.vendas.order_by('-data')[:3]
    #Despesas recentes (3 mais recentes)
    despesas_recentes = Despesa.objects.filter(loja=loja).order_by('data')[:3]

    contexto = {
        'loja': loja,
        'total_receitas': total_receitas,
        'total_despesas': total_despesas,
        'saldo_atual': saldo_atual,
        'ultimas_vendas': ultimas_vendas,
        'despesas_recentes': despesas_recentes,
    }
    return render(request, 'dashboard_loja.html', contexto)


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
def lista_vendas(request, loja_id):
    vendas = Venda.objects.filter(loja_id=loja_id).select_related('produto')
    return render(request, 'financeiro/lista_vendas.html', {'vendas': vendas, 'loja_id': loja_id} )

@login_required
def cadastrar_venda(request, loja_id):
    if request.method == "POST":
        form = VendaForm(request.POST)
        if form.is_valid():
            venda = form.save(commit=False)
            venda.loja_id = loja_id
            venda.preco_unitario = venda.produto.preco_venda
            venda.save()
            #atualiza estoque produto
            produto = venda.produto
            produto.estoque -= venda.quantidade
            produto.save()
            return redirect('lista_vendas', loja_id=loja_id)
    else:
        form = VendaForm()
    return render(request, 'financeiro/cadastrar_venda.html', {'loja_id': loja_id, 'form': form})

@login_required
def editar_venda(request, loja_id, pk):
    venda = get_object_or_404(Venda, pk=pk, loja_id=loja_id)
    produto_antigo = venda.produto
    quantidade_antiga = venda.quantidade

    if request.method == "POST":
        form = VendaForm(request.POST, instance=venda)
        if form.is_valid():
            venda = form.save(commit=False)
            venda.loja_id = loja_id
            venda.save()

            produto_novo = venda.produto 
            quantidade_nova = venda.quantidade
            if produto_novo == produto_antigo:
                delta = quantidade_nova - quantidade_antiga
                produto_novo.estoque -= delta
                produto_novo.save()
            else:
                produto_antigo.estoque += quantidade_antiga
                produto_antigo.save()
                produto_novo.estoque -= quantidade_nova
                produto_novo.save()
            return redirect('lista_vendas', loja_id=loja_id)
    else:
        form = VendaForm(instance=venda)
    return render(request, 'financeiro/cadastrar_venda.html', {'loja_id': loja_id, 'form': form})

@login_required
def deletar_venda(request, loja_id, pk):
    venda = get_object_or_404(Venda, pk=pk, loja_id=loja_id)
    if request.method == "POST":
        produto = venda.produto
        produto.estoque += venda.quantidade
        produto.save()
        venda.delete()
        return redirect('lista_vendas', loja_id=loja_id)
    return render(request, 'financeiro/deletar_venda.html', {'venda': venda, 'loja_id': loja_id})


@login_required
def lista_despesas(request, loja_id):
    loja = get_object_or_404(Loja, id=loja_id)
    despesas = Despesa.objects.filter(loja=loja)
    return render(request, 'financeiro/lista_despesas.html', {'despesas': despesas, 'loja': loja})

@login_required
def cadastrar_despesa(request, loja_id):
    loja = get_object_or_404(Loja, id=loja_id)
    form = DespesaForm(request.POST or None)
    if form.is_valid():
        despesa = form.save(commit=False)
        despesa.loja = loja
        despesa.save()
        return redirect('lista_despesas', loja_id=loja.id)
    return render(request, 'financeiro/cadastrar_despesa.html', {'form': form, 'loja': loja})

@login_required
def editar_despesa(request, loja_id , id):
    loja = get_object_or_404(Loja, id=loja_id)
    despesa = get_object_or_404(Despesa, id=id, loja=loja)
    form = DespesaForm(request.POST or None, instance=despesa)
    if form.is_valid():
        form.save()
        return redirect('lista_despesas', loja_id=loja.id)
    return render(request, 'financeiro/cadastrar_despesa.html', {'form': form, 'loja': loja})

@login_required
def deletar_despesa(request, loja_id, id):
    loja = get_object_or_404(Loja, id=loja_id)
    despesa = get_object_or_404(Despesa, id=id, loja=loja)
    if request.method == "POST":
        despesa.delete()
        return redirect('lista_despesas', loja_id=loja.id)
    return render(request, 'financeiro/deletar_despesa.html', {'despesa': despesa, 'loja': loja})


@login_required
def relatorio_lucros(request, loja_id):
    user = request.user
    loja = user.lojas.get(id=loja_id)
    produtos = loja.produtos.all()
    relatorio = []

    for produto in produtos:
        vendas_produto = produto.vendas_produto.all()
        total_quantidade = sum(v.quantidade for v in vendas_produto)
        total_receita = sum(v.preco_unitario * v.quantidade for v in vendas_produto)
        total_custo = sum(produto.preco_compra * v.quantidade for v in vendas_produto)
        lucro = total_receita - total_custo

        relatorio.append({
            'produto': produto.nome,
            'quantidade_vendida': total_quantidade,
            'total_receita': total_receita,
            'total_custo': total_custo,
            'lucro': lucro,
        })
    return render(request, 'financeiro/relatorio_lucros.html', {'loja': loja, 'relatorio': relatorio})
