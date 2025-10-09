from django.views.generic import FormView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView

from .models import Pessoa, Banco, GastoMensal
from .forms import GastoForm, PessoaForm

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

        # Cria o usuário
        user = User.objects.create_user(username=username, password=password)
        user.save()

        # Cria a Pessoa VINCULADA ao usuário
        pessoa = Pessoa.objects.create(
            user=user,
            cpf=cpf,
            nome=nome,
            sexo=sexo,
            data_nascimento=data_nascimento
        )

        # Login automático
        login(request, user)

        return redirect('cadastro_gastos')

    return render(request, 'cadastro_usuario.html')

# Edição de perfil do funcionário
class EditarPerfilView(LoginRequiredMixin, UpdateView):
    model = Pessoa
    form_class = PessoaForm
    template_name = 'editar_perfil.html'
    success_url = reverse_lazy('editar_perfil')

    def get_object(self, queryset=None):
        user = self.request.user
        try:
            return user.pessoa
        except Pessoa.DoesNotExist:
            pessoa = Pessoa.objects.create(
                user=user,
                nome=user.username or "Novo usuário",
                sexo='Outro',
                data_nascimento=None
            )
            return pessoa

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.request.user.username  # 👈 manda o nome de usuário pro template
        return context

    def form_valid(self, form):
        messages.success(self.request, "Seus dados foram atualizados com sucesso!")
        return super().form_valid(form)

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