from django.views.generic import FormView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages

from .models import Pessoa, Banco, GastoMensal
from .forms import PessoaForm, GastoForm

# Tela inicial (Index)
class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # informações resumidas, como número de pessoas cadastradas E bancos
        context['total_pessoas'] = Pessoa.objects.count()
        context['total_bancos'] = Banco.objects.count()
        return context

# Cadastro de Pessoa
class PessoaCreateView(FormView):
    template_name = 'cadastro_pessoa.html'
    form_class = PessoaForm
    success_url = reverse_lazy('cadastro_gastos')  # redireciona para a tela de gastos

    def form_valid(self, form):
        pessoa = form.save()
        messages.success(self.request, f'Cadastro de {pessoa.nome} realizado com sucesso!')
        self.request.session['pessoa_id'] = pessoa.id
        return super().form_valid(form)

# Registro de Gastos Mensais
class GastoCreateView(FormView):
    template_name = 'cadastro_gasto.html'
    form_class = GastoForm
    success_url = reverse_lazy('relatorio')  # redireciona para o relatório final

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pessoas'] = Pessoa.objects.all()  # adiciona todas as pessoas
        context['bancos'] = Banco.objects.all()    # adiciona todos os bancos
        return context

    def form_valid(self, form):
        pessoa_id = self.request.session.get('pessoa_id')
        if not pessoa_id:
            messages.error(self.request, 'Pessoa não encontrada. Cadastre primeiro.')
            return super().form_invalid(form)

        gasto = form.save(commit=False)
        gasto.pessoa_id = pessoa_id
        gasto.save()
        messages.success(self.request, 'Gasto registrado com sucesso!')
        return super().form_valid(form)

# Relatório em Charts.js
class RelatorioView(TemplateView):
    template_name = 'relatorio.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pessoa_id = self.request.session.get('pessoa_id')
        if pessoa_id:
            context['gastos'] = GastoMensal.objects.filter(pessoa_id=pessoa_id).order_by('mes')
        else:
            context['gastos'] = []
        return context