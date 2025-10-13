from django.contrib import admin

from .models import Pessoa, GastoMensal

# Ações para ativar/desativar
def ativar(modeladmin, request, queryset):
    queryset.update(ativo=True)
ativar.short_description = "Ativar selecionados"

def desativar(modeladmin, request, queryset):
    queryset.update(ativo=False)
desativar.short_description = "Desativar selecionados"

# Admin de Pessoa
@admin.register(Pessoa)
class PessoaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'sexo', 'data_nascimento', 'ativo', 'criados', 'modificado')
    list_display_links = ('nome', 'cpf')
    list_filter = ('sexo', 'ativo')
    search_fields = ('nome', 'cpf', 'user__username')
    ordering = ('nome',)
    readonly_fields = ('criados', 'modificado')
    actions = [ativar, desativar]

# Admin de Gastos Mensais
@admin.register(GastoMensal)
class GastoMensalAdmin(admin.ModelAdmin):
    list_display = ('pessoa_nome', 'banco', 'mes', 'valor', 'descricao', 'ativo', 'criados', 'modificado')
    list_display_links = ('pessoa_nome', 'mes')
    list_filter = ('banco', 'mes', 'ativo')
    search_fields = ('pessoa__nome', 'banco', 'descricao')
    ordering = ('-mes',)
    readonly_fields = ('criados', 'modificado')
    actions = [ativar, desativar]

    def pessoa_nome(self, obj):
        return obj.pessoa.nome
    pessoa_nome.short_description = 'Pessoa'