# ProjectCare – Documentação Técnica

## Visão Geral do Projeto
ProjectCare é uma aplicação web desenvolvida em Flask para intermediar o cadastro e a conexão entre **cuidadores**, **responsáveis** e **idosos**. O sistema permite criar perfis distintos, registrar informações de cuidados, consultar endereços via ViaCEP e organizar contratos entre responsáveis e cuidadores. As principais tecnologias incluem Flask, Flask-SQLAlchemy, Flask-Migrate, PostgreSQL, Jinja2 para templates e a biblioteca Argon2 para hashing seguro de senhas.

## Arquitetura e Estrutura

### Organização de pastas
- `run.py` – ponto de entrada da aplicação; inicializa a instância Flask via `create_app`.
- `app/` – pacote principal da aplicação.
  - `__init__.py` – fábrica de aplicação, configuração de extensões, registro de blueprints e criação do banco.
  - `run.py` – atalho para executar a aplicação a partir do pacote.
  - `models/` – modelos de domínio mapeados pelo SQLAlchemy (`User`, `Caregiver`, `Responsible`, `Elderly`, `Contract`).
  - `routes/` – blueprints que expõem rotas web e API (home, login, registro, dashboards e integração ViaCEP).
  - `services/` – camada de serviço com regras de negócio e integração externa (autenticação, CRUDs, ViaCEP).
  - `templates/` e `static/` – front-end baseado em Jinja2 (HTML/CSS/JS).
- `requirements.txt` – dependências Python do projeto.
- `migrations/` – diretório de controle de schema do Flask-Migrate (seeds/migrations gerados).
- `vercel.json` – configuração de deployment.

### Fluxo de dados principal
```mermaid
graph TD
    A[Cliente HTTP] --> B[Blueprints em app/routes]
    B --> C[Serviços (app/services)]
    C --> D[Modelos SQLAlchemy (app/models)]
    D -->|ORM| E[(Banco de Dados PostgreSQL)]
    C --> F[APIs Externas (ViaCEP)]
    B --> G[Templates Jinja2]
```

### Interação entre módulos
- **Blueprints** recebem requisições HTTP, validam entrada básica e delegam regras para a camada de serviços.
- **Serviços** encapsulam lógica de negócio, consultas e persistência usando os modelos SQLAlchemy; também gerenciam sessão de autenticação e integrações externas (ViaCEP).
- **Modelos** representam as entidades principais com relacionamentos bidirecionais (users-caretakers/responsibles, responsibles-elderly, contracts com cuidadores e responsáveis). Constraints em nível de banco reforçam domínios (gênero, status de contrato, métodos de contato, etc.).
- **Templates** consomem dados fornecidos pelos blueprints para renderizar páginas dinâmicas.

## Pré-requisitos e Instalação

### Dependências principais
- **Python 3.11+** (recomendado).
- **PostgreSQL** (URL em `DATABASE_URL`).
- Bibliotecas Python: Flask, Flask-SQLAlchemy, Flask-Migrate, Flask-WTF, Flask-Security-Too, Argon2-CFFI, Requests, python-dotenv, entre outras listadas em `requirements.txt`.

### Variáveis de ambiente
- `SECRET_KEY` – chave de sessão Flask.
- `DATABASE_URL` – URL completa do banco PostgreSQL (ex.: `postgresql+psycopg2://user:pass@host:5432/db`).

### Passo a passo de instalação
1. **Clonar o repositório**
   ```bash
   git clone <url-do-repo>
   cd ProjectCare
   ```
2. **Criar ambiente virtual**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```
3. **Instalar dependências**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configurar variáveis**
   Crie um arquivo `.env` na raiz com:
   ```env
   SECRET_KEY=<sua_chave_segura>
   DATABASE_URL=postgresql+psycopg2://usuario:senha@localhost:5432/projectcare
   ```
5. **Inicializar banco**
   - Crie o banco no PostgreSQL conforme a URL.
   - (Opcional) Rodar migrações se existirem scripts em `migrations/`:
     ```bash
     flask db upgrade
     ```
   - A aplicação também executa `db.create_all()` na inicialização para garantir que tabelas existam.
6. **Executar a aplicação**
   ```bash
   python run.py  # ou flask run se FLASK_APP=run.py estiver definido
   ```

## Guia de Uso

### Execução local
- Inicie o servidor com `python run.py`; por padrão roda em `http://0.0.0.0:5000` em modo debug.
- A navegação principal ocorre pelas páginas:
  - `/` – home.
  - `/register` – criação de usuário e seleção de perfil (cuidador ou responsável).
  - `/login` – autenticação e seleção do perfil ativo.
  - `/caregivers/` – listagem de cuidadores.
  - `/caregivers/elderly` – listagem de idosos (para cuidadores).
  - `/responsible/my-elderly` – lista de idosos vinculados ao responsável logado.
  - `/contact/` e páginas legais em `/politica-privacidade`, `/termos-uso`, `/politica-cookies`.

### API ViaCEP
- **GET** `/api/cep/<cep>`: retorna dados de endereço para o CEP informado.
- **POST** `/api/cep` com JSON `{ "cep": "00000-000" }`: alternativa via POST.
- Resposta de sucesso:
  ```json
  { "success": true, "data": {"logradouro": "...", "bairro": "...", "localidade": "...", "uf": "..." } }
  ```
- Resposta de erro (exemplo de CEP inválido):
  ```json
  { "success": false, "error": "CEP deve conter exatamente 8 dígitos" }
  ```

## Documentação Técnica dos Módulos

### `run.py` (raiz)
- Inicializa o app via `create_app()` e ativa logs detalhados; executa servidor em modo debug e host público (0.0.0.0).

### `app/__init__.py`
- **create_app()**: configura Flask, carrega variáveis `.env`, valida `SECRET_KEY`/`DATABASE_URL`, inicializa `SQLAlchemy` e `Migrate`, cria tabelas, registra blueprints e injeta o template de navbar de acordo com sessão.

### Modelos (`app/models`)
- **User** (`user.py`): dados pessoais, contato, endereço; métodos `set_password` (hash Argon2) e `check_password`; relacionamentos um-para-um com `Caregiver` e `Responsible`. Constraints para gênero e unicidade de CPF/telefone/email.
- **Caregiver** (`caregiver.py`): perfil de cuidador com especialidade, experiência, educação, habilidades, disponibilidade e pretensão salarial; FK para `User`; relaciona-se com `Contract`.
- **Responsible** (`responsible.py`): perfil de responsável; dados de relacionamento, necessidades e método preferido de contato; relaciona-se com `Elderly` e `Contract`.
- **Elderly** (`elderly.py`): informações completas do idoso (dados pessoais, endereço, saúde, contatos de emergência); FK para `Responsible`.
- **Contract** (`contract.py`): dados de contrato entre responsável e cuidador, com datas, remuneração, condições e status controlado por constraint.

### Rotas (`app/routes`)
- **home.py**: blueprint `home` com rota `/` para página inicial.
- **caregivers.py**: lista cuidadores (`/caregivers/`) e idosos disponíveis (`/caregivers/elderly`) consultando serviços correspondentes.
- **contact.py**: rota `/contact/` para página de contato (ganchos comentados para submissão futura).
- **login.py**: fluxo de login, seleção de perfil ativo e logout; usa `AuthenticationService` e `UserService` para validação e gestão de sessão.
- **register.py**: cadastro de usuário, seleção de perfil, criação de perfis de cuidador, responsável e cadastro de idosos vinculados; coordena persistência via serviços e manipula sessão/flash.
- **responsible_dashboard.py**: rota `/responsible/my-elderly` que lista idosos do responsável autenticado.
- **api.py**: expõe endpoints REST para consulta de CEP via `ViaCepService` (GET e POST).
- **legal.py**: páginas de política de privacidade, termos de uso e cookies.

### Serviços (`app/services`)
- **AuthenticationService**: valida credenciais (`validate_credentials`), monta sessão (`setup_session`), identifica perfis do usuário (`get_user_profiles`), define redirecionamento pós-login e realiza logout (`clear_session`).
- **UserService**: valida unicidade e persiste usuários (`save`, `validate_user_creation`), além de consultas por ID/email/CPF/telefone.
- **CaregiverService**: salva e consulta cuidadores (`save`, `get_all`, `get_by_id`, `get_by_email`, `get_by_user_id`).
- **ResponsibleService**: salva e consulta responsáveis (`save`, `get_all`, `get_by_id`, `get_by_email`, `get_by_user_id`).
- **ElderlyService**: salva, lista e gerencia idosos (`save`, `get_all`, `get_by_user_id`, `get_by_responsible_id`, `find_elderly_by_responsible`, `exists_by_user_id`, `exists_by_responsible_id`, `count_by_responsible_id`, `update`, `delete`).
- **ViaCepService**: integra com a API ViaCEP para sanitizar, validar e consultar CEPs; retorna `ViaCepResult` com dados formatados ou mensagens de erro.

### Templates/Front-end
- Estrutura em `templates/` com páginas para home, login, registro de perfis, listagens, contato e políticas legais; `static/` contém ativos de estilo e scripts. (Conteúdo HTML/CSS não detalhado aqui.)

## Conclusão e Melhorias Futuras
1. **Corrigir imports ausentes nos serviços**: `CaregiverService`, `ResponsibleService` e `ElderlyService` utilizam `db` e classes de modelo sem importá-los explicitamente, o que gera erros em runtime; adicionar `from app import db` e imports das classes faltantes.
2. **Aprimorar validação de formulários**: substituir validações manuais por WTForms/Flask-WTF com CSRF e validações de tipo (datas, números, escolhas), elevando segurança e consistência.
3. **Fluxo de migrações robusto**: remover `db.create_all()` na inicialização em produção e confiar apenas em migrações versionadas (`flask db upgrade`) para evitar divergências de schema, além de adicionar scripts de seeding controlados.
