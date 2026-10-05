# 🛡️ APS — Segurança da Informação em Sistema Web para Registros Emergéticos

Protótipo de sistema web desenvolvido para a **Atividade Prática Supervisionada (APS)** do curso de **Sistemas de Informação**, na disciplina de **Segurança da Informação**.

O projeto foi inspirado no contexto do software **SCALE**, com foco no registro e consulta de dados emergéticos e na aplicação prática de mecanismos de **segurança, autenticação, controle de acesso e mitigação de vulnerabilidades**.

## 📌 Sobre o projeto

O sistema funciona como uma aplicação web de **login e gerenciamento de registros**, desenvolvida com **Python, Flask e SQLite**.

A proposta foi aplicar conceitos de Segurança da Informação diretamente no desenvolvimento da aplicação, buscando proteger credenciais, controlar o acesso às funcionalidades e reduzir riscos relacionados a vulnerabilidades comuns em sistemas web.

Entre os principais conceitos trabalhados estão:

* 🔐 Autenticação e proteção de senhas;
* 👥 Autorização e controle de acesso;
* 🛡️ Proteção contra SQL Injection;
* 🚫 Mitigação de ataques de força bruta;
* ⏱️ Limitação de requisições por endereço IP;
* 📋 Registro e monitoramento de atividades;
* ⚠️ Tratamento seguro de exceções;
* 🧪 Testes e validação dos mecanismos de segurança.

## 🔒 Mecanismos de segurança implementados

### 🔑 Autenticação e proteção de senhas

As credenciais dos usuários são protegidas utilizando **hash de senha**, por meio de **Bcrypt/Werkzeug**, evitando o armazenamento das senhas em texto puro.

### 👤 Controle de acesso — RBAC

O sistema utiliza diferentes níveis de acesso para **usuários comuns e administradores**, protegendo rotas e funcionalidades de acordo com o papel do usuário autenticado.

### 💉 Proteção contra SQL Injection

As consultas ao banco de dados utilizam **queries parametrizadas (Prepared Statements)**, reduzindo o risco de injeção de comandos SQL por meio de entradas fornecidas pelo usuário.

### 🚨 Mitigação de força bruta

O sistema possui mecanismos de controle de tentativas de login para dificultar ataques de força bruta contra as credenciais dos usuários.

### ⏱️ Rate Limiting

Rotas críticas, como a de login, possuem **limitação básica de requisições por endereço IP**, reduzindo a possibilidade de abuso por excesso de solicitações.

### 📋 Auditoria e logs

As principais ações realizadas no sistema são registradas em **logs**, permitindo maior rastreabilidade e monitoramento das atividades.

### ⚠️ Tratamento de exceções

O sistema possui tratamento de erros para evitar a exposição de informações sensíveis, como detalhes internos da aplicação e *stack traces*.

## 🛠️ Tecnologias utilizadas

* 🐍 **Python 3**
* 🌐 **Flask**
* 🗄️ **SQLite**
* 🧱 **HTML5**
* 🎨 **CSS**
* 🔐 **Bcrypt/Werkzeug**

## 📁 Estrutura do projeto

```text
aps-seguranca/
│
├── app.py                # Rotas, controladores e mecanismos de segurança
├── database.py           # Conexão, tabelas e queries parametrizadas
├── login_service.py      # Autenticação, hashing e controle de tentativas
├── requirements.txt      # Dependências do projeto
├── README.md             # Documentação do projeto
│
└── templates/            # Interfaces HTML
    ├── login.html
    ├── dashboard.html
    ├── admin.html
    ├── registros.html
    └── acesso_negado.html
```

## 🚀 Como executar

### 1. Clone o repositório

```bash
git clone https://github.com/christopherbmagalhaes-coder/Criptografia-de-registros-.git
```

### 2. Acesse a pasta do projeto

```bash
cd Criptografia-de-registros-
```

### 3. Crie um ambiente virtual

```bash
python -m venv venv
```

### 4. Ative o ambiente virtual

**Windows:**

```bash
venv\Scripts\activate
```

**Linux/macOS:**

```bash
source venv/bin/activate
```

### 5. Instale as dependências

```bash
pip install -r requirements.txt
```

### 6. Execute a aplicação

```bash
python app.py
```

Depois, acesse a aplicação pelo navegador no endereço disponibilizado pelo Flask.

## 🎓 Objetivo acadêmico

O projeto teve como objetivo colocar em prática conceitos de **Segurança da Informação aplicados ao desenvolvimento de sistemas web**, demonstrando como mecanismos de proteção podem ser incorporados à estrutura de uma aplicação.

A atividade permitiu trabalhar conceitos relacionados a **autenticação, autorização, proteção de credenciais, segurança de banco de dados, controle de requisições, logs e tratamento de erros**.

## 👥 Integrantes

* **Christopher Bruno Magalhães**
* **Leonardo Souza**
* **Anderson**

