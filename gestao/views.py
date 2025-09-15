from django.shortcuts import render, redirect, get_object_or_404
from .models import Loja
from .forms import LojaForm
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
