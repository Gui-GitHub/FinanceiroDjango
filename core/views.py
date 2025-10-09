from django.views.generic import FormView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Pessoa, Banco, GastoMensal
from .forms import GastoForm

# Tela inicial (Index)
class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # informações resumidas, como número de pessoas cadastradas E bancos
        context['total_pessoas'] = Pessoa.objects.count()
        context['total_bancos'] = Banco.objects.count()
        return context

# Função para cadastrar o usuário no sistema
def cadastro_usuario(request):
    if request.method == 'POST':
        cpf = request.POST['cpf']
        nome = request.POST['nome']
        sexo = request.POST['sexo']
        data_nascimento = request.POST['data_nascimento']
        username = request.POST['username']
        password = request.POST['password']

        # Evita duplicidade de usernames
        if User.objects.filter(username=username).exists():
            return render(request, 'cadastro_usuario.html', {'erro': 'Usuário já existe.'})

        # Cria o usuário com hash automático da senha
        user = User.objects.create_user(username=username, password=password)
        user.save()

        # Cria o registro de Pessoa vinculado
        pessoa = Pessoa.objects.create(
            cpf=cpf,
            nome=nome,
            sexo=sexo,
            data_nascimento=data_nascimento
        )
        pessoa.save()

        # Faz login automático após cadastro
        login(request, user)

        return redirect('cadastro_gastos')

    return render(request, 'cadastro_usuario.html')

# Edição de perfil do funcionário
# def editar_perfil(request)

# Cadastrar seus gastos
class GastoCreateView(LoginRequiredMixin, FormView):
    template_name = 'cadastro_gasto.html'
    form_class = GastoForm
    success_url = reverse_lazy('relatorio')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bancos'] = Banco.objects.all()
        return context

    def form_valid(self, form):
        pessoa = self.request.user.pessoa
        gasto = form.save(commit=False)
        gasto.pessoa = pessoa
        gasto.save()
        messages.success(self.request, 'Gasto registrado com sucesso!')
        return super().form_valid(form)

# Relatório gerado
class RelatorioView(LoginRequiredMixin, TemplateView):
    template_name = 'relatorio.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pessoa = self.request.user.pessoa
        context['gastos'] = GastoMensal.objects.filter(pessoa=pessoa).order_by('mes')
        return context
    
# Definição de logout
def logout_view(request):
    logout(request)
    return redirect('login')