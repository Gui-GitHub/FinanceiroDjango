from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from core.models import Pessoa

# Testando Index
class IndexViewTest(TestCase):
    def test_index_view(self):
        # Checando a resposta http
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

# Testando Login
class LoginViewTest(TestCase):
    def test_login_get(self):
        # Checando a resposta http
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

# Testando cadastro de usuário
class CadastroUsuarioViewTest(TestCase):
    def test_cadastro_usuario_get(self):
        # Checando a resposta http
        response = self.client.get(reverse('cadastro_usuario'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cadastro_usuario.html')

# Testando a lista de gastos
class GastoListViewTest(TestCase):
    def setUp(self):
        # Criando dados para o teste (SetUp)
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.pessoa = Pessoa.objects.create(user=self.user, cpf='123.456.789-00', nome='Test', sexo='Outro')
        self.client.login(username='testuser', password='12345')

    def test_gasto_list_view(self):
        # Checando a resposta http
        response = self.client.get(reverse('meus_gastos'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'meus_gastos.html')