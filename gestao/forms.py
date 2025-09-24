from django import forms
from .models import Loja, Produto, Cliente, Fornecedor, Venda, Despesa, PerfilUsuario
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm

class LojaForm(forms.ModelForm):
    class Meta:
        model = Loja
        fields = ['nome', 'endereco']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'preco_compra', 'preco_venda', 'estoque']

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'email', 'telefone', 'endereco', 'loja']

class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        fields = ['nome', 'email', 'telefone', 'cnpj', 'endereco']

class VendaForm(forms.ModelForm):
    class Meta:
        model = Venda
        fields = ['produto', 'cliente', 'quantidade']
        widgets = {
            'quantidade': forms.NumberInput(attrs={'min': 1}),
            'preco_unitario': forms.NumberInput(attrs={'step': '0.01'}),
        }

class DespesaForm(forms.ModelForm):
    class Meta:
        model = Despesa
        fields = ['descricao','valor', 'categoria', 'observacoes']
        widgets = {
            'descricao': forms.TextInput(attrs={'placeholder': 'Descrição da despesa'}),
            'valor': forms.NumberInput(attrs={'step': '0.01'}),
            'categoria': forms.TextInput(attrs={'categoria': 'Categoria da Despesa'}),
            'observacoes': forms.Textarea(attrs={'rows': 3, 'placeholders': 'Observações'}),
        }

class FiltroRelatorioForm(forms.Form):
    data_inicio = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
        )
    data_fim = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.all(),
        required=False,
        empty_label="Todos os clientes"
    )
    produto = forms.ModelChoiceField(
        queryset=Produto.objects.all(),
        required=False,
        empty_label="Todos os produtos"
    )


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'E-mail',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class PerfilUsuarioForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = ['telefone', 'endereco']
        widgets = {
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CustomPasswordChangeForm(PasswordChangeForm):
    
    old_password = forms.CharField(
        label = "Senha atual",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
        )
    new_password1 = forms.CharField(
        label = "Nova senha",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
        )
    new_password2 = forms.CharField(
        label = "Confirme a nova senha",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
        )

