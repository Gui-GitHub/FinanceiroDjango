
from django.contrib.auth.password_validation import validate_password
from datetime import datetime
from decimal import Decimal
from django import forms

from .models import Pessoa, GastoMensal, GanhoMensal

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

# Formulário para a senha
class SenhaForm(forms.Form):
    password = forms.CharField(
        label="Senha Atual",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Digite sua senha atual'}),
        required=True
    )
    new_password = forms.CharField(
        label="Nova Senha",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Digite a nova senha'}),
        required=True,
        validators=[validate_password]
    )
    confirm_password = forms.CharField(
        label="Confirmar Nova Senha",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirme a nova senha'}),
        required=True
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("As senhas digitadas não coincidem.")
        return cleaned_data

# Formulário de Gastos Mensais
class GastoForm(forms.ModelForm):
    banco = forms.ChoiceField(
        choices=GastoMensal.BANCO_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    mes = forms.CharField(
        label='Mês',
        widget=forms.TextInput(attrs={'type': 'month', 'class': 'form-control'})
    )
    valor = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'valor'})
    )

    class Meta:
        model = GastoMensal
        fields = ['descricao', 'banco', 'mes', 'valor']
        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite a descrição'}),
        }

    def clean_valor(self):
        valor = self.cleaned_data['valor']

        if isinstance(valor, str):
            if ',' in valor:  # apenas se o usuário digitar com vírgula
                valor = valor.replace('.', '').replace(',', '.')

        try:
            return Decimal(valor)
        except:
            raise forms.ValidationError("Informe um número válido.")

    def clean_mes(self):
        mes = self.cleaned_data['mes']
        try:
            return datetime.strptime(mes + '-01', '%Y-%m-%d').date()
        except:
            raise forms.ValidationError("Informe uma data válida.")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.mes:
            self.initial['mes'] = self.instance.mes.strftime('%Y-%m')

# Formulário de Ganhos Mensais
class GanhoForm(forms.ModelForm):
    banco = forms.ChoiceField(
        choices=GanhoMensal.BANCO_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    mes = forms.CharField(
        label='Mês',
        widget=forms.TextInput(attrs={'type': 'month', 'class': 'form-control'})
    )
    valor = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'valor'})
    )

    class Meta:
        model = GanhoMensal
        fields = ['descricao', 'banco', 'mes', 'valor']
        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite a descrição'}),
        }

    def clean_valor(self):
        valor = self.cleaned_data['valor']
        if isinstance(valor, str):
            if ',' in valor:
                valor = valor.replace('.', '').replace(',', '.')
        try:
            return Decimal(valor)
        except:
            raise forms.ValidationError("Informe um número válido.")

    def clean_mes(self):
        mes = self.cleaned_data['mes']
        try:
            return datetime.strptime(mes + '-01', '%Y-%m-%d').date()
        except:
            raise forms.ValidationError("Informe uma data válida.")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.mes:
            self.initial['mes'] = self.instance.mes.strftime('%Y-%m')