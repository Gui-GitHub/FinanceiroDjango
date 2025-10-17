from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import update_session_auth_hash
from django.views.generic import FormView, TemplateView
from django.contrib.auth import authenticate, login
from django.views.generic.edit import UpdateView
from django.views.generic import ListView, View
from django.shortcuts import render, redirect
from django.utils.timezone import make_aware
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.contrib import messages
from datetime import datetime
import random
import json

from .forms import GastoForm, GanhoForm, PessoaForm, SenhaForm
from .models import Pessoa, GastoMensal, GanhoMensal
from .validators import Validator

# Tela inicial (Index)
class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # informações resumidas
        context['total_pessoas'] = Pessoa.objects.count()
        context['total_gastos'] = GastoMensal.objects.count()
        context['total_ganhos'] = GanhoMensal.objects.count()
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
            return redirect('index')

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
    
# Tela para editar a senha do usuário
class EditarSenhaView(LoginRequiredMixin, FormView):
    template_name = 'editar_senha.html'
    form_class = SenhaForm
    success_url = reverse_lazy('editar_senha')

    def form_valid(self, form):
        user = self.request.user
        current_password = form.cleaned_data.get('current_password')
        new_password = form.cleaned_data.get('new_password')

        if not user.check_password(current_password):
            form.add_error('current_password', 'Senha atual incorreta.')
            return self.form_invalid(form)

        user.set_password(new_password)
        user.save()

        # Mantém o usuário logado após trocar a senha
        update_session_auth_hash(self.request, user)

        messages.success(self.request, "Senha alterada com sucesso!")
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
    
# Gerar gastos aleatórios para testes
@login_required
def gerar_gastos_exemplo(request):
    pessoa = request.user.pessoa

    bancos = ['Itau', 'Bradesco', 'Santander', 'Nubank', 'Outro']
    gastos_gerados = []

    for _ in range(5):
        # Banco aleatório
        banco = random.choice(bancos)

        # Valor entre 500 e 3000 (R$)
        valor = round(random.uniform(500, 3000), 2)

        # Data aleatória entre 01/2025 e 12/2025
        mes_aleatorio = random.randint(1, 12)
        data = datetime(2025, mes_aleatorio, random.randint(1, 28))
        data = make_aware(data)

        gasto = GastoMensal.objects.create(
            pessoa=pessoa,
            descricao='Gasto Teste',
            banco=banco,
            mes=data,
            valor=valor
        )
        gastos_gerados.append(gasto)

    messages.success(request, f"{len(gastos_gerados)} gastos de exemplo foram adicionados com sucesso!")
    return redirect('meus_gastos')

# Função para deletar os gastos
@login_required
def excluir_todos_gastos(request):
    pessoa = request.user.pessoa
    total = GastoMensal.objects.filter(pessoa=pessoa).count()

    if total == 0:
        messages.info(request, "Você não possui gastos para excluir.")
    else:
        GastoMensal.objects.filter(pessoa=pessoa).delete()
        messages.success(request, f"Todos os {total} gastos foram excluídos com sucesso!")

    return redirect('meus_gastos')

# Relatório gerado
class RelatorioView(LoginRequiredMixin, TemplateView):
    template_name = 'relatorio.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pessoa = self.request.user.pessoa

        # Gastos, mandando para o js
        gastos_qs = GastoMensal.objects.filter(pessoa=pessoa).order_by('mes')
        gastos_list = [
            {
                'data': g.mes.strftime('%Y-%m-%d'),
                'banco': g.banco,
                'valor': float(g.valor),
                'descricao': g.descricao
            } for g in gastos_qs
        ]
        context['gastos_json'] = json.dumps(gastos_list)

        # Ganhos, mandando para o js
        ganhos_qs = GanhoMensal.objects.filter(pessoa=pessoa).order_by('mes')
        ganhos_list = [
            {
                'data': g.mes.strftime('%Y-%m-%d'),
                'banco': g.banco,
                'valor': float(g.valor),
                'descricao': g.descricao
            } for g in ganhos_qs
        ]
        context['ganhos_json'] = json.dumps(ganhos_list)

        return context

# Cadastrar ganhos
class GanhoCreateView(LoginRequiredMixin, FormView):
    template_name = 'cadastrar_ganho.html'
    form_class = GanhoForm
    success_url = reverse_lazy('meus_ganhos')

    def form_valid(self, form):
        ganho = form.save(commit=False)
        ganho.pessoa = self.request.user.pessoa
        ganho.save()
        messages.success(self.request, 'Ganho registrado com sucesso!')
        return super().form_valid(form)

# Listar ganhos do usuário
class GanhoListView(LoginRequiredMixin, ListView):
    model = GanhoMensal
    template_name = 'meus_ganhos.html'
    context_object_name = 'ganhos'

    def get_queryset(self):
        return GanhoMensal.objects.filter(pessoa=self.request.user.pessoa).order_by('-mes')

# Editar ganho existente
class GanhoUpdateView(LoginRequiredMixin, UpdateView):
    model = GanhoMensal
    form_class = GanhoForm
    template_name = 'editar_ganho.html'

    def get_queryset(self):
        return GanhoMensal.objects.filter(pessoa=self.request.user.pessoa)

    def get_success_url(self):
        messages.success(self.request, "Ganho atualizado com sucesso!")
        return reverse_lazy('meus_ganhos')

# Deletar um ganho
class GanhoDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        ganho = get_object_or_404(GanhoMensal, pk=pk, pessoa=request.user.pessoa)
        ganho.delete()
        messages.success(request, "Ganho excluído com sucesso!")
        return redirect('meus_ganhos')

# Gerar ganhos aleatórios para testes
@login_required
def gerar_ganhos_exemplo(request):
    pessoa = request.user.pessoa

    bancos = ['Itau', 'Bradesco', 'Santander', 'Nubank', 'Outro']
    ganhos_gerados = []

    for _ in range(5):
        banco = random.choice(bancos)
        valor = round(random.uniform(500, 3000), 2)
        mes_aleatorio = random.randint(1, 12)
        data = datetime(2025, mes_aleatorio, random.randint(1, 28))
        data = make_aware(data)

        ganho = GanhoMensal.objects.create(
            pessoa=pessoa,
            descricao='Ganho Teste',
            banco=banco,
            mes=data,
            valor=valor
        )
        ganhos_gerados.append(ganho)

    messages.success(request, f"{len(ganhos_gerados)} ganhos de exemplo foram adicionados com sucesso!")
    return redirect('meus_ganhos')

# Excluir todos os ganhos
@login_required
def excluir_todos_ganhos(request):
    pessoa = request.user.pessoa
    total = GanhoMensal.objects.filter(pessoa=pessoa).count()

    if total == 0:
        messages.info(request, "Você não possui ganhos para excluir.")
    else:
        GanhoMensal.objects.filter(pessoa=pessoa).delete()
        messages.success(request, f"Todos os {total} ganhos foram excluídos com sucesso!")

    return redirect('meus_ganhos')
    
# Definição de logout
def logout_view(request):
    logout(request)
    return redirect('login')