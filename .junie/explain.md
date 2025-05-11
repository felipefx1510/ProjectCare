# ProjectCare - Documentação Técnica

## Visão Geral

ProjectCare é uma aplicação web projetada para conectar cuidadores com pessoas idosas que necessitam de cuidados. A plataforma funciona como um marketplace onde pessoas responsáveis (familiares ou tutores) podem encontrar e contratar cuidadores qualificados para seus parentes idosos.

### Problema a Resolver

Muitas pessoas idosas necessitam de cuidados especializados, mas encontrar cuidadores qualificados pode ser um desafio para os familiares. O ProjectCare visa resolver este problema:

1. Fornecendo uma plataforma onde cuidadores podem se registrar e mostrar suas qualificações
2. Permitindo que pessoas responsáveis pesquisem e se conectem com cuidadores
3. Facilitando a criação e gestão de contratos de cuidados
4. Garantindo uma experiência de cuidado segura e confiável

## Tecnologias Utilizadas

### Tecnologias Principais

- **Flask**: Um framework web Python leve que fornece ferramentas e bibliotecas para construir aplicações web
  - Usado para roteamento, manipulação de requisições e renderização de templates
  - Blueprints são usados para organizar a aplicação em componentes modulares

- **SQLAlchemy**: Uma biblioteca de Mapeamento Objeto-Relacional (ORM) para Python
  - Permite interação com o banco de dados usando objetos Python em vez de SQL puro
  - Gerencia conexões, consultas e transações com o banco de dados

- **PostgreSQL**: Um sistema de banco de dados relacional poderoso e de código aberto
  - Armazena todos os dados da aplicação (usuários, cuidadores, contratos, etc.)
  - Fornece confiabilidade e suporte para consultas complexas

### Tecnologias Adicionais

- **Flask-Migrate**: Uma extensão que gerencia migrações de banco de dados SQLAlchemy
  - Usa Alembic internamente para gerenciar mudanças no esquema do banco de dados
  - Fornece comandos para criar e aplicar migrações

- **Jinja2**: Um motor de templates para Python
  - Usado para renderizar templates HTML com dados dinâmicos
  - Suporta herança de templates, loops, condicionais e mais

- **python-dotenv**: Uma biblioteca para carregar variáveis de ambiente de um arquivo .env
  - Usada para gerenciar configurações como strings de conexão com banco de dados e chaves secretas

## Estrutura do Projeto

### Diretórios e Arquivos de Nível Superior

- **app/**: O pacote principal da aplicação
  - Contém todo o código da aplicação, incluindo modelos, rotas e templates

- **migrations/**: Contém arquivos de migração do banco de dados
  - Gerados e gerenciados pelo Flask-Migrate
  - Rastreia mudanças no esquema do banco de dados ao longo do tempo

- **test/**: Contém arquivos de teste para a aplicação
  - Usa o framework unittest para testes
  - Inclui testes para modelos e outros componentes

- **.junie/**: Diretório de documentação
  - Contém diretrizes e explicações para desenvolvedores

- **config.py**: Arquivo de configuração (atualmente comentado)
  - Normalmente conteria configurações da aplicação

- **requirements.txt**: Lista todas as dependências Python
  - Usado para instalar pacotes necessários com pip

- **.env**: Arquivo de variáveis de ambiente (não rastreado no git)
  - Contém configurações sensíveis como credenciais de banco de dados e chaves secretas

### Estrutura do Diretório App

- **models/**: Modelos de banco de dados
  - Cada arquivo define uma tabela diferente do banco de dados e seus relacionamentos

- **routes/**: Manipuladores de rotas (controladores)
  - Organizados em blueprints para diferentes partes da aplicação

- **services/**: Lógica de negócios
  - Contém serviços que lidam com operações nos modelos

- **static/**: Arquivos estáticos (CSS, JavaScript, imagens)
  - Servidos diretamente ao cliente

- **templates/**: Templates HTML
  - Organizados por blueprint/funcionalidade

- **__init__.py**: Factory da aplicação
  - Cria e configura a aplicação Flask

- **run.py**: Ponto de entrada para executar a aplicação

## Explicação Arquivo por Arquivo

### Pacote App

#### app/__init__.py

Este arquivo contém a função factory `create_app()` que:
- Carrega variáveis de ambiente do arquivo `.env` usando `load_dotenv(override=True)`
- Verifica se as variáveis de ambiente obrigatórias ('SECRET_KEY', 'DATABASE_URL') estão definidas
- Cria uma nova aplicação Flask
- Configura a aplicação (chave secreta, URI do banco de dados, etc.)
- Inicializa extensões (SQLAlchemy, Flask-Migrate)
- Cria tabelas do banco de dados se elas não existirem
- Registra blueprints para diferentes partes da aplicação

```python
def create_app():
    app = Flask(__name__)

    # Verifica se as variáveis obrigatórias estão definidas
    required_env_vars = ['SECRET_KEY', 'DATABASE_URL']
    for var in required_env_vars:
        if not os.getenv(var):
            raise RuntimeError(f"A variável de ambiente '{var}' não está definida. Verifique o arquivo .env.")

    # Configuração
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar extensões
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        db.create_all()  # Cria as tabelas no banco de dados se não existirem

    # Registrar blueprints
    # ...

    return app
```

#### app/run.py

Um script simples que cria a aplicação e a executa em modo de desenvolvimento:

```python
from . import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
```

### Modelos

#### app/models/caregiver.py

Define o modelo `Caregiver` (Cuidador), representando os prestadores de cuidados de saúde no sistema:
- Informações pessoais (nome, CPF, telefone, email, endereço)
- Informações profissionais (especialidade, experiência, educação, área de expertise, habilidades, avaliação)
- Relacionamento com contratos

```python
class Caregiver(db.Model):
    __tablename__ = "caregiver"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    # ... outros campos ...

    # Relacionamento com contratos
    contracts = db.relationship("Contract", back_populates="caregiver", cascade="all, delete-orphan")
```

#### app/models/elderly.py

Define o modelo `Elderly` (Idoso), representando pessoas idosas que precisam de cuidados:
- Informações pessoais (nome, data de nascimento, gênero, endereço)
- Relacionamento com pessoas responsáveis

```python
class Elderly(db.Model):
    __tablename__ = "elderly"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    # ... outros campos ...

    # Relacionamento com pessoas responsáveis
    responsible_id = db.Column(db.Integer, db.ForeignKey("responsible.id"), nullable=False)
    responsible = db.relationship("Responsible", back_populates="elderly")
```

#### app/models/responsible.py

Define o modelo `Responsible` (Responsável), representando pessoas responsáveis por indivíduos idosos:
- Informações pessoais (nome, CPF, telefone, email)
- Relacionamentos com pessoas idosas e contratos

```python
class Responsible(db.Model):
    __tablename__ = "responsible"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    # ... outros campos ...

    # Relacionamentos
    elderly = db.relationship("Elderly", back_populates="responsible", cascade="all, delete-orphan")
    contracts = db.relationship("Contract", back_populates="responsible", cascade="all, delete-orphan")
```

#### app/models/contract.py

Define o modelo `Contract` (Contrato), representando acordos entre cuidadores e pessoas responsáveis:
- Detalhes do contrato (data_inicio, data_fim)
- Relacionamentos com cuidadores e pessoas responsáveis

```python
class Contract(db.Model):
    __tablename__ = "contract"
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)

    # Relacionamentos
    responsible_id = db.Column(db.Integer, db.ForeignKey("responsible.id"), nullable=False)
    caregiver_id = db.Column(db.Integer, db.ForeignKey("caregiver.id"), nullable=False)
    responsible = db.relationship("Responsible", back_populates="contracts")
    caregiver = db.relationship("Caregiver", back_populates="contracts")
```

### Rotas (Blueprints)

#### app/routes/home.py

Define o blueprint para a página inicial:
- Cria um blueprint com o prefixo de URL "/"
- Define uma rota para a URL raiz que renderiza o template home

```python
home_bp = Blueprint("home", __name__, url_prefix="/")

@home_bp.route("/", methods=["GET"])
def home():
    return render_template("home/home.html")
```

#### app/routes/caregivers.py

Define o blueprint para rotas relacionadas a cuidadores:
- Cria um blueprint com o prefixo de URL "/caregivers"
- Define uma rota para listar todos os cuidadores

```python
caregivers_bp = Blueprint("caregivers", __name__, url_prefix="/caregivers")

@caregivers_bp.route("/", methods=["GET"])
def list_caregivers():
    caregivers = caregiver_service.get_all_caregivers()
    return render_template("caregivers/list.html", caregivers=caregivers)
```

#### app/routes/contact.py

Define o blueprint para a página de contato:
- Cria um blueprint com o prefixo de URL "/contact"
- Define uma rota para a página de contato

```python
contact_bp = Blueprint("contact", __name__, url_prefix="/contact")

@contact_bp.route("/", methods=["GET"])
def contact():
    return render_template("contact/contact.html")
```

#### app/routes/login.py

Define o blueprint para autenticação de usuários:
- Cria um blueprint com o prefixo de URL "/login"
- Define uma rota para a página de login que lida com requisições GET e POST
- Atualmente, a lógica de autenticação não está totalmente implementada

```python
login_bp = Blueprint("login", __name__, url_prefix="/login")

@login_bp.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # A lógica de autenticação iria aqui
        return redirect(url_for('home.home'))
    return render_template("login/login.html")
```

#### app/routes/register.py

Define o blueprint para registro de usuários:
- Cria um blueprint com o prefixo de URL "/register"
- Define rotas para registrar pessoas responsáveis e cuidadores

```python
register_bp = Blueprint("register", __name__, url_prefix="/register")

@register_bp.route("/", methods=["GET", "POST"])
def register():
    return render_template("login/register.html")

@register_bp.route('/responsible', methods=['POST'])
def register_responsible():
    # Obter dados do formulário e criar um objeto Responsible
    # ...
    return redirect(url_for('login.login'))

@register_bp.route('/caregiver', methods=['POST'])
def register_caregiver():
    # Obter dados do formulário e criar um objeto Caregiver
    # ...
    return redirect(url_for('login.login'))
```

### Templates

A aplicação usa templates Jinja2 organizados por funcionalidade:
- **home/home.html**: O template da página inicial
- **caregivers/list.html**: Template para listar cuidadores
- **contact/contact.html**: O template da página de contato
- **login/login.html**: O template da página de login
- **login/register.html**: O template da página de registro
- **fragments/navbar.html**: Um template reutilizável de barra de navegação

### Arquivos Estáticos

A aplicação inclui arquivos estáticos como imagens no diretório `app/static/images/`.

## Estrutura do Banco de Dados

### Modelos e Relacionamentos

O banco de dados tem quatro tabelas principais:
1. **caregiver**: Armazena informações sobre cuidadores
2. **elderly**: Armazena informações sobre pessoas idosas
3. **responsible**: Armazena informações sobre pessoas responsáveis
4. **contract**: Armazena informações sobre contratos entre cuidadores e pessoas responsáveis

Os relacionamentos entre essas tabelas são:
- Uma pessoa responsável pode estar associada a várias pessoas idosas (um-para-muitos)
- Uma pessoa responsável pode ter vários contratos (um-para-muitos)
- Um cuidador pode ter vários contratos (um-para-muitos)
- Um contrato conecta um cuidador com uma pessoa responsável (muitos-para-um para ambos)

### Migrações

As migrações de banco de dados são gerenciadas usando Flask-Migrate:
- Arquivos de migração são armazenados no diretório `migrations/versions/`
- Cada arquivo de migração representa uma mudança no esquema do banco de dados
- Migrações podem ser criadas usando `flask db migrate -m "descrição"`
- Migrações podem ser aplicadas usando `flask db upgrade`

## Fluxo de Autenticação

O fluxo de autenticação ainda não está totalmente implementado, mas a estrutura está no lugar:
1. Usuários (cuidadores ou pessoas responsáveis) se registram através da página de registro
2. Os dados de registro são processados pelo manipulador de rota apropriado
3. As informações do usuário são salvas no banco de dados
4. Os usuários são redirecionados para a página de login
5. A página de login autenticaria os usuários (não implementado ainda)
6. Após autenticação bem-sucedida, os usuários seriam redirecionados para a página inicial

## Configuração

A aplicação usa variáveis de ambiente para configuração:
- **DATABASE_URL**: A string de conexão PostgreSQL
- **SECRET_KEY**: Uma chave secreta para proteger sessões e cookies

Essas variáveis podem ser definidas em um arquivo `.env` no diretório raiz do projeto.

Se o `DATABASE_URL` não estiver definido, a aplicação usa uma string de conexão padrão:
```
postgresql://postgres:@localhost:5432/ProjectCare
```

## Executando a Aplicação

### Desenvolvimento

Para executar a aplicação em modo de desenvolvimento:
1. Crie e ative um ambiente virtual:
   ```
   python -m venv .venv
   .venv\Scripts\activate
   ```
2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```
3. Configure variáveis de ambiente em um arquivo `.env`
4. Execute a aplicação:
   ```
   python -m app.run
   ```

A aplicação iniciará em modo de depuração, que fornece:
- Recarregamento automático quando o código muda
- Páginas de erro detalhadas
- O depurador interativo

### Produção

Para implantação em produção, você normalmente:
1. Usaria um servidor WSGI como Gunicorn em vez do servidor Flask embutido
2. Definiria `debug=False` para desativar o depurador interativo
3. Usaria variáveis de ambiente para configuração em vez de um arquivo `.env`
4. Consideraria usar um proxy reverso como Nginx na frente da aplicação

## Áreas para Melhoria

1. **Autenticação**: O sistema de autenticação não está totalmente implementado. Considere usar Flask-Login ou outra biblioteca de autenticação.

2. **Segurança de Senhas**: As senhas atualmente são armazenadas em texto simples. Elas devem ser criptografadas usando uma biblioteca como as funções de segurança do Werkzeug ou passlib.

3. **Validação de Formulários**: Não há validação para entradas de formulário. Considere usar Flask-WTF para manipulação e validação de formulários.

4. **Tratamento de Erros**: A aplicação não possui tratamento abrangente de erros. Adicione blocos try-except e páginas de erro.

5. **Testes**: Embora exista um diretório de testes, testes mais abrangentes melhorariam a confiabilidade.

6. **Configuração**: Considere usar o arquivo `config.py` comentado para uma abordagem de configuração mais estruturada.

7. **Documentação de API**: Se a aplicação expõe APIs, considere adicionar documentação usando Swagger/OpenAPI.

8. **Logging**: Adicione logging para ajudar na depuração e monitoramento.

9. **Framework Frontend**: Considere usar um framework frontend como React ou Vue.js para uma experiência de usuário mais interativa.

10. **Containerização**: Considere usar Docker para containerizar a aplicação para facilitar a implantação.
