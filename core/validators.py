import re
from django.contrib.auth.models import User

from .models import Pessoa

# Valida os campos antes da pessoa se cadastrar
class Validator:
    @staticmethod
    def cpf(cpf):
        cpf = re.sub(r'\D', '', cpf)
        if len(cpf) != 11 or cpf == cpf[0] * 11:
            return False
        for i in range(9, 11):
            soma = sum(int(cpf[num]) * ((i + 1) - num) for num in range(i))
            digito = (soma * 10 % 11) % 10
            if digito != int(cpf[i]):
                return False
        return True

    # Validador de senha
    @staticmethod
    def senha(password):
        regras = [
            (len(password) >= 4, "A senha deve ter pelo menos 4 caracteres."),
            (re.search(r"[A-Z]", password), "A senha deve conter pelo menos uma letra maiúscula."),
            (re.search(r"[a-z]", password), "A senha deve conter pelo menos uma letra minúscula."),
            (re.search(r"[!@#$%^&*(),.?\":{}|<>*\-_\[\]\\\/]", password), "A senha deve conter pelo menos um caractere especial.")
        ]
        for ok, msg in regras:
            if not ok:
                return msg
        return None

    # Validador de CPF, verifica se o cpf já existe em outro login
    @staticmethod
    def cpf_existente(cpf):
        return Pessoa.objects.filter(cpf=cpf).exists()

    # Validador de USUÁRIO, verifica se o usuário já existe em outro login
    @staticmethod
    def usuario_existente(username):
        return User.objects.filter(username=username).exists()

    # Validador de nome (Não utilizado no momento)
    # @staticmethod
    # def nome_igual_usuario(nome, username):
    #     return nome.strip().lower() == username.strip().lower()