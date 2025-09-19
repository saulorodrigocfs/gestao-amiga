from django import forms
from .models import Loja, Produto, Cliente, Fornecedor, Venda, Despesa

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
        fields = ['produto', 'quantidade', 'preco_unitario']
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
