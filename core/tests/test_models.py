from django.test import TestCase
from model_mommy import mommy

from core.models import Pessoa, GastoMensal, GanhoMensal

# Teste para Pessoa
class PessoaModelTest(TestCase):
    def test_str(self):
        # Mommy para criar dados ficticios
        pessoa = mommy.make(Pessoa, nome='João da Silva')
        self.assertEqual(str(pessoa), 'João da Silva')

# Teste para Gastos
class GastoMensalModelTest(TestCase):
    def test_str(self):
        # Mommy para criar dados ficticios
        pessoa = mommy.make(Pessoa, nome='Maria')
        gasto = mommy.make(GastoMensal, pessoa=pessoa, banco='Itau', valor=100.50)
        expected_str = f'{gasto.pessoa.nome} - Itau - {gasto.mes.strftime("%m/%Y")}: {gasto.valor}'
        self.assertEqual(str(gasto), expected_str)

# Teste para Ganhos
class GanhoMensalModelTest(TestCase):
    def test_str(self):
        # Mommy para criar dados ficticios
        pessoa = mommy.make(Pessoa, nome='Maria')
        ganho = mommy.make(GanhoMensal, pessoa=pessoa, banco='Nubank', valor=1500.00)
        expected_str = f'{ganho.pessoa.nome} - Nubank - {ganho.mes.strftime("%m/%Y")}: {ganho.valor}'
        self.assertEqual(str(ganho), expected_str)