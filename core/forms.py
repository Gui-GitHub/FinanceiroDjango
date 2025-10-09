from django import forms
from .models import Pessoa, Banco, GastoMensal
from django.forms.widgets import SelectDateWidget

# Formulário de Pessoa
class PessoaForm(forms.ModelForm):
    class Meta:
        model = Pessoa
        fields = ['cpf', 'nome', 'sexo', 'data_nascimento']
        widgets = {
            'cpf': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly',
            }),
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome completo',
                'required': True,
            }),
            'sexo': forms.Select(choices=[
                ('', 'Selecione'),
                ('Masculino', 'Masculino'),
                ('Feminino', 'Feminino'),
                ('Outro', 'Outro'),
            ], attrs={
                'class': 'form-control',
                'required': True,
            }),
            'data_nascimento': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                    'required': True,
                }
            ),
        }
        input_formats = {
            'data_nascimento': ['%Y-%m-%d', '%d/%m/%Y']
        }

# Formulário de Gastos Mensais
class GastoForm(forms.ModelForm):
    class Meta:
        model = GastoMensal
        fields = ['banco', 'mes', 'valor']
        widgets = {
            'mes': forms.DateInput(attrs={'type': 'month'}),
        }