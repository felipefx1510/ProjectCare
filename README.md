# ProjectCare

## Visão Geral do Projeto

ProjectCare é uma plataforma web desenvolvida em Flask que visa conectar responsáveis por idosos a cuidadores profissionais. A plataforma facilita o cadastro de usuários (cuidadores e responsáveis), a criação de perfis detalhados, o registro de informações sobre os idosos, e a busca por profissionais adequados às necessidades de cada família.

### Principais Funcionalidades

- **Cadastro e Autenticação de Usuários**: Sistema seguro de registro e login com hash de senha usando Argon2.
- **Perfis Múltiplos**: Usuários podem se registrar como cuidadores, responsáveis, ou ambos.
- **Cadastro de Idosos**: Responsáveis podem cadastrar idosos com informações detalhadas de saúde e cuidados.
- **Busca de Cuidadores**: Responsáveis podem buscar cuidadores com base em suas especialidades e disponibilidade.
- **Visualização de Perfis**: Detalhes completos sobre cuidadores e idosos para facilitar a escolha.
- **Contratos**: Gerenciamento de contratos entre responsáveis e cuidadores.

## Arquitetura da Aplicação

ProjectCare segue uma arquitetura baseada no padrão Model-View-Controller (MVC), adaptado para o Flask:

- **Models**: Representam as entidades do banco de dados e suas relações (`app/models/`)
- **Views**: Implementadas como templates Jinja2 (`app/templates/`)
- **Controllers**: Implementados como rotas Flask (`app/routes/`) e serviços (`app/services/`)

### Principais Componentes

- **Models**: Definem a estrutura de dados e relacionamentos usando SQLAlchemy.
  - `User`: Modelo base para todos os usuários
  - `Caregiver`: Perfil de cuidador
  - `Responsible`: Perfil de responsável
  - `Elderly`: Informações sobre idosos
  - `Contract`: Contratos entre responsáveis e cuidadores

- **Routes**: Controlam o fluxo da aplicação e processam requisições HTTP.
  - `home`: Página inicial
  - `login`: Autenticação de usuários
  - `register`: Registro de usuários e perfis
  - `caregivers`: Listagem e busca de cuidadores
  - `responsible_dashboard`: Dashboard para responsáveis
  - `contact`: Página de contato

- **Services**: Encapsulam a lógica de negócios e interações com os modelos.
  - `user_service`: Operações relacionadas a usuários
  - `caregiver_service`: Operações relacionadas a cuidadores
  - `responsible_service`: Operações relacionadas a responsáveis
  - `elderly_service`: Operações relacionadas a idosos

### Fluxo de Dados Principal

1. **Cadastro de Usuário**:
   - Usuário preenche formulário de registro
   - Sistema valida dados e cria um objeto User
   - Usuário é redirecionado para selecionar um perfil (cuidador ou responsável)
   - Sistema cria o perfil selecionado associado ao usuário

2. **Login**:
   - Usuário fornece email e senha
   - Sistema verifica credenciais
   - Se o usuário tem múltiplos perfis, é solicitado que escolha um
   - Usuário é redirecionado para a página inicial com o perfil ativo

3. **Cadastro de Idoso**:
   - Responsável preenche formulário com dados do idoso
   - Sistema cria um objeto Elderly associado ao responsável
   - Idoso aparece na lista de idosos do responsável

## Tecnologias Utilizadas

### Backend
- **Python 3.x**: Linguagem de programação principal
- **Flask 3.1.0**: Framework web
- **SQLAlchemy 2.0.40**: ORM (Object-Relational Mapping)
- **Flask-SQLAlchemy 3.1.1**: Integração do SQLAlchemy com Flask
- **Flask-Migrate 4.1.0**: Gerenciamento de migrações de banco de dados
- **Flask-Login 0.6.3**: Gerenciamento de sessões de usuário
- **Flask-WTF 1.2.2**: Validação de formulários
- **Argon2-cffi 23.1.0**: Hash seguro de senhas
- **Python-dotenv 1.1.0**: Gerenciamento de variáveis de ambiente

### Frontend
- **HTML/CSS**: Estrutura e estilo das páginas
- **Jinja2 3.1.6**: Engine de templates
- **Bootstrap** (presumido): Framework CSS para design responsivo

### Banco de Dados
- **PostgreSQL**: Sistema de gerenciamento de banco de dados relacional
- **Psycopg2-binary 2.9.10**: Driver PostgreSQL para Python

### Deployment
- **Vercel**: Plataforma de hospedagem

## Configuração do Ambiente de Desenvolvimento

### Pré-requisitos
- Python 3.x
- pip (gerenciador de pacotes Python)
- PostgreSQL

### Passos para Configuração

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/seu-usuario/projectcare.git
   cd projectcare
   ```

2. **Crie e ative um ambiente virtual**:
   ```bash
   python -m venv venv
   # No Windows
   venv\Scripts\activate
   # No Linux/Mac
   source venv/bin/activate
   ```

3. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as variáveis de ambiente**:
   Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:
   ```
   SECRET_KEY=sua_chave_secreta_aqui
   DATABASE_URL=postgresql://usuario:senha@localhost/projectcare
   ```
   
   Substitua:
   - `sua_chave_secreta_aqui` por uma string aleatória e segura
   - `usuario` e `senha` pelas suas credenciais do PostgreSQL
   - `projectcare` pelo nome do banco de dados que você criou

5. **Crie o banco de dados**:
   ```bash
   # No PostgreSQL
   createdb projectcare
   ```

6. **Execute as migrações**:
   ```bash
   flask db upgrade
   ```

## Executando a Aplicação

1. **Inicie o servidor de desenvolvimento**:
   ```bash
   python -m app.run
   ```

2. **Acesse a aplicação**:
   Abra seu navegador e acesse `http://localhost:5000`

## Estrutura do Banco de Dados

### Modelo User
- **Atributos**: id, name, cpf, gender, birthdate, phone, email, password_hash, address, city, state, created_at
- **Relacionamentos**: 
  - One-to-One com Caregiver
  - One-to-One com Responsible

### Modelo Caregiver
- **Atributos**: id, specialty, experience, education, expertise_area, skills, rating, dias_disponiveis, periodos_disponiveis, inicio_imediato, pretensao_salarial, user_id
- **Relacionamentos**: 
  - One-to-One com User
  - One-to-Many com Contract

### Modelo Responsible
- **Atributos**: id, user_id, relationship_with_elderly, primary_need_description, preferred_contact_method
- **Relacionamentos**: 
  - One-to-One com User
  - One-to-Many com Elderly
  - One-to-Many com Contract

### Modelo Elderly
- **Atributos**: id, name, cpf, birthdate, gender, address_elderly, city_elderly, state_elderly, photo_url, medical_conditions, allergies, medications_in_use, mobility_level, specific_care_needs, emergency_contact_name, emergency_contact_phone, emergency_contact_relationship, health_plan_name, health_plan_number, additional_notes, responsible_id
- **Relacionamentos**: 
  - Many-to-One com Responsible

### Modelo Contract
- **Atributos**: id, start_date, end_date, responsible_id, caregiver_id
- **Relacionamentos**: 
  - Many-to-One com Responsible
  - Many-to-One com Caregiver

## Módulos e Rotas Principais (Endpoints)

### Blueprint: home
- **Propósito**: Gerenciar a página inicial
- **Rotas**:
  - `GET /`: Página inicial da aplicação

### Blueprint: login
- **Propósito**: Gerenciar autenticação de usuários
- **Rotas**:
  - `GET, POST /login/`: Formulário de login e processamento
  - `GET, POST /login/select-acting-profile`: Seleção de perfil ativo (cuidador ou responsável)
  - `GET /login/logout`: Logout do usuário

### Blueprint: register
- **Propósito**: Gerenciar registro de usuários e perfis
- **Rotas**:
  - `GET, POST /register/`: Formulário de registro de usuário e processamento
  - `GET /register/select-profile`: Seleção de perfil para criar (cuidador ou responsável)
  - `GET, POST /register/add-profile`: Adição de perfil para usuário existente
  - `GET, POST /register/caregiver`: Formulário de registro de cuidador e processamento
  - `GET, POST /register/responsible`: Formulário de registro de responsável e processamento
  - `GET, POST /register/elderly`: Formulário de registro de idoso e processamento

### Blueprint: caregivers
- **Propósito**: Gerenciar listagem de cuidadores e idosos
- **Rotas**:
  - `GET /caregivers/`: Lista todos os cuidadores
  - `GET /caregivers/elderly`: Lista todos os idosos

### Blueprint: responsible_dashboard
- **Propósito**: Gerenciar dashboard do responsável
- **Rotas**:
  - `GET /responsible-dashboard/`: Dashboard principal do responsável
  - `GET /responsible-dashboard/my-elderly`: Lista de idosos do responsável

### Blueprint: contact
- **Propósito**: Gerenciar página de contato
- **Rotas**:
  - `GET /contact/`: Página de contato

## Serviços (Lógica de Negócios)

### user_service
- **Responsabilidade**: Gerenciar operações relacionadas a usuários
- **Principais funções**:
  - `save(user)`: Salva um usuário no banco de dados
  - `get_by_id(user_id)`: Busca um usuário pelo ID
  - `get_by_email(email)`: Busca um usuário pelo email
  - `get_by_email_or_phone_or_cpf(email, phone, cpf)`: Busca um usuário por email, telefone ou CPF
  - `get_all()`: Retorna todos os usuários
  - `delete(user)`: Remove um usuário

### caregiver_service
- **Responsabilidade**: Gerenciar operações relacionadas a cuidadores
- **Principais funções**:
  - `save(caregiver)`: Salva um cuidador no banco de dados
  - `get_all_caregivers()`: Retorna todos os cuidadores
  - `get_caregiver_by_id(caregiver_id)`: Busca um cuidador pelo ID
  - `get_caregiver_by_email(email)`: Busca um cuidador pelo email

### responsible_service
- **Responsabilidade**: Gerenciar operações relacionadas a responsáveis
- **Principais funções**:
  - `save(responsible)`: Salva um responsável no banco de dados
  - `get_responsible_by_id(responsible_id)`: Busca um responsável pelo ID
  - `get_responsible_by_email(email)`: Busca um responsável pelo email

### elderly_service
- **Responsabilidade**: Gerenciar operações relacionadas a idosos
- **Principais funções**:
  - `save(elderly)`: Salva um idoso no banco de dados
  - `get_all()`: Retorna todos os idosos
  - `get_by_id(elderly_id)`: Busca um idoso pelo ID

## Autenticação e Autorização

### Autenticação
- A autenticação é baseada em sessões usando Flask's `session`
- As senhas são armazenadas usando hash Argon2, um algoritmo seguro e moderno
- O login é feito através do email e senha

### Autorização
- Após o login, o usuário pode ter um ou mais perfis (cuidador, responsável)
- Se o usuário tiver múltiplos perfis, ele deve escolher qual perfil usar
- O perfil ativo é armazenado na sessão como `acting_profile`
- Certas rotas e funcionalidades são restritas com base no perfil ativo

### Segurança de Senha
- As senhas são protegidas usando Argon2, um algoritmo de hash vencedor da competição Password Hashing Competition
- Configurações de segurança incluem:
  - time_cost: 5
  - memory_cost: 131072 (128 MiB)
  - parallelism: 10
  - hash_len: 64
  - salt_len: 16

## Deploy

O projeto está configurado para deploy na plataforma Vercel, usando o arquivo `vercel.json` na raiz do projeto. A configuração define:

- O ponto de entrada da aplicação como `app/run.py`
- Todas as rotas são direcionadas para esse arquivo

Para fazer deploy na Vercel:
1. Instale a CLI da Vercel: `npm i -g vercel`
2. Execute `vercel login` e siga as instruções
3. Execute `vercel` na raiz do projeto

## Possíveis Melhorias e Próximos Passos

Com base na análise do código, aqui estão algumas sugestões para melhorias:

1. **Segurança**:
   - Implementar proteção CSRF em todos os formulários
   - Adicionar validação mais rigorosa de entrada de dados
   - Implementar rate limiting para prevenir ataques de força bruta

2. **Arquitetura**:
   - Refatorar os serviços para usar uma abordagem consistente (funções vs. classes)
   - Implementar injeção de dependência para facilitar testes
   - Adicionar logging abrangente

3. **Funcionalidades**:
   - Implementar sistema de avaliações para cuidadores
   - Adicionar sistema de mensagens entre responsáveis e cuidadores
   - Implementar notificações por email
   - Adicionar sistema de pagamento
   - Implementar sistema de busca avançada de cuidadores

4. **UX/UI**:
   - Melhorar a responsividade para dispositivos móveis
   - Adicionar mais feedback visual para ações do usuário
   - Implementar upload de fotos para perfis

5. **Testes**:
   - Aumentar a cobertura de testes unitários
   - Adicionar testes de integração
   - Implementar testes end-to-end

6. **Documentação**:
   - Adicionar docstrings a todas as funções e classes
   - Gerar documentação automática usando Sphinx
   - Criar documentação de API para possível integração futura

7. **Infraestrutura**:
   - Configurar CI/CD para testes automáticos e deploy
   - Implementar monitoramento e alertas
   - Configurar backups automáticos do banco de dados

---