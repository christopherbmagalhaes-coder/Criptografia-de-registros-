# APS — Segurança da Informação em Sistema Web para Registros Emergéticos

## 1. Sobre o projeto

Este projeto foi desenvolvido como Atividade Prática Supervisionada do curso de Sistemas de Informação, na disciplina de Segurança da Informação.

A proposta consiste no desenvolvimento de um protótipo de sistema web inspirado no contexto do software SCALE, voltado ao registro e consulta de dados emergéticos, com aplicação prática de mecanismos de Segurança da Informação.

O sistema tem como objetivo demonstrar conceitos de:

- autenticação;
- autorização;
- controle de acesso;
- proteção de senhas;
- proteção contra SQL Injection;
- mitigação de força bruta;
- limite básico de requisições por IP;
- monitoramento de atividades;
- registro de logs;
- testes e validação.

---

## 2. Tecnologias utilizadas

O sistema foi desenvolvido utilizando:

- Python;
- Flask;
- SQLite;
- HTML;
- estilização básica incorporada aos templates HTML.

---

## 3. Estrutura principal do projeto

A estrutura principal do sistema é:

```text
aps-seguranca/
│
├── app.py
├── database.py
├── login_service.py
├── requirements.txt
├── README.md
│
└── templates/
    ├── login.html
    ├── dashboard.html
    ├── admin.html
    ├── registros.html
    └── acesso_negado.html