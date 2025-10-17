from django.test import TestCase
from core.forms import PessoaForm, GastoForm, GanhoForm

# Teste formulário de usuário
class PessoaFormTest(TestCase):
    # Teste com dados válidos
    def test_valid_form(self):
        data = {
            'cpf': '123.456.789-00',
            'nome': 'Teste',
            'sexo': 'Masculino',
            'data_nascimento': '2000-01-01'
        }
        form = PessoaForm(data=data)
        self.assertTrue(form.is_valid())

    # Teste com dados inválidos
    def test_invalid_form(self):
        data = {
            'cpf': '',
            'nome': '',
            'sexo': '',
            'data_nascimento': ''
        }
        form = PessoaForm(data=data)
        self.assertFalse(form.is_valid())

# Teste formulário de gastos
class GastoFormTest(TestCase):
    # Teste com dados válidos
    def test_valid_form(self):
        data = {
            'descricao': 'Conta de luz',
            'banco': 'Itau',
            'mes': '2024-06',
            'valor': '123,45'
        }
        form = GastoForm(data=data)
        self.assertTrue(form.is_valid())
        
    # Teste com dados inválidos
    def test_invalid_valor(self):
        data = {
            'descricao': 'Conta de água',
            'banco': 'Itau',
            'mes': '2024-06',
            'valor': 'abc'
        }
        form = GastoForm(data=data)
        self.assertFalse(form.is_valid())

# Teste formulário de ganhos
class GanhoFormTest(TestCase):
    # Teste com dados válidos
    def test_valid_form(self):
        data = {
            'descricao': 'Salário',
            'banco': 'Nubank',
            'mes': '2024-06',
            'valor': '2500,00'
        }
        form = GanhoForm(data=data)
        self.assertTrue(form.is_valid())
        
    # Teste com dados inválidos
    def test_invalid_valor(self):
        data = {
            'descricao': 'Salário',
            'banco': 'Nubank',
            'mes': '2024-06',
            'valor': 'abc'
        }
        form = GanhoForm(data=data)
        self.assertFalse(form.is_valid())
