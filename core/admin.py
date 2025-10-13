from django.contrib import admin

from .models import Pessoa, Banco, GastoMensal

# Admin de Pessoa
@admin.register(Pessoa)
class PessoaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'sexo', 'data_nascimento', 'ativo', 'criados', 'modificado')
    list_filter = ('sexo', 'ativo')
    search_fields = ('nome',)
    ordering = ('nome',)

# Admin de Banco
@admin.register(Banco)
class BancoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao', 'ativo', 'criados', 'modificado')
    search_fields = ('nome',)
    ordering = ('nome',)

# Admin de Gastos Mensais
@admin.register(GastoMensal)
class GastoMensalAdmin(admin.ModelAdmin):
    list_display = ('pessoa', 'banco', 'mes', 'valor', 'ativo', 'criados', 'modificado')
    list_filter = ('banco', 'mes', 'ativo')
    search_fields = ('pessoa__nome', 'banco__nome')
    ordering = ('-mes',)