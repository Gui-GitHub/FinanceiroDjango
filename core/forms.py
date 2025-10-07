from django import forms
from .models import Pessoa, Banco, GastoMensal
from django.forms.widgets import SelectDateWidget

# Formulário de Pessoa
class PessoaForm(forms.ModelForm):
    class Meta:
        model = Pessoa
        fields = ['nome', 'sexo', 'data_nascimento']
        widgets = {
            'data_nascimento': SelectDateWidget(years=range(1900, 2020))
        }

# Formulário de Gastos Mensais
class GastoForm(forms.ModelForm):
    class Meta:
        model = GastoMensal
        fields = ['banco', 'mes', 'valor']
        widgets = {
            'mes': forms.DateInput(attrs={'type': 'month'}),
        }