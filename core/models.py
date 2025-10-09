from django.db import models
from django.contrib.auth.models import User

# Classe padrão na criação
class Base(models.Model):
    criados = models.DateField('Criação', auto_now_add=True)
    modificado = models.DateField('Atualização', auto_now=True)
    ativo = models.BooleanField('Ativo?', default=True)

    class Meta:
        abstract = True

# Campo da Pessoa
class Pessoa(Base):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='pessoa', null=True, blank=True)
    cpf = models.CharField('CPF', max_length=14, unique=True)
    nome = models.CharField('Nome', max_length=100)
    sexo = models.CharField('Sexo', max_length=20)
    data_nascimento = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = 'Pessoa'
        verbose_name_plural = 'Pessoas'

    def __str__(self):
        return self.nome

# Campo do banco
class Banco(Base):
    nome = models.CharField('Nome', max_length=100)
    descricao = models.TextField('Descrição', max_length=200, blank=True)

    class Meta:
        verbose_name = 'Banco'
        verbose_name_plural = 'Bancos'

    def __str__(self):
        return self.servico
    
# Gastos Mensais
class GastoMensal(Base):
    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE, related_name='gastos')
    banco = models.ForeignKey(Banco, on_delete=models.CASCADE, related_name='gastos')
    mes = models.DateField('Mês e Ano')  # Podemos usar o dia 1 do mês para simplificar
    valor = models.DecimalField('Valor gasto', max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Gasto Mensal'
        verbose_name_plural = 'Gastos Mensais'
        ordering = ['mes']

    def __str__(self):
        return f'{self.pessoa.nome} - {self.banco.nome} - {self.mes.strftime("%m/%Y")}: {self.valor}'