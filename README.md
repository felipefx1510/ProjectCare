# ProjectCare - Documentação Técnica

## Visão Geral do Projeto

O ProjectCare é uma plataforma web desenvolvida em Flask que conecta Responsáveis por idosos a Cuidadores qualificados. O sistema permite:

- Cadastro de usuários com perfis de Cuidador e/ou Responsável
- Cadastro de idosos vinculados a um Responsável
- Listagem e visualização de perfis de Cuidadores
- Listagem e visualização de idosos cadastrados
- Gerenciamento de contratos entre Cuidadores e Responsáveis

O público-alvo da aplicação são pessoas que precisam de cuidadores para seus idosos (Responsáveis) e profissionais que oferecem serviços de cuidados para idosos (Cuidadores).

## Arquitetura e Tecnologias

### Principais Tecnologias

- **Backend**: Flask 3.1.0 (framework web Python)
- **ORM**: SQLAlchemy 2.0.40 com Flask-SQLAlchemy 3.1.1
- **Banco de Dados**: PostgreSQL (via psycopg2-binary 2.9.10)
- **Migrações**: Flask-Migrate 4.1.0 com Alembic 1.15.2
- **Autenticação**: Gerenciamento de sessão nativo do Flask
- **Segurança de Senhas**: Argon2 (via argon2-cffi 23.1.0)
- **Frontend**: 
  - Templates Jinja2 3.1.6
  - Bootstrap 5.3.3
  - CSS customizado
  - Biblioteca de animações AOS
- **Configuração de Ambiente**: python-dotenv 1.1.0
- **Deploy**: Vercel

### Estrutura do Projeto

```
ProjectCare/
├── app/                        # Pacote principal da aplicação
│   ├── __init__.py             # Inicialização da aplicação Flask
│   ├── config/                 # Configurações
│   │   └── securityconfig.py   # Configurações de segurança
│   ├── models/                 # Modelos de dados
│   │   ├── __init__.py
│   │   ├── caregiver.py        # Modelo de Cuidador
│   │   ├── contract.py         # Modelo de Contrato
│   │   ├── elderly.py          # Modelo de Idoso
│   │   ├── responsible.py      # Modelo de Responsável
│   │   └── user.py             # Modelo de Usuário
│   ├── routes/                 # Rotas/Blueprints
│   │   ├── __init__.py
│   │   ├── caregivers.py       # Rotas para cuidadores
│   │   ├── contact.py          # Rotas para contato
│   │   ├── home.py             # Rotas para página inicial
│   │   ├── login.py            # Rotas para login/autenticação
│   │   ├── register.py         # Rotas para registro
│   │   ├── responsible_dashboard.py # Rotas para dashboard de responsáveis
│   │   └── user.py             # Rotas para usuários
│   ├── services/               # Serviços (lógica de negócios)
│   │   ├── __init__.py
│   │   ├── caregiver_service.py # Serviço para cuidadores
│   │   ├── elderly_service.py   # Serviço para idosos
│   │   ├── responsible_service.py # Serviço para responsáveis
│   │   └── user_service.py      # Serviço para usuários
│   ├── static/                 # Arquivos estáticos
│   │   ├── css/
│   │   │   └── style.css       # CSS customizado
│   │   └── images/             # Imagens
│   ├── templates/              # Templates HTML
│   │   ├── base.html           # Template base
│   │   ├── contact/            # Templates de contato
│   │   ├── fragments/          # Fragmentos reutilizáveis
│   │   ├── home/               # Templates da página inicial
│   │   ├── list/               # Templates de listagem
│   │   ├── login/              # Templates de login
│   │   └── register/           # Templates de registro
│   └── run.py                  # Ponto de entrada da aplicação
├── migrations/                 # Migrações de banco de dados
│   ├── versions/               # Versões das migrações
│   ├── alembic.ini             # Configuração do Alembic
│   ├── env.py                  # Ambiente de migração
│   ├── README                  # Documentação das migrações
│   └── script.py.mako          # Template para scripts de migração
├── config.py                   # Configurações gerais
├── requirements.txt            # Dependências do projeto
└── vercel.json                 # Configuração de deploy na Vercel
```

### Fluxo de uma Requisição HTTP

1. O cliente faz uma requisição HTTP para uma URL da aplicação
2. A Vercel direciona a requisição para o ponto de entrada `app/run.py`
3. O Flask processa a requisição e a encaminha para o blueprint e rota correspondentes
4. A função controladora da rota é executada, interagindo com os serviços e modelos conforme necessário
5. Os serviços executam a lógica de negócios, interagindo com o banco de dados via SQLAlchemy
6. A função controladora renderiza um template Jinja2 com os dados necessários
7. O Flask retorna a resposta HTTP com o HTML renderizado para o cliente

## Configuração do Ambiente de Desenvolvimento

### Pré-requisitos

- Python 3.8 ou superior
- PostgreSQL

### Instalação

1. Clone o repositório:
   ```bash
   git clone <url-do-repositorio>
   cd ProjectCare
   ```

2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   # No Windows
   venv\Scripts\activate
   # No Linux/Mac
   source venv/bin/activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:
   ```
   SECRET_KEY=sua_chave_secreta_aqui
   DATABASE_URL=postgresql://usuario:senha@localhost/projectcare
   ```

### Configuração do Banco de Dados

1. Crie um banco de dados PostgreSQL:
   ```sql
   CREATE DATABASE projectcare;
   ```

2. Execute as migrações para criar as tabelas:
   ```bash
   flask db upgrade
   ```

### Executando a Aplicação

```bash
python -m app.run
```

A aplicação estará disponível em `http://localhost:5000`.

## Modelos de Dados (Banco de Dados)

### Diagrama ER

```
+-------------+       +---------------+       +-------------+
|    User     |       |   Caregiver   |       |  Contract   |
+-------------+       +---------------+       +-------------+
| id          |<----->| id            |<----->| id          |
| name        |       | user_id       |       | caregiver_id|
| cpf         |       | specialty     |       | responsible_id|
| gender      |       | experience    |       | start_date  |
| birthdate   |       | education     |       | end_date    |
| phone       |       | expertise_area|       +-------------+
| email       |       | skills        |
| password_hash|       | rating        |
| address     |       | dias_disponiveis|
| city        |       | periodos_disponiveis|
| state       |       | inicio_imediato|
| created_at  |       | pretensao_salarial|
+-------------+       +---------------+
      ^                      
      |                      
      |                      
+-------------+       +-------------+
| Responsible |       |   Elderly   |
+-------------+       +-------------+
| id          |<----->| id          |
| user_id     |       | name        |
| relationship_with_elderly|       | cpf         |
| primary_need_description|       | birthdate   |
| preferred_contact_method|       | gender      |
+-------------+       | address_elderly|
                      | city_elderly|
                      | state_elderly|
                      | photo_url   |
                      | medical_conditions|
                      | allergies   |
                      | medications_in_use|
                      | mobility_level|
                      | specific_care_needs|
                      | emergency_contact_name|
                      | emergency_contact_phone|
                      | emergency_contact_relationship|
                      | health_plan_name|
                      | health_plan_number|
                      | additional_notes|
                      | responsible_id|
                      +-------------+
```

### User

**Propósito**: Armazena informações básicas dos usuários do sistema.

**Atributos**:
- `id` (Integer, PK): Identificador único do usuário
- `name` (String, not null): Nome completo do usuário
- `cpf` (String, unique, not null): CPF do usuário
- `gender` (String, not null): Gênero do usuário
- `birthdate` (Date, not null): Data de nascimento
- `phone` (String, unique, not null): Telefone de contato
- `email` (String, unique, not null): Email do usuário
- `password_hash` (String, not null): Hash da senha usando Argon2
- `address` (String, not null): Endereço completo
- `city` (String, not null): Cidade
- `state` (String, not null): Estado
- `created_at` (DateTime): Data de criação do registro

**Relacionamentos**:
- `caregiver` (One-to-One): Relação com o modelo Caregiver
- `responsible` (One-to-One): Relação com o modelo Responsible

**Métodos**:
- `set_password(password)`: Define a senha do usuário, aplicando hash com Argon2
- `check_password(password)`: Verifica se a senha fornecida corresponde ao hash armazenado

### Caregiver

**Propósito**: Armazena informações profissionais dos cuidadores.

**Atributos**:
- `id` (Integer, PK): Identificador único do cuidador
- `user_id` (Integer, FK, not null): Referência ao usuário associado
- `specialty` (String, not null): Especialidade do cuidador
- `experience` (Integer, not null): Anos de experiência
- `education` (String, not null): Formação educacional
- `expertise_area` (String, not null): Área de expertise
- `skills` (String, not null): Habilidades e competências
- `rating` (Float, not null, default=0.0): Avaliação média
- `dias_disponiveis` (String): Dias da semana disponíveis
- `periodos_disponiveis` (String): Períodos do dia disponíveis
- `inicio_imediato` (Boolean): Disponibilidade para início imediato
- `pretensao_salarial` (Float): Pretensão salarial

**Relacionamentos**:
- `user` (Many-to-One): Relação com o modelo User
- `contracts` (One-to-Many): Relação com o modelo Contract

### Responsible

**Propósito**: Armazena informações dos responsáveis por idosos.

**Atributos**:
- `id` (Integer, PK): Identificador único do responsável
- `user_id` (Integer, FK, not null): Referência ao usuário associado
- `relationship_with_elderly` (String): Relação com o idoso (filho, cônjuge, etc.)
- `primary_need_description` (String): Descrição da necessidade principal de cuidado
- `preferred_contact_method` (String): Método de contato preferido

**Relacionamentos**:
- `user` (Many-to-One): Relação com o modelo User
- `elderly` (One-to-Many): Relação com o modelo Elderly
- `contracts` (One-to-Many): Relação com o modelo Contract

### Elderly

**Propósito**: Armazena informações detalhadas sobre os idosos cadastrados.

**Atributos**:
- `id` (Integer, PK): Identificador único do idoso
- `name` (String, not null): Nome completo do idoso
- `cpf` (String): CPF do idoso
- `birthdate` (Date, not null): Data de nascimento
- `gender` (String, not null): Gênero
- `address_elderly` (String): Endereço do idoso
- `city_elderly` (String): Cidade do idoso
- `state_elderly` (String): Estado do idoso
- `photo_url` (String): URL da foto do idoso
- `medical_conditions` (Text): Condições médicas
- `allergies` (Text): Alergias
- `medications_in_use` (Text): Medicamentos em uso
- `mobility_level` (String): Nível de mobilidade
- `specific_care_needs` (Text): Necessidades específicas de cuidado
- `emergency_contact_name` (String): Nome do contato de emergência
- `emergency_contact_phone` (String): Telefone do contato de emergência
- `emergency_contact_relationship` (String): Relação do contato de emergência
- `health_plan_name` (String): Nome do plano de saúde
- `health_plan_number` (String): Número do plano de saúde
- `additional_notes` (Text): Observações adicionais
- `responsible_id` (Integer, FK, not null): Referência ao responsável

**Relacionamentos**:
- `responsible` (Many-to-One): Relação com o modelo Responsible

### Contract

**Propósito**: Armazena informações sobre contratos entre cuidadores e responsáveis.

**Atributos**:
- `id` (Integer, PK): Identificador único do contrato
- `responsible_id` (Integer, FK, not null): Referência ao responsável
- `caregiver_id` (Integer, FK, not null): Referência ao cuidador
- `start_date` (DateTime, not null): Data de início do contrato
- `end_date` (DateTime, not null): Data de término do contrato

**Relacionamentos**:
- `responsible` (Many-to-One): Relação com o modelo Responsible
- `caregiver` (Many-to-One): Relação com o modelo Caregiver

## Rotas e Controladores (Blueprints)

### home_bp (/):
- **/** (GET): Página inicial da aplicação
  - Função: `home()`
  - Template: `home/home.html`
  - Descrição: Exibe a página inicial com informações sobre o serviço

### login_bp (/login):
- **/login/** (GET, POST): Autenticação de usuários
  - Função: `login()`
  - Template: `login/login.html`
  - Descrição: Processa o login de usuários e gerencia a sessão
  - Parâmetros POST: email, password
  - Sessão: Define `user_id` e `acting_profile`

- **/login/select-acting-profile** (GET, POST): Seleção de perfil de atuação
  - Função: `select_acting_profile()`
  - Template: `login/select_acting_profile.html`
  - Descrição: Permite ao usuário escolher entre perfil de Cuidador ou Responsável
  - Parâmetros POST: acting_profile
  - Sessão: Define `acting_profile` como 'caregiver' ou 'responsible'

- **/login/logout** (GET): Logout de usuários
  - Função: `logout()`
  - Descrição: Remove a sessão do usuário

### register_bp (/register):
- **/register/** (GET, POST): Registro de novos usuários
  - Função: `register()`
  - Template: `register/register.html`
  - Descrição: Processa o registro de novos usuários
  - Parâmetros POST: name, cpf, phone, email, password, address, city, state, birthdate, gender
  - Sessão: Define `user_id`

- **/register/select-profile** (GET): Seleção de perfil após registro
  - Função: `select_profile()`
  - Template: `register/select.html`
  - Descrição: Permite ao usuário escolher qual perfil criar após o registro

- **/register/add-profile** (GET, POST): Adicionar perfil a usuário existente
  - Função: `add_profile()`
  - Template: `profile/select.html`
  - Descrição: Permite adicionar um perfil adicional a um usuário existente
  - Parâmetros POST: add_caregiver, add_responsible

- **/register/caregiver** (GET, POST): Registro de perfil de cuidador
  - Função: `register_caregiver()`
  - Template: `register/register_caregiver.html`
  - Descrição: Processa o registro de um perfil de cuidador
  - Parâmetros POST: specialty, experience, education, expertise, skills, dias[], periodos[], inicio_imediato, pretensao
  - Sessão: Define `acting_profile` como 'caregiver'

- **/register/responsible** (GET, POST): Registro de perfil de responsável
  - Função: `register_responsible()`
  - Template: `register/register_responsible.html`
  - Descrição: Processa o registro de um perfil de responsável
  - Parâmetros POST: relationship_with_elderly, primary_need_description, preferred_contact_method
  - Sessão: Define `acting_profile` como 'responsible'

- **/register/elderly** (GET, POST): Registro de idoso
  - Função: `register_elderly()`
  - Template: `register/register_elderly.html`
  - Descrição: Processa o registro de um idoso por um responsável
  - Parâmetros POST: Diversos campos com informações do idoso

### caregivers_bp (/caregivers):
- **/caregivers/** (GET): Listagem de cuidadores
  - Função: `list_caregivers()`
  - Template: `list/caregiver_list.html`
  - Descrição: Exibe a lista de cuidadores disponíveis

- **/caregivers/<int:caregiver_id>** (GET): Detalhes de um cuidador
  - Função: `caregiver_details(caregiver_id)`
  - Template: `list/caregiver_details.html`
  - Descrição: Exibe detalhes de um cuidador específico

### responsible_dashboard_bp (/responsible):
- **/responsible/dashboard** (GET): Dashboard do responsável
  - Função: `dashboard()`
  - Template: `responsible/dashboard.html`
  - Descrição: Exibe o dashboard para usuários com perfil de responsável

- **/responsible/elderly** (GET): Listagem de idosos do responsável
  - Função: `list_elderly()`
  - Template: `list/my_elderly_list.html`
  - Descrição: Exibe a lista de idosos cadastrados pelo responsável

- **/responsible/elderly/<int:elderly_id>** (GET): Detalhes de um idoso
  - Função: `elderly_details(elderly_id)`
  - Template: `list/elderly_details.html`
  - Descrição: Exibe detalhes de um idoso específico

### contact_bp (/contact):
- **/contact/** (GET, POST): Página de contato
  - Função: `contact()`
  - Template: `contact/contact.html`
  - Descrição: Exibe e processa o formulário de contato

## Camada de Serviço

### user_service

**Responsabilidade**: Gerenciar operações relacionadas a usuários.

**Métodos**:
- `save(user)`: Salva um novo usuário no banco de dados
- `get_by_id(user_id)`: Recupera um usuário pelo ID
- `get_by_email(email)`: Recupera um usuário pelo email
- `get_by_email_or_phone_or_cpf(email, phone, cpf)`: Recupera um usuário pelo email, telefone ou CPF
- `get_all()`: Recupera todos os usuários
- `delete(user)`: Remove um usuário do banco de dados

### CaregiverService

**Responsabilidade**: Gerenciar operações relacionadas a cuidadores.

**Métodos**:
- `save(caregiver)`: Salva um novo cuidador no banco de dados
- `get_all_caregivers()`: Recupera todos os cuidadores
- `get_caregiver_by_id(caregiver_id)`: Recupera um cuidador pelo ID
- `get_caregiver_by_email(email)`: Recupera um cuidador pelo email do usuário associado

### ResponsibleService

**Responsabilidade**: Gerenciar operações relacionadas a responsáveis.

**Métodos**:
- `save(responsible)`: Salva um novo responsável no banco de dados
- `get_all_responsibles()`: Recupera todos os responsáveis
- `get_responsible_by_id(responsible_id)`: Recupera um responsável pelo ID
- `get_responsible_by_email(email)`: Recupera um responsável pelo email do usuário associado
- `get_responsible_by_user_id(user_id)`: Recupera um responsável pelo ID do usuário associado

### ElderlyService

**Responsabilidade**: Gerenciar operações relacionadas a idosos.

**Métodos**:
- `save(elderly)`: Salva um novo idoso no banco de dados
- `get_all()`: Recupera todos os idosos
- `get_by_id(elderly_id)`: Recupera um idoso pelo ID
- `get_by_user_id(user_id)`: Recupera um idoso pelo ID do usuário (método não utilizado)
- `get_by_responsible_id(responsible_id)`: Recupera todos os idosos associados a um responsável específico

## Autenticação e Gerenciamento de Sessão

### Autenticação

O sistema utiliza autenticação baseada em sessão nativa do Flask:

1. O usuário fornece email e senha no formulário de login
2. O sistema verifica as credenciais usando o método `check_password` do modelo User
3. Se as credenciais forem válidas, o ID do usuário é armazenado na sessão (`session['user_id']`)
4. O sistema verifica quais perfis o usuário possui (Cuidador e/ou Responsável)
5. Se o usuário tiver ambos os perfis, ele é redirecionado para escolher qual perfil usar
6. O perfil escolhido é armazenado na sessão (`session['acting_profile']`)

### Segurança de Senhas

As senhas são armazenadas usando o algoritmo Argon2, considerado um dos mais seguros para hash de senhas:

1. Quando um usuário é criado ou altera sua senha, o método `set_password` é chamado
2. Este método aplica o hash Argon2 à senha e armazena o resultado em `password_hash`
3. Durante o login, o método `check_password` verifica se a senha fornecida corresponde ao hash armazenado

### Gerenciamento de Sessão

A sessão do Flask é usada para armazenar:
- `user_id`: ID do usuário autenticado
- `acting_profile`: Perfil atual do usuário ('caregiver' ou 'responsible')

O context processor `inject_user` em `app/__init__.py` injeta informações do usuário nos templates, permitindo que a navbar seja renderizada corretamente com base no estado de autenticação.

## Interface do Usuário (Frontend)

### Estrutura de Templates

A aplicação utiliza uma estrutura hierárquica de templates Jinja2:

- `base.html`: Template base com estrutura HTML comum, CSS, JavaScript e blocos para conteúdo
- Fragmentos reutilizáveis em `fragments/`:
  - `navbar.html`: Barra de navegação para usuários não autenticados
  - `navbar_login.html`: Barra de navegação para usuários autenticados
  - `footer.html`: Rodapé comum a todas as páginas
  - `flash.html`: Exibição de mensagens flash

### Tecnologias Frontend

- **Bootstrap 5.3.3**: Framework CSS para layout responsivo e componentes
- **Google Fonts**: Fontes Nunito e Lora
- **Bootstrap Icons**: Ícones
- **AOS Animation Library**: Animações de scroll
- **CSS Customizado**: Estilos específicos da aplicação em `static/css/style.css`

## Fluxos de Usuário Chave

### Registro de Novo Usuário

1. Usuário acessa a página de registro (`/register/`)
2. Preenche o formulário com informações pessoais (nome, CPF, email, senha, etc.)
3. Sistema valida os dados e verifica se o usuário já existe
4. Se os dados forem válidos, o usuário é criado e o ID é armazenado na sessão
5. Usuário é redirecionado para a página de seleção de perfil (`/register/select-profile`)
6. Usuário escolhe entre criar um perfil de Cuidador ou Responsável
7. Usuário é redirecionado para o formulário específico do perfil escolhido
8. Após preencher o formulário do perfil, o perfil é criado e ativado
9. Usuário é redirecionado para a página inicial com o perfil ativo

### Login e Seleção de Perfil

1. Usuário acessa a página de login (`/login/`)
2. Preenche o formulário com email e senha
3. Sistema valida as credenciais
4. Se válidas, o sistema verifica quais perfis o usuário possui:
   - Se não tiver nenhum perfil, é redirecionado para criar um
   - Se tiver ambos os perfis, é redirecionado para escolher qual usar
   - Se tiver apenas um perfil, este é automaticamente ativado
5. O perfil ativo é armazenado na sessão como 'caregiver' ou 'responsible'
6. Usuário é redirecionado para a página inicial com o perfil ativo

### Cadastro de Idoso (para Responsáveis)

1. Usuário com perfil de Responsável acessa a página de cadastro de idoso (`/register/elderly`)
2. Preenche o formulário com informações detalhadas sobre o idoso:
   - Informações básicas (nome, CPF, data de nascimento, gênero)
   - Endereço
   - Informações médicas (condições, alergias, medicamentos)
   - Nível de mobilidade e necessidades específicas
   - Contato de emergência
   - Plano de saúde
   - Observações adicionais
3. Sistema valida os dados e cria o registro do idoso
4. Idoso é associado ao responsável atual
5. Usuário recebe confirmação de cadastro bem-sucedido

## Deploy (Vercel)

A aplicação está configurada para deploy na plataforma Vercel:

### Configuração (vercel.json)

```json
{
    "version": 2,
    "builds": [
      {
        "src": "app/run.py",
        "use": "@vercel/python"
      }
    ],
    "routes": [
      {
        "src": "/(.*)",
        "dest": "app/run.py"
      }
    ]
}
```

### Ponto de Entrada

O arquivo `app/run.py` serve como ponto de entrada para a Vercel:
- Importa a função `create_app` do pacote app
- Cria uma instância da aplicação Flask
- Configura logging para depuração

### Variáveis de Ambiente

As seguintes variáveis de ambiente devem ser configuradas na Vercel:
- `SECRET_KEY`: Chave secreta para segurança da aplicação
- `DATABASE_URL`: URL de conexão com o banco de dados PostgreSQL

## Possíveis Melhorias e Próximos Passos

### Funcionalidades

1. **Sistema de Avaliações**: Implementar um sistema para responsáveis avaliarem cuidadores após serviços prestados
2. **Mensagens Diretas**: Adicionar um sistema de mensagens entre cuidadores e responsáveis
3. **Calendário de Disponibilidade**: Implementar um calendário para cuidadores indicarem disponibilidade
4. **Pagamentos**: Integrar um sistema de pagamento para facilitar transações entre responsáveis e cuidadores
5. **Notificações**: Adicionar notificações por email ou push para eventos importantes

### Técnicas

1. **Testes Automatizados**: Implementar testes unitários e de integração
2. **API RESTful**: Criar uma API para permitir integrações com aplicativos móveis
3. **Refatoração de Serviços**: Padronizar a abordagem (funcional vs. classe) nos serviços
4. **Cache**: Implementar cache para melhorar o desempenho
5. **Monitoramento**: Adicionar ferramentas de monitoramento e logging
6. **Documentação de API**: Se uma API for implementada, documentá-la com Swagger/OpenAPI

### Segurança

1. **Autenticação de Dois Fatores**: Adicionar 2FA para maior segurança
2. **Rate Limiting**: Implementar limitação de taxa para prevenir ataques de força bruta
3. **CSRF Protection**: Garantir proteção contra ataques CSRF em todos os formulários
4. **Verificação de Email**: Adicionar verificação de email durante o registro
5. **Auditoria**: Implementar logs de auditoria para ações sensíveis