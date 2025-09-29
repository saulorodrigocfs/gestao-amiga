import io
from datetime import datetime
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from django.views.decorators.csrf import csrf_exempt
from urllib.parse import parse_qs
from django.shortcuts import render, redirect, get_object_or_404
from .models import Loja, Produto, Cliente, Fornecedor, Venda, Despesa, PerfilUsuario
from .forms import LojaForm, ProdutoForm, ClienteForm, FornecedorForm, VendaForm, DespesaForm, FiltroRelatorioForm, UserForm, PerfilUsuarioForm, CustomPasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.db.models import Sum


@login_required
def painel_loja(request):
    user = request.user
    lojas = user.lojas.all() #lista de lojas do usuário

    contexto = {
        'lojas': lojas,
        'mostrar_sidebar': False,
    }
    return render(request, 'painel_loja.html', contexto)


@login_required
def cadastrar_loja(request):
    user = request.user
    if request.method == "POST":
        form = LojaForm(request.POST)
        if form.is_valid():
            nova_loja = form.save(commit=False)
            nova_loja.dono = user
            nova_loja.save()
            return redirect('painel_loja') #atualiza a página
    else:
        form = LojaForm()
    return render(request, 'cadastrar_loja.html', {'form': form})

@login_required
def editar_loja(request, pk):
    loja = get_object_or_404(Loja, pk=pk, dono=request.user)
    if request.method == "POST":
        form = LojaForm(request.POST, instance=loja)
        if form.is_valid():
            form.save()
            return redirect('painel_loja')
    else:
        form = LojaForm(instance=loja)
        return render(request, 'cadastrar_loja.html', {'form': form, 'loja': loja})

@login_required
def deletar_loja(request, pk):
    loja = get_object_or_404(Loja, pk=pk, dono=request.user)
    if request.method=="POST":
        loja.delete()
        return redirect('painel_loja')
    return render(request, 'deletar_loja.html', {'loja': loja})


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
        'mostrar_sidebar': True,
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
            
            #atualiza estoque produto
            produto = venda.produto
            produto.estoque -= venda.quantidade
            produto.save()
            if venda.forma_pagamento != 'credito_parcelado':
                venda.parcelas = 1
            venda.save()
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
    loja = request.user.lojas.get(id=loja_id)
    vendas = Venda.objects.filter(loja=loja)

    form = FiltroRelatorioForm(request.GET or None)
    if form.is_valid():
        data_inicio = form.cleaned_data.get('data_inicio')
        data_fim = form.cleaned_data.get('data_fim')
        cliente = form.cleaned_data.get('cliente')
        produto = form.cleaned_data.get('produto')

        if data_inicio:
            vendas = vendas.filter(data__date__gte=data_inicio)
        if data_fim:
            vendas = vendas.filter(data__date__lte=data_fim)
        if cliente:
            vendas = vendas.filter(cliente=cliente)
        if produto:
            vendas = vendas.filter(produto=produto)
    
    relatorio = []

    for venda in vendas:
        relatorio.append({
            'produto': venda.produto.nome,
            'data': venda.data,
            'cliente': venda.cliente,
            'forma_pagamento': venda.forma_pagamento,
            'quantidade_vendida': venda.quantidade,
            'total_receita': venda.preco_unitario * venda.quantidade,
            'total_custo': venda.produto.preco_compra * venda.quantidade,
            'lucro': (venda.preco_unitario - venda.produto.preco_compra) * venda.quantidade,
        })
    
    
    return render(request, 'financeiro/relatorio_lucros.html', {
        'loja_id': loja_id, 'form': form, 'relatorio': relatorio
    })


@login_required
@csrf_exempt
def exportar_relatorio_pdf(request, loja_id):
    loja = request.user.lojas.get(id=loja_id)
    vendas = Venda.objects.filter(loja=loja)

    # Filtragem
    data_inicio = request.POST.get('data_inicio')
    data_fim = request.POST.get('data_fim')
    cliente_id = request.POST.get('cliente')
    produto_id = request.POST.get('produto')
    
    if data_inicio:
        data_inicio_obj = datetime.strptime(data_inicio, "%d-%m-%Y").date()
        vendas = vendas.filter(data_date_gte=data_inicio_obj)
    if data_fim:
        data_fim_obj = datetime.strptime(data_fim, "%d-%m-%Y").date()
        vendas = vendas.filter(data_date_lte=data_fim_obj)
    if cliente_id:
        cliente_obj = get_object_or_404(Cliente, id=int(cliente_id))
        vendas = vendas.filter(cliente=cliente_obj)
    if produto_id:
        produto_obj = get_object_or_404(Produto, id=int(produto_id))
        vendas = vendas.filter(produto=produto_obj)

    # Criando PDF em horizontal
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=landscape(A4))
    largura, altura = landscape(A4)

    y = altura - 50
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, f"Relatório de Lucros - Loja: {loja.nome}")
    y -= 30

    # Cabeçalho
    p.setFont("Helvetica-Bold", 10)
    colunas = [
        ("Produto", 50, "left"),
        ("Data", 200, "left"),
        ("Cliente", 300, "left"),
        ("Qtd", 450, "right"),
        ("Receita", 500, "right"),
        ("Custo", 570, "right"),
        ("Lucro", 640, "right")
    ]
    for titulo, x, align in colunas:
        if align == "left":
            p.drawString(x, y, titulo)
        else:
            p.drawRightString(x, y, titulo)
    y -= 20
    p.setFont("Helvetica", 10)

    # Conteúdo
    for venda in vendas:
        dados = [
            (venda.produto.nome, 50, "left"),
            (venda.data.strftime("%d/%m/%Y"), 200, "left"),
            (str(venda.cliente), 300, "left"),
            (str(venda.quantidade), 450, "right"),
            (f"{venda.preco_unitario * venda.quantidade:.2f}", 500, "right"),
            (f"{venda.produto.preco_compra * venda.quantidade:.2f}", 570, "right"),
            (f"{(venda.preco_unitario - venda.produto.preco_compra) * venda.quantidade:.2f}", 640, "right")
        ]
        for valor, x, align in dados:
            if align == "left":
                p.drawString(x, y, valor)
            else:
                p.drawRightString(x, y, valor)
        y -= 20

        # Nova página se necessário
        if y < 50:
            p.showPage()
            y = altura - 50
            p.setFont("Helvetica-Bold", 10)
            for titulo, x, align in colunas:
                if align == "left":
                    p.drawString(x, y, titulo)
                else:
                    p.drawRightString(x, y, titulo)
            y -= 20
            p.setFont("Helvetica", 10)

    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='relatorio_lucros.pdf')


@login_required
def perfil_usuario(request):
    perfil, created = PerfilUsuario.objects.get_or_create(usuario=request.user)

    if request.method=="POST":
        user_form = UserForm(request.POST, instance=request.user)
        perfil_form = PerfilUsuarioForm(request.POST, instance=perfil)
        if user_form.is_valid() and perfil_form.is_valid():
            user_form.save()
            perfil_form.save()
            messages.success(request, "Perfil atualizado com sucesso!")
            return redirect('perfil_usuario')
    else:
        user_form = UserForm(instance=request.user)
        perfil_form = PerfilUsuarioForm(instance=perfil)

    return render(request, 'perfil_usuario.html', {
        'user_form': user_form,
        'perfil_form': perfil_form,
    })

@login_required
def alterar_senha(request):
    if request.method=="POST":
        form = CustomPasswordChangeForm(user = request.user, data = request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Senha alterada com sucesso!")
            return redirect('perfil_usuario')
    else:
        form = CustomPasswordChangeForm(user=request.user)
    return render(request, 'alterar_senha.html', {'form': form})
