<h1 align="center">FinanceiroDjango - Sistema de Gestão Financeira</h1>

<p align="center">
  <img width="1584" height="780" alt="image" src="https://github.com/user-attachments/assets/e6c8ec51-5960-4035-b8db-a167c19d6b1f" />
</p>

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Django](https://img.shields.io/badge/django-4.2-green)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-brightgreen)

---

## 📑 Descrição do Projeto

O **FinanceiroDjango** é um sistema completo de gestão financeira, desenvolvido em **Django**, com foco em organização de gastos, ganhos e geração de relatórios interativos. O projeto é estruturado para suportar **ETL**, **APIs**, testes automatizados e deploy na plataforma **Render**, utilizando **PostgreSQL** como banco de dados principal.

Acesse em `financeirodjango.onrender.com`

Objetivos principais:

- Centralizar o controle financeiro de usuários de forma simples e segura.
- Gerar relatórios visuais interativos usando **Charts.js**.
- Manter código organizado e testado com boas práticas de desenvolvimento.
- Garantir deploy seguro e escalável na nuvem.

Durante o desenvolvimento, foram implementadas melhorias como:

- Estrutura modular para maior organização de código.
- Uso de **.env** para variáveis sensíveis, como credenciais do banco.
- Banco de dados PostgreSQL configurado para produção.
- Funções de ETL para importar, processar e transformar dados financeiros.
- APIs REST para integração com sistemas externos.
- Testes automatizados para validação das funcionalidades.

---

## 🛠️ Funcionalidades Principais

- **Cadastro de Usuários**
  - Autenticação com senha segura
  - Controle de permissões
  - Alteração de dados incluindo senha

- **Gestão de Finanças**
  - Registro de **gastos** e **ganhos**
  - Edição, exclusão e visualização detalhada
  - Histórico de transações por usuário

- **Relatórios e Dashboards**
  - Gráficos interativos com **Charts.js**
  - Visualização de tendências de gastos e ganhos
  - Filtros por período, categoria e usuário
  - Exportação CSV

- **ETL Financeiro**
  - Importação e transformação de dados de fontes externas
  - Processamento de dados para relatórios e APIs

- **APIs REST**
  - Endpoints para consulta e envio de dados financeiros

- **Banco de Dados PostgreSQL**
  - Estrutura relacional para usuários, transações e relatórios
  - Conexão segura via **.env**
  - Migrações automáticas com Django

- **Testes Automatizados**
  - Cobertura de funcionalidades críticas
  - Testes unitários e de integração com **pytest**

- **Deploy na Render**
  - Ambiente configurado com variáveis de ambiente
  - Suporte a escalabilidade e segurança

- **Interface Web Amigável**
  - Templates Django modernos e responsivos
  - Navegação intuitiva e fácil para usuários finais

---

## 📥 Como clonar este projeto

Clone via **HTTPS**:
```bash
git clone https://github.com/SEU_USUARIO/FinanceiroDjango.git
```

Ou via **SSH**:
```bash
git clone git@github.com:SEU_USUARIO/FinanceiroDjango.git
```

Entre na pasta do projeto:
```bash
cd FinanceiroDjango
```

---

## 🖥 Como executar

### 1) Pré-requisitos
- **Python 3.10+**
  ```bash
  python --version
  ```
- **pip** atualizado
  ```bash
  python -m pip install --upgrade pip
  ```

### 2) Criar e ativar ambiente virtual
- **Windows**
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```
- **Linux/macOS**
  ```bash
  python -m venv venv
  source venv/bin/activate
  ```

### 3) Instalar dependências
```bash
pip install -r requirements.txt
```

### 4) Configurar variáveis de ambiente
Crie um arquivo `.env` com as seguintes informações mínimas:
```
DATABASE_URL= seudatabase
SECRET_KEY= senhadjango
DEBUG= true ou false
```

### 5) Executar migrações
```bash
python manage.py migrate
```

### 6) Rodar a aplicação
```bash
python manage.py runserver
```
Acesse em `http://127.0.0.1:8000/`

---

## 📸 Prints da Aplicação

<table>
  <tr>
    <td width="50%"><img src="https://github.com/user-attachments/assets/c1ab6a45-9a4a-474c-ae19-5f74ea1df253" width="100%"/></td>
    <td width="50%"><img src="https://github.com/user-attachments/assets/863e690c-2201-44b8-b046-2270cf8381bf" width="100%"/></td>
  </tr>
  <tr>
    <td align="center">Tela de Ganhos</td>
    <td align="center">Tela de Relatórios com Charts.js</td>
  </tr>
</table>

## 🧰 Tecnologias Utilizadas

- **Python 3.10+**
- **Django 4.2**
- **PostgreSQL** - banco de dados relacional
- **Charts.js** - gráficos interativos
- **APIs REST** - integração com outros sistemas
- **dotenv** - variáveis de ambiente
- **pytest / unittest** - testes automatizados
- **Render** - deploy da aplicação

---

## 📜 Licença

Este projeto está licenciado sob a **MIT License** - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

