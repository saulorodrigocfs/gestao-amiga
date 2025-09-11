from django.shortcuts import render, redirect
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
            return redirect('painel_loja') #atualiza a página
    else:
        form = LojaForm()
    return render(request, 'painel_loja.html', {'lojas': lojas, 'form': form})
