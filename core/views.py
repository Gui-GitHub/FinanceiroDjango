from django.views.generic import FormView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.views.generic import ListView, View
from django.shortcuts import redirect, get_object_or_404
from .models import GastoMensal

from .models import Pessoa, Banco, GastoMensal
from .forms import GastoForm, PessoaForm
from .validators import Validator

# Tela inicial (Index)
class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # informações resumidas, como número de pessoas cadastradas E bancos
        context['total_pessoas'] = Pessoa.objects.count()
        context['total_gastos'] = GastoMensal.objects.count()
        return context

# View de login
def login_view(request):
    if request.method == 'POST':
        post = request.POST
        dados = post.dict()  # Digitação do usuário

        username = post.get('username', '').strip()
        password = post.get('password', '').strip()

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')  # Redireciona
        else:
            erro = "Usuário ou senha incorretos."
            # Renderiza mas mantendo o nome digitado
            return render(request, 'login.html', {'erro': erro, 'dados': dados})

    # GET — exibe o formulário vazio
    return render(request, 'login.html')

# Função para cadastrar o usuário no sistema
def cadastro_usuario(request):
    if request.method == 'POST':
        post = request.POST
        dados = post.dict()  # Converte para QueryDict

        cpf = post.get('cpf', '').strip()
        nome = post.get('nome', '').strip()
        sexo = post.get('sexo', '').strip()
        data_nascimento = post.get('data_nascimento', '').strip()
        username = post.get('username', '').strip()
        password = post.get('password', '')

        # Validações
        if Validator.cpf_existente(cpf):
            erro = "Este CPF já está cadastrado."
        elif not Validator.cpf(cpf):
            erro = "CPF inválido. Verifique e tente novamente."
        elif Validator.usuario_existente(username):
            erro = "Usuário já existe."
        elif (msg := Validator.senha(password)):
            erro = msg
        else:
            user = User.objects.create_user(username=username, password=password)
            Pessoa.objects.create(
                user=user, cpf=cpf, nome=nome, sexo=sexo, data_nascimento=data_nascimento
            )
            login(request, user)
            return redirect('cadastro_gastos')

        # Erro, renderiza novamente mantendo os dados preenchidos
        return render(request, 'cadastro_usuario.html', {'erro': erro, 'dados': dados})

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
        context['username'] = self.request.user.username
        return context

    def form_valid(self, form):
        messages.success(self.request, "Seus dados foram atualizados com sucesso!")
        return super().form_valid(form)

# Cadastrar seus gastos
class GastoCreateView(LoginRequiredMixin, FormView):
    template_name = 'cadastro_gasto.html'
    form_class = GastoForm
    success_url = reverse_lazy('meus_gastos')

    def form_valid(self, form):
        gasto = form.save(commit=False)
        gasto.pessoa = self.request.user.pessoa
        gasto.save()
        messages.success(self.request, 'Gasto registrado com sucesso!')
        return super().form_valid(form)
    
# Listar todos os gastos do usuário logado
class GastoListView(LoginRequiredMixin, ListView):
    model = GastoMensal
    template_name = 'meus_gastos.html'
    context_object_name = 'gastos'

    # Filtro a listagem por mês
    def get_queryset(self):
        return GastoMensal.objects.filter(pessoa=self.request.user.pessoa).order_by('-mes')


# Editar gastos existente
class GastoUpdateView(LoginRequiredMixin, UpdateView):
    model = GastoMensal
    form_class = GastoForm
    template_name = 'editar_gasto.html'

    def get_queryset(self):
        # Garante que o usuário só pode editar os próprios gastos
        return GastoMensal.objects.filter(pessoa=self.request.user.pessoa)

    def get_success_url(self):
        # URL de retorno
        messages.success(self.request, "Gasto atualizado com sucesso!")
        return reverse_lazy('meus_gastos')
    
# Deletar algum cadastro
class GastoDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        gasto = get_object_or_404(GastoMensal, pk=pk, pessoa=request.user.pessoa)
        gasto.delete()
        messages.success(request, "Gasto excluído com sucesso!")
        return redirect('meus_gastos')

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