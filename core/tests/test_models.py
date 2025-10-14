from django.test import TestCase
from model_mommy import mommy

from core.models import Pessoa, GastoMensal

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