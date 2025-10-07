from django.db import models

import uuid
from django.db import models

# Classe padrão na criação
class Base(models.Model):
    criados = models.DateField('Criação', auto_now_add=True)
    modificado = models.DateField('Atualização', auto_now=True)
    ativo = models.BooleanField('Ativo?', default=True)

    class Meta:
        abstract = True

# Campo da Pessoa
class Pessoa(Base):
    nome = models.CharField('Nome', max_length=100)
    sexo = models.CharField('Facebook')
    data_nascimento = models.DateField('Data de nascimento')

    class Meta:
        verbose_name = 'Pessoa'
        verbose_name_plural = 'Pessoas'

    def __str__(self):
        return self.nome

# Campo do banco
class Banco(Base):
    nome = models.CharField('Nome', max_length=100)
    descricao = models.TextField('Descrição', max_length=200)

    class Meta:
        verbose_name = 'Banco'
        verbose_name_plural = 'Bancos'

    def __str__(self):
        return self.servico