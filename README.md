# ProjectCare 🏥

Sistema de gerenciamento de cuidadores e responsáveis por idosos, desenvolvido em Flask com arquitetura MVC e integração com APIs externas.

## 📋 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Funcionalidades](#funcionalidades)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Arquitetura](#arquitetura)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Como Usar](#como-usar)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Modelos de Dados](#modelos-de-dados)
- [API Endpoints](#api-endpoints)
- [Deploy](#deploy)

## 📖 Sobre o Projeto

O **ProjectCare** é uma plataforma web que conecta cuidadores qualificados com responsáveis por idosos, facilitando a contratação de serviços de cuidado domiciliar. O sistema oferece dashboards personalizados para diferentes perfis de usuário e gerenciamento completo de contratos.

### Objetivos

- 🎯 Facilitar a conexão entre cuidadores e famílias
- 📊 Fornecer dashboards informativos para cada perfil
- 🔒 Garantir segurança na autenticação e autorização
- 📱 Oferecer interface responsiva e intuitiva
- 🏥 Gerenciar informações médicas e de cuidado

## ⚡ Funcionalidades

### Para Responsáveis
- ✅ Cadastro e gerenciamento de perfil
- 👴 Cadastro de idosos sob cuidado
- 🔍 Busca e visualização de cuidadores disponíveis
- 📋 Criação e gerenciamento de contratos
- 📊 Dashboard personalizado com estatísticas

### Para Cuidadores
- ✅ Cadastro com especialidades e disponibilidade
- 📝 Definição de experiência e qualificações
- 👥 Visualização de idosos cadastrados
- 💼 Gestão de contratos ativos
- 📈 Dashboard com métricas de desempenho

### Funcionalidades Gerais
- 🔐 Sistema de autenticação seguro
- 👤 Seleção de perfil de atuação (cuidador/responsável)
- 🏠 Integração com ViaCEP para endereços
- 📱 Interface responsiva com Bootstrap
- 🎨 Design moderno e acessível

## 🛠 Tecnologias Utilizadas

### Backend
- **Python 3.13** - Linguagem principal
- **Flask** - Framework web
- **SQLAlchemy** - ORM para banco de dados
- **Flask-Migrate** - Migrações de banco
- **Werkzeug** - Utilitários WSGI

### Frontend
- **HTML5/CSS3** - Estrutura e estilização
- **Bootstrap 5** - Framework CSS responsivo
- **JavaScript** - Interatividade no frontend
- **Jinja2** - Engine de templates

### Banco de Dados
- **SQLite** (desenvolvimento)
- **PostgreSQL** (produção)

### Integrações
- **ViaCEP API** - Consulta de endereços por CEP
- **Vercel** - Deploy e hospedagem

### Ferramentas
- **python-dotenv** - Gerenciamento de variáveis de ambiente
- **Alembic** - Controle de versão do banco

## 🏗 Arquitetura

O projeto segue a arquitetura **MVC (Model-View-Controller)** com camada de serviços:

```
ProjectCare/
├── app/
│   ├── models/          # Modelos de dados (ORM)
│   ├── routes/          # Controllers (Blueprints)
│   ├── services/        # Lógica de negócio
│   ├── templates/       # Views (HTML Templates)
│   └── static/          # Arquivos estáticos
├── migrations/          # Migrações do banco
└── config files         # Configurações e deploy
```

### Padrões Utilizados
- **Repository Pattern** - Camada de serviços
- **Blueprint** - Organização de rotas
- **Factory Pattern** - Criação da aplicação Flask
- **Dependency Injection** - Injeção de dependências

## 📦 Instalação

### Pré-requisitos
- Python 3.8+
- pip
- Git

### Passos

1. **Clone o repositório**
```bash
git clone https://github.com/seu-usuario/projectcare.git
cd projectcare
```

2. **Crie um ambiente virtual**
```bash
python -m venv venv
```

3. **Ative o ambiente virtual**
```bash
# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

4. **Instale as dependências**
```bash
pip install -r requirements.txt
```

## ⚙ Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
# Configurações obrigatórias
SECRET_KEY=sua_chave_secreta_muito_segura_aqui
DATABASE_URL=sqlite:///projectcare.db

# Para produção (PostgreSQL)
# DATABASE_URL=postgresql://usuario:senha@host:porta/database

# Configurações opcionais
FLASK_ENV=development
FLASK_DEBUG=True
```

### Inicialização do Banco

```bash
# Inicializar migrações (apenas primeira vez)
flask db init

# Criar migração
flask db migrate -m "Migração inicial"

# Aplicar migrações
flask db upgrade
```

## 🚀 Como Usar

### Desenvolvimento

```bash
# Executar aplicação
python app/run.py

# Ou usando Flask CLI
flask run
```

A aplicação estará disponível em `http://localhost:5000`

### Primeiro Acesso

1. Acesse a página inicial
2. Clique em "Cadastrar-se"
3. Escolha o tipo de usuário (Responsável ou Cuidador)
4. Preencha as informações necessárias
5. Faça login e explore as funcionalidades

## 📁 Estrutura do Projeto

```
ProjectCare/
├── app/
│   ├── __init__.py              # Factory da aplicação Flask
│   ├── run.py                   # Entry point da aplicação
│   ├── models/                  # Modelos de dados
│   │   ├── __init__.py
│   │   ├── user.py              # Modelo base de usuário
│   │   ├── caregiver.py         # Modelo de cuidador
│   │   ├── responsible.py       # Modelo de responsável
│   │   ├── elderly.py           # Modelo de idoso
│   │   └── contract.py          # Modelo de contrato
│   ├── routes/                  # Controllers (Blueprints)
│   │   ├── __init__.py
│   │   ├── home.py              # Página inicial e dashboards
│   │   ├── login.py             # Autenticação
│   │   ├── register.py          # Cadastros
│   │   ├── caregivers.py        # Listagens
│   │   ├── contact.py           # Contato
│   │   ├── api.py               # API endpoints
│   │   └── responsible_dashboard.py  # Dashboard do responsável
│   ├── services/                # Camada de negócio
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   ├── caregiver_service.py
│   │   ├── responsible_service.py
│   │   ├── elderly_service.py
│   │   ├── authentication_service.py
│   │   └── viacep_service.py
│   ├── templates/               # Templates HTML
│   │   ├── base.html            # Template base
│   │   ├── home/                # Páginas iniciais
│   │   ├── login/               # Templates de login
│   │   ├── register/            # Templates de cadastro
│   │   ├── list/                # Templates de listagem
│   │   ├── contact/             # Página de contato
│   │   └── fragments/           # Componentes reutilizáveis
│   └── static/                  # Arquivos estáticos
│       ├── css/
│       │   └── style.css        # Estilos customizados
│       ├── js/
│       │   └── cep.js           # Funcionalidade de CEP
│       └── images/              # Imagens do projeto
├── migrations/                  # Migrações do banco
├── requirements.txt             # Dependências Python
├── vercel.json                  # Configuração de deploy
├── .env                         # Variáveis de ambiente
└── README.md                    # Este arquivo
```

## 🗄 Modelos de Dados

### User (Usuário Base)
```python
- id: Identificador único
- name: Nome completo
- email: Email (único)
- password_hash: Senha criptografada
- phone: Telefone
- created_at: Data de criação
```

### Caregiver (Cuidador)
```python
- user_id: Referência ao usuário
- experience_years: Anos de experiência
- specialties: Especialidades (JSON)
- availability: Disponibilidade (JSON)
- hourly_rate: Valor por hora
- description: Descrição profissional
- address: Endereço completo
```

### Responsible (Responsável)
```python
- user_id: Referência ao usuário
- relationship: Relacionamento com idoso
- address: Endereço completo
```

### Elderly (Idoso)
```python
- id: Identificador único
- responsible_id: Referência ao responsável
- name: Nome completo
- age: Idade
- medical_conditions: Condições médicas
- medications: Medicamentos
- care_needs: Necessidades de cuidado
- mobility_level: Nível de mobilidade
```

### Contract (Contrato)
```python
- id: Identificador único
- caregiver_id: Referência ao cuidador
- responsible_id: Referência ao responsável
- elderly_id: Referência ao idoso
- start_date: Data de início
- end_date: Data de término
- status: Status do contrato
- terms: Termos contratuais
```

## 🔌 API Endpoints

### Autenticação
- `POST /login` - Login de usuário
- `POST /logout` - Logout de usuário
- `POST /select-profile` - Seleção de perfil

### Cadastros
- `GET/POST /register` - Cadastro de usuário
- `GET/POST /register/caregiver` - Cadastro de cuidador
- `GET/POST /register/responsible` - Cadastro de responsável
- `GET/POST /register/elderly` - Cadastro de idoso

### Listagens
- `GET /caregivers` - Lista de cuidadores
- `GET /elderly` - Lista de idosos

### API Externa
- `GET /api/cep/<cep>` - Consulta CEP via ViaCEP

### Dashboards
- `GET /` - Dashboard principal
- `GET /responsible-dashboard` - Dashboard do responsável

## 🌐 Deploy

### Vercel (Recomendado)

1. **Configure o arquivo `vercel.json`** (já incluído)
2. **Configure as variáveis de ambiente** no painel da Vercel
3. **Conecte seu repositório** GitHub à Vercel
4. **Deploy automático** a cada push

### Configuração Manual

```bash
# Instalar Vercel CLI
npm i -g vercel

# Deploy
vercel

# Configurar variáveis de ambiente
vercel env add SECRET_KEY
vercel env add DATABASE_URL
```

### Outras Plataformas

O projeto também pode ser deployado em:
- Heroku
- Railway
- PythonAnywhere
- DigitalOcean App Platform

### Padrões de Código

- Siga a **PEP 8** para Python
- Use **nomes descritivos** para variáveis e funções
- **Documente** suas funções e classes
- **Teste** suas funcionalidades
- **Mantenha** a consistência com o código existente

### Estrutura de Commits

```
tipo(escopo): descrição

- feat: nova funcionalidade
- fix: correção de bug
- docs: documentação
- style: formatação
- refactor: refatoração
- test: testes
```

### Issues e Bugs

Para reportar bugs ou sugerir melhorias:
1. Verifique se já existe uma issue similar
2. Crie uma nova issue com template apropriado
3. Forneça informações detalhadas
4. Inclua screenshots quando relevante

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👥 Autores

- **Breno Siqueira e Felipe Félix** - *Desenvolvimento* - [GitHub](https://github.com/felipefx1510)

## 🙏 Agradecimentos

- Comunidade Flask pelo excelente framework
- Bootstrap pela biblioteca de componentes
- ViaCEP pela API gratuita de CEP
- Vercel pela hospedagem