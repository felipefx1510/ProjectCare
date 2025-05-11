# Documentação de Orientação - ProjectCare

## Visão Geral do Projeto

O ProjectCare é uma aplicação web desenvolvida em Flask que conecta responsáveis por idosos a cuidadores profissionais. O sistema permite o cadastro de cuidadores e responsáveis, gerenciamento de contratos e acompanhamento de idosos. A aplicação utiliza uma arquitetura em camadas com modelos, serviços e rotas bem definidos.

## Estrutura do Projeto

```
app/
├── __init__.py                # Inicialização da aplicação Flask
├── models/                    # Modelos de dados (SQLAlchemy)
│   ├── __init__.py
│   ├── caregiver.py           # Modelo de cuidador
│   ├── contract.py            # Modelo de contrato
│   ├── elderly.py             # Modelo de idoso
│   └── responsible.py         # Modelo de responsável
├── routes/                    # Rotas da aplicação (Blueprints Flask)
│   ├── __init__.py
│   ├── caregivers.py          # Rotas para cuidadores
│   ├── contact.py             # Rotas para página de contato
│   ├── home.py                # Rotas para página inicial
│   ├── login.py               # Rotas para autenticação
│   └── register.py            # Rotas para registro de usuários
├── services/                  # Camada de serviço para lógica de negócios
│   ├── __init__.py
│   ├── caregiver_service.py   # Serviços para cuidadores
│   └── responsible_service.py # Serviços para responsáveis
├── static/                    # Arquivos estáticos
│   └── images/                # Imagens utilizadas na aplicação
└── templates/                 # Templates HTML (Jinja2)
    ├── caregivers/            # Templates para cuidadores
    ├── contact/               # Templates para contato
    ├── fragments/             # Fragmentos de templates reutilizáveis
    ├── home/                  # Templates para página inicial
    └── login/                 # Templates para login e registro
migrations/                    # Migrações de banco de dados
├── versions/                  # Versões das migrações
│   └── 3c65ead452be_criação_inicial_das_tabelas.py
test/                          # Testes automatizados
requirements.txt               # Dependências do projeto
```

## Análise Detalhada dos Arquivos

### Inicialização da Aplicação

#### `app/__init__.py`

Este arquivo é responsável pela inicialização da aplicação Flask. Ele utiliza o padrão de fábrica de aplicação (application factory pattern), que é uma prática recomendada para aplicações Flask.

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

load_dotenv()  # Carrega variáveis de ambiente do arquivo .env

db = SQLAlchemy()  # Instância do SQLAlchemy para operações de banco de dados
migrate = Migrate()  # Instância do Flask-Migrate para migrações

def create_app():
    app = Flask(__name__)  # Cria uma instância da aplicação Flask

    # Configuração do app
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev_key')  # Chave secreta para sessões
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:@localhost:5432/ProjectCare')  # URL de conexão com o banco de dados
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desativa o rastreamento de modificações do SQLAlchemy

    # Inicialização das extensões
    db.init_app(app)  # Inicializa o SQLAlchemy com a aplicação
    migrate.init_app(app, db)  # Inicializa o Flask-Migrate com a aplicação e o SQLAlchemy

    # Cria as tabelas no banco de dados se não existirem
    with app.app_context():
        db.create_all()

    # Registro de blueprints (módulos da aplicação)
    from app.routes.home import home_bp
    from app.routes.caregivers import caregivers_bp
    from app.routes.contact import contact_bp
    from app.routes.login import login_bp
    from app.routes.register import register_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(caregivers_bp)
    app.register_blueprint(contact_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(register_bp)

    return app  # Retorna a aplicação configurada
```

**Detalhes importantes:**
- O arquivo utiliza `load_dotenv()` para carregar variáveis de ambiente de um arquivo `.env`, permitindo configuração flexível.
- A aplicação é configurada com uma chave secreta (`SECRET_KEY`) para sessões e cookies.
- A URL de conexão com o banco de dados (`SQLALCHEMY_DATABASE_URI`) é configurada a partir de variáveis de ambiente ou usa um valor padrão.
- As extensões SQLAlchemy e Flask-Migrate são inicializadas com a aplicação.
- As tabelas do banco de dados são criadas automaticamente se não existirem.
- Vários blueprints são registrados para organizar as rotas da aplicação.

### Modelos de Dados

#### `app/models/caregiver.py`

Este arquivo define o modelo `Caregiver` (Cuidador) que representa os profissionais de saúde no sistema.

```python
from datetime import datetime
from app import db

class Caregiver(db.Model):
    __tablename__ = "caregiver"  # Nome da tabela no banco de dados
    id = db.Column(db.Integer, primary_key=True)  # Chave primária
    name = db.Column(db.String(100), nullable=False)  # Nome do cuidador
    cpf = db.Column(db.String(14), unique=True, nullable=False)  # CPF (único)
    phone = db.Column(db.String(20), nullable=False)  # Telefone
    email = db.Column(db.String(100), unique=True, nullable=False)  # Email (único)
    password = db.Column(db.String(200), nullable=False)  # Senha
    specialty = db.Column(db.String(100), nullable=False)  # Especialidade
    experience = db.Column(db.Integer, nullable=False)  # Experiência em anos
    education = db.Column(db.String(100), nullable=False)  # Formação
    expertise_area = db.Column(db.String(100), nullable=False)  # Área de atuação
    skills = db.Column(db.String(200), nullable=False)  # Habilidades
    rating = db.Column(db.Float, nullable=False)  # Avaliação
    address = db.Column(db.String(200), nullable=False)  # Endereço
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Data de criação

    # Relacionamento com contratos
    contracts = db.relationship("Contract", back_populates="caregiver", cascade="all, delete-orphan")

    def __init__(self, name, cpf, phone, email, password, specialty, experience, education, expertise_area, skills, rating, address):
        self.name = name
        self.cpf = cpf
        self.phone = phone
        self.email = email
        self.password = password  # Nota: a senha deve ser hash antes de armazenar
        self.specialty = specialty
        self.experience = experience
        self.education = education
        self.expertise_area = expertise_area
        self.skills = skills
        self.rating = rating
        self.address = address

    def __repr__(self):
        return f"<Caregiver {self.name}>"  # Representação em string do objeto
```

**Detalhes importantes:**
- O modelo herda de `db.Model`, que é a classe base do SQLAlchemy para modelos.
- Cada coluna é definida com seu tipo, tamanho e restrições (como `nullable=False` para campos obrigatórios).
- Os campos `cpf` e `email` têm a restrição `unique=True`, garantindo que não haja duplicatas.
- O campo `created_at` tem um valor padrão que é a data e hora atual.
- Há um relacionamento com o modelo `Contract`, permitindo acessar os contratos de um cuidador.
- O método `__init__` inicializa um objeto com os valores fornecidos.
- O método `__repr__` fornece uma representação em string do objeto para depuração.

#### `app/models/contract.py`

Este arquivo define o modelo `Contract` (Contrato) que representa os acordos entre cuidadores e responsáveis.

```python
from datetime import datetime
from app import db

class Contract(db.Model):
    __tablename__ = "contract"  # Nome da tabela no banco de dados
    id = db.Column(db.Integer, primary_key=True)  # Chave primária
    start_date = db.Column(db.DateTime, nullable=False)  # Data de início
    end_date = db.Column(db.DateTime, nullable=False)  # Data de término

    # Chaves estrangeiras
    responsible_id = db.Column(db.Integer, db.ForeignKey("responsible.id"), nullable=False)  # ID do responsável
    caregiver_id = db.Column(db.Integer, db.ForeignKey("caregiver.id"), nullable=False)  # ID do cuidador

    # Relacionamentos
    responsible = db.relationship("Responsible", back_populates="contracts")  # Relação com responsável
    caregiver = db.relationship("Caregiver", back_populates="contracts")  # Relação com cuidador

    def __init__(self, responsible, caregiver, start_date=None, end_date=None):
        self.responsible = responsible
        self.caregiver = caregiver
        self.start_date = start_date
        self.end_date = end_date

    def __repr__(self):
        return f"<Contract {self.id}: {self.caregiver.name} - {self.responsible.name}>"  # Representação em string
```

**Detalhes importantes:**
- O modelo tem campos para as datas de início e término do contrato.
- Há chaves estrangeiras para os modelos `Responsible` e `Caregiver`.
- Os relacionamentos são bidirecionais, permitindo acessar o responsável e o cuidador a partir do contrato, e vice-versa.
- O método `__init__` aceita objetos `responsible` e `caregiver` diretamente, em vez de IDs.

#### `app/models/elderly.py`

Este arquivo define o modelo `Elderly` (Idoso) que representa as pessoas idosas sob cuidados.

```python
from datetime import date
from app import db

class Elderly(db.Model):
    __tablename__ = "elderly"  # Nome da tabela no banco de dados
    id = db.Column(db.Integer, primary_key=True)  # Chave primária
    name = db.Column(db.String(100), nullable=False)  # Nome do idoso
    birthdate = db.Column(db.Date, nullable=False)  # Data de nascimento
    gender = db.Column(db.String(10), nullable=False)  # Gênero
    address = db.Column(db.String(200), nullable=False)  # Endereço

    # Chave estrangeira
    responsible_id = db.Column(db.Integer, db.ForeignKey("responsible.id"), nullable=False)  # ID do responsável

    # Relacionamento
    responsible = db.relationship("Responsible", back_populates="elderly")  # Relação com responsável

    def __init__(self, name, birthdate, gender, address, responsible=None):
        self.name = name
        self.birthdate = birthdate
        self.gender = gender
        self.address = address
        self.responsible = responsible

    def __repr__(self):
        return f"<Elderly {self.name}>"  # Representação em string
```

**Detalhes importantes:**
- O modelo armazena informações básicas sobre o idoso, como nome, data de nascimento, gênero e endereço.
- Há uma chave estrangeira para o modelo `Responsible`, indicando quem é o responsável pelo idoso.
- O relacionamento é bidirecional, permitindo acessar o responsável a partir do idoso, e vice-versa.

#### `app/models/responsible.py`

Este arquivo define o modelo `Responsible` (Responsável) que representa as pessoas responsáveis pelos idosos.

```python
from app import db

class Responsible(db.Model):
    __tablename__ = "responsible"  # Nome da tabela no banco de dados

    id = db.Column(db.Integer, primary_key=True)  # Chave primária
    name = db.Column(db.String(100), nullable=False)  # Nome do responsável
    cpf = db.Column(db.String(14), unique=True, nullable=False)  # CPF (único)
    phone = db.Column(db.String(20), nullable=False)  # Telefone
    email = db.Column(db.String(100), unique=True, nullable=False)  # Email (único)
    password = db.Column(db.String(200), nullable=False)  # Senha

    # Relacionamentos
    elderly = db.relationship("Elderly", back_populates="responsible", cascade="all, delete-orphan")  # Relação com idosos
    contracts = db.relationship("Contract", back_populates="responsible", cascade="all, delete-orphan")  # Relação com contratos

    def __init__(self, name, cpf, phone, email, password):
        self.name = name
        self.cpf = cpf
        self.phone = phone
        self.email = email
        self.password = password  # Nota: a senha deve ser hash antes de armazenar

    def __repr__(self):
        return f"<Responsible {self.name}>"  # Representação em string
```

**Detalhes importantes:**
- O modelo armazena informações básicas sobre o responsável, como nome, CPF, telefone, email e senha.
- Os campos `cpf` e `email` têm a restrição `unique=True`, garantindo que não haja duplicatas.
- Há relacionamentos com os modelos `Elderly` e `Contract`, permitindo acessar os idosos e contratos de um responsável.
- A opção `cascade="all, delete-orphan"` garante que quando um responsável é excluído, seus idosos e contratos também são excluídos.

### Serviços

#### `app/services/__init__.py`

Este arquivo inicializa os serviços da aplicação, criando instâncias das classes de serviço.

```python
# Este arquivo torna o diretório services um pacote Python
from app.services.caregiver_service import CaregiverService
from app.services.responsible_service import ResponsibleService

# Cria instâncias de serviço
caregiver_service = CaregiverService()
responsible_service = ResponsibleService()
```

**Detalhes importantes:**
- O arquivo importa as classes de serviço e cria instâncias delas.
- Essas instâncias são usadas em toda a aplicação para acessar a lógica de negócios.

#### `app/services/caregiver_service.py`

Este arquivo define o serviço `CaregiverService` que contém a lógica de negócios relacionada aos cuidadores.

```python
from app import db
from app.models.caregiver import Caregiver

class CaregiverService:
    def save(self, caregiver: Caregiver) -> None:
        """
        Salva um novo cuidador no banco de dados.
        """
        db.session.add(caregiver)
        db.session.commit()
        return caregiver

    def get_all_caregivers(self):
        """
        Recupera todos os cuidadores do banco de dados.
        """
        return Caregiver.query.all()

    def get_caregiver_by_id(self, caregiver_id: int):
        """
        Recupera um cuidador pelo seu ID.
        """
        return Caregiver.query.get(caregiver_id)

    def get_caregiver_by_email(self, email: str):
        """
        Recupera um cuidador pelo seu email.
        """
        return Caregiver.query.filter_by(email=email).first()
```

**Detalhes importantes:**
- O serviço fornece métodos para salvar um cuidador, obter todos os cuidadores, obter um cuidador por ID e obter um cuidador por email.
- Os métodos usam a API do SQLAlchemy para interagir com o banco de dados.
- O método `save` adiciona um cuidador à sessão do banco de dados e confirma a transação.
- Os outros métodos executam consultas no banco de dados para recuperar cuidadores.

#### `app/services/responsible_service.py`

Este arquivo define o serviço `ResponsibleService` que contém a lógica de negócios relacionada aos responsáveis.

```python
from app import db
from app.models.responsible import Responsible

class ResponsibleService:
    def save(self, responsible: Responsible):
        """
        Salva um novo responsável no banco de dados.
        """
        try:
            db.session.add(responsible)
            db.session.commit()
            return responsible
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao salvar no banco de dados: {e}")
            raise

    def get_all_responsibles(self):
        """
        Recupera todos os responsáveis do banco de dados.
        """
        return Responsible.query.all()

    def get_responsible_by_id(self, responsible_id: int):
        """
        Recupera um responsável pelo seu ID.
        """
        return Responsible.query.get(responsible_id)

    def get_responsible_by_email(self, email: str):
        """
        Recupera um responsável pelo seu email.
        """
        return Responsible.query.filter_by(email=email).first()
```

**Detalhes importantes:**
- O serviço fornece métodos semelhantes ao `CaregiverService`, mas para responsáveis.
- O método `save` inclui tratamento de exceções, fazendo rollback da transação em caso de erro.
- Os outros métodos são semelhantes aos do `CaregiverService`, mas para o modelo `Responsible`.

### Rotas

#### `app/routes/home.py`

Este arquivo define as rotas para a página inicial da aplicação.

```python
from flask import Blueprint, render_template

home_bp = Blueprint("home", __name__, url_prefix="/")

@home_bp.route("/", methods=["GET"])
def home():
    """
    Página inicial.
    """
    return render_template("home/home.html")
```

**Detalhes importantes:**
- O arquivo cria um Blueprint chamado "home" com o prefixo de URL "/".
- Define uma rota para a URL raiz ("/") que renderiza o template "home/home.html".
- O Blueprint é registrado na aplicação principal em `app/__init__.py`.

#### `app/routes/caregivers.py`

Este arquivo define as rotas relacionadas aos cuidadores.

```python
from flask import Blueprint, render_template
from app.services import caregiver_service

caregivers_bp = Blueprint("caregivers", __name__, url_prefix="/caregivers")

@caregivers_bp.route("/", methods=["GET"])
def list_caregivers():
    """
    Lista todos os cuidadores.
    """
    caregivers = caregiver_service.get_all_caregivers()
    return render_template("caregivers/list.html", caregivers=caregivers)
```

**Detalhes importantes:**
- O arquivo cria um Blueprint chamado "caregivers" com o prefixo de URL "/caregivers".
- Define uma rota para listar todos os cuidadores que usa o serviço `caregiver_service` para obter os dados.
- Os cuidadores são passados para o template "caregivers/list.html" para renderização.

#### `app/routes/contact.py`

Este arquivo define as rotas para a página de contato.

```python
from flask import Blueprint, render_template

contact_bp = Blueprint("contact", __name__, url_prefix="/contact")

@contact_bp.route("/", methods=["GET"])
def contact():
    """
    Página de contato.
    """
    return render_template("contact/contact.html")
```

**Detalhes importantes:**
- O arquivo cria um Blueprint chamado "contact" com o prefixo de URL "/contact".
- Define uma rota para a página de contato que renderiza o template "contact/contact.html".

#### `app/routes/login.py`

Este arquivo define as rotas para autenticação de usuários.

```python
from flask import Blueprint, render_template, request, redirect, url_for

login_bp = Blueprint("login", __name__, url_prefix="/login")

@login_bp.route("/", methods=["GET", "POST"])
def login():
    """
    Página de login.
    """
    if request.method == "POST":
        # Aqui você pode adicionar a lógica de autenticação
        # Por enquanto, redireciona para a página inicial após o login
        return redirect(url_for('home.home'))

    # Retorna o template de login para o método GET
    return render_template("login/login.html")
```

**Detalhes importantes:**
- O arquivo cria um Blueprint chamado "login" com o prefixo de URL "/login".
- Define uma rota que lida com requisições GET e POST.
- Para requisições GET, renderiza o template de login.
- Para requisições POST, atualmente apenas redireciona para a página inicial (a lógica de autenticação ainda não está implementada).

#### `app/routes/register.py`

Este arquivo define as rotas para registro de usuários.

```python
from flask import Blueprint, render_template, request, redirect, url_for
from app.models.caregiver import Caregiver
from app.models.responsible import Responsible
from app.services import caregiver_service, responsible_service

register_bp = Blueprint("register", __name__, url_prefix="/register")

@register_bp.route("/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        pass
    return render_template("login/register.html")

@register_bp.route('/responsible', methods=['POST'])
def register_responsible():
    """
    Registra um novo responsável.
    """
    name = request.form.get('name')
    cpf = request.form.get('cpf')
    phone = request.form.get('phone')
    email = request.form.get('email')
    password = request.form.get('password')

    responsible = Responsible(name=name, cpf=cpf, phone=phone, email=email, password=password)
    responsible_service.save(responsible)

    return redirect(url_for('login.login'))

@register_bp.route('/caregiver', methods=['POST'])
def register_caregiver():
    """
    Registra um novo cuidador.
    """
    name = request.form.get('name')
    cpf = request.form.get('cpf')
    phone = request.form.get('phone')
    email = request.form.get('email')
    password = request.form.get('password')
    specialty = request.form.get('specialty')
    experience = request.form.get('experience')
    education = request.form.get('education')
    expertise_area = request.form.get('expertise')
    skills = request.form.get('skills')

    caregiver = Caregiver(
        name=name,
        cpf=cpf,
        phone=phone,
        email=email,
        password=password,
        specialty=specialty,
        experience=experience,
        education=education,
        expertise_area=expertise_area,
        skills=skills,
        rating=0.0,
        address=""
    )

    caregiver_service.save(caregiver)
    # Redireciona para a página de login após o registro bem-sucedido
    return redirect(url_for('login.login'))
```

**Detalhes importantes:**
- O arquivo cria um Blueprint chamado "register" com o prefixo de URL "/register".
- Define três rotas:
  1. Uma rota principal que renderiza o template de registro
  2. Uma rota para registrar responsáveis que coleta dados do formulário e cria um novo objeto `Responsible`
  3. Uma rota para registrar cuidadores que coleta dados do formulário e cria um novo objeto `Caregiver`
- Ambas as rotas de registro usam seus respectivos serviços para salvar o novo usuário no banco de dados.
- Após o registro bem-sucedido, o usuário é redirecionado para a página de login.

### Templates

#### `app/templates/home/home.html`

Este template define a estrutura da página inicial da aplicação.

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Cuidados Dedicados</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>

{% include 'fragments/navbar.html' %}

<header class="bg-primary text-white text-center py-5">
    <div class="container">
        <h1 class="display-5">Encontre Profissionais de Saúde para Cuidar de Quem Você Ama</h1>
        <p class="lead mt-3">Conectamos famílias a profissionais dedicados ao cuidado de idosos com carinho e respeito.</p>
    </div>
</header>

<section class="py-5">
    <div class="container">
        <h2 class="mb-4 text-center">Profissionais em Destaque</h2>
        <div class="row row-cols-1 row-cols-md-3 g-4">
            <!-- Cards de profissionais -->
            <!-- ... (código omitido para brevidade) ... -->
        </div>
    </div>
</section>

<footer class="bg-light text-center py-4 mt-5">
    <div class="container">
        <p class="mb-0">© 2025 Cuidados Dedicados. Todos os direitos reservados.</p>
    </div>
</footer>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

**Detalhes importantes:**
- O template usa Bootstrap para estilização.
- Inclui o fragmento de template `navbar.html` para a barra de navegação.
- Tem um cabeçalho com título e descrição, uma seção para mostrar profissionais em destaque, e um rodapé.
- Usa a sintaxe Jinja2 para inclusão de templates e geração de URLs.

#### `app/templates/fragments/navbar.html`

Este fragmento de template define a barra de navegação usada em toda a aplicação.

```html
<!DOCTYPE html>
<html>
<head>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css" rel="stylesheet">
</head>
<body>
<nav class="navbar navbar-expand-lg navbar-light bg-light shadow-sm px-4 py-2">
    <div class="container">
        <a class="navbar-brand fw-bold text-primary" href="#">ProjectCare</a>

        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
            <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse justify-content-between" id="navbarNav">
            <ul class="navbar-nav">
                <li class="nav-item">
                    <a class="nav-link" href="{{ url_for('home.home') }}">Home Care</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="{{ url_for('contact.contact') }}">Contato</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="{{ url_for('caregivers.list_caregivers') }}">Ver Cuidadores</a>
                </li>
            </ul>

            <div class="d-flex align-items-center">
                <span class="me-3 text-muted"><i class="bi bi-telephone-fill"></i> (82) 9 8131-6407</span>
                <a href="https://wa.me/5582981316407" class="btn btn-success btn-sm me-2" target="_blank">
                    <i class="bi bi-whatsapp"></i> WhatsApp
                </a>
                <a href="{{ url_for('login.login') }}" class="btn btn-outline-primary btn-sm me-2">Login</a>
                <a href="{{ url_for('register.register') }}" class="btn btn-primary btn-sm">Cadastro</a>
            </div>
        </div>
    </div>
</nav>
```

**Detalhes importantes:**
- O fragmento define uma barra de navegação Bootstrap com links para as principais páginas da aplicação.
- Usa a função `url_for()` do Jinja2 para gerar URLs com base nos nomes das rotas, o que é uma boa prática.
- Inclui links para contato via WhatsApp e telefone.
- Tem botões para login e cadastro no canto direito.

#### `app/templates/caregivers/list.html`

Este template exibe uma lista de cuidadores cadastrados.

```html
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Lista de Cuidadores</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
{% include 'fragments/navbar.html' %}

<div class="container mt-5">
    <h2 class="mb-4 text-center">Cuidadores Cadastrados</h2>

    <table class="table table-bordered table-hover">
        <thead class="table-primary">
        <tr>
            <th>ID</th>
            <th>Nome</th>
            <th>Telefone</th>
        </tr>
        </thead>
        <tbody>
        {% for caregiver in caregivers %}
        <tr>
            <td>{{ caregiver.id }}</td>
            <td>{{ caregiver.name }}</td>
            <td>{{ caregiver.phone }}</td>
        </tr>
        {% endfor %}
        </tbody>
    </table>
</div>
```

**Detalhes importantes:**
- O template exibe uma tabela com os cuidadores cadastrados.
- Usa um loop `for` do Jinja2 para iterar sobre a lista de cuidadores passada pela rota.
- Para cada cuidador, exibe o ID, nome e telefone.
- Inclui o fragmento de navbar para manter a consistência da navegação.

#### `app/templates/contact/contact.html`

Este template exibe a página de contato com informações sobre os criadores do projeto.

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Contato - ProjectCare</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
{% include 'fragments/navbar.html' %}

<div class="container mt-5">
    <h2 class="text-center mb-4">Nosso Contato</h2>

    <div class="row mb-4">
        <div class="col-md-6 text-center">
            <img src="{{ url_for('static', filename='images/breno.jpg') }}" class="rounded-circle mb-2" alt="Breno Siqueira" width="150" height="150">
            <h5>Breno Siqueira</h5>
            <p><strong>Email:</strong> brenosiqueira@hotmail.com</p>
            <p><strong>Telefone:</strong> 99 9 9999 9999</p>
        </div>
        <div class="col-md-6 text-center">
            <img src="{{ url_for('static', filename='images/felipe.jpg') }}" class="rounded-circle mb-2" alt="Felipe Felix" width="150" height="150">
            <h5>Felipe Felix</h5>
            <p><strong>Email:</strong> felipefelix@hotmail.com</p>
            <p><strong>Telefone:</strong> 99 9 9999 9999</p>
        </div>
    </div>

    <div class="mb-5">
        <h4 class="text-center mb-3">Sobre o Projeto</h4>
        <textarea class="form-control" rows="5" readonly>
ProjectCare é um sistema voltado para conectar responsáveis por idosos a cuidadores profissionais. Com foco em facilitar o processo de contratação e acompanhar o bem-estar dos idosos, o sistema permite cadastramento, avaliações, e gerenciamento de contratos de forma simples e intuitiva.
        </textarea>
    </div>
</div>
```

**Detalhes importantes:**
- O template exibe informações de contato dos criadores do projeto.
- Usa a função `url_for()` para gerar URLs para imagens estáticas.
- Inclui uma descrição do projeto em um campo de texto somente leitura.

#### `app/templates/login/login.html`

Este template exibe o formulário de login.

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Login - Cuidados Dedicados</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css" rel="stylesheet">
</head>
<body>

{% include 'fragments/navbar.html' %}

<section class="d-flex align-items-center justify-content-center vh-100 bg-light">
    <div class="card shadow-lg p-4" style="max-width: 400px; width: 100%;">
        <div class="text-center mb-4">
            <h2 class="text-primary">Bem-vindo de volta!</h2>
            <p class="text-muted">Acesse sua conta para continuar</p>
        </div>

        <form method="post" action="{{ url_for('login.login') }}">
            <div class="mb-3">
                <label for="email" class="form-label">E-mail</label>
                <input type="email" class="form-control" id="email" name="email" placeholder="Digite seu e-mail" required>
            </div>

            <div class="mb-3">
                <label for="senha" class="form-label">Senha</label>
                <input type="password" class="form-control" id="senha" name="senha" placeholder="Digite sua senha" required>
            </div>

            <div class="d-grid mb-3">
                <button type="submit" class="btn btn-primary">Entrar</button>
            </div>

            <div class="text-center">
                <a href="#" class="text-decoration-none text-primary">Esqueceu a senha?</a>
            </div>
        </form>

        <hr>

        <div class="text-center">
            <p class="mb-0">Novo por aqui? <a href="{{ url_for('register.register') }}" class="text-primary text-decoration-none">Crie uma conta</a></p>
        </div>
    </div>
</section>
```

**Detalhes importantes:**
- O template exibe um formulário de login com campos para email e senha.
- O formulário é enviado para a rota `login.login` usando o método POST.
- Inclui um link para recuperação de senha (não implementado) e um link para a página de registro.
- Usa Bootstrap para estilização e layout responsivo.

#### `app/templates/login/register.html`

Este template exibe o formulário de registro com duas opções: para responsáveis e para cuidadores.

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>Cadastro - Cuidados Dedicados</title>
    <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css" rel="stylesheet">
    <style>
        /* Estilos CSS omitidos para brevidade */
    </style>
</head>
<body>

{% include 'fragments/navbar.html' %}

<section class="vh-100 bg-light">
    <div class="container-perspective">
        <div class="card-flip" id="card">
            <!-- Formulário do Responsável -->
            <div class="face front">
                <h2>Cadastro - Responsável</h2>
                <form method="post" action="{{ url_for('register.register_responsible') }}">
                    <input type="text" placeholder="Nome completo" name="name" required />
                    <input type="text" placeholder="CPF" name="cpf" required />
                    <input type="text" placeholder="Telefone" name="phone" required />
                    <input type="email" placeholder="Email" name="email" required />
                    <input type="password" placeholder="Senha" name="password" required />
                    <button type="submit">Cadastrar</button>
                </form>
                <button type="button" class="toggle-btn" onclick="toggleCard()">Sou Cuidador</button>
            </div>

            <!-- Formulário do Cuidador -->
            <div class="face back">
                <h2>Cadastro - Cuidador</h2>
                <form method="post" action="{{ url_for('register.register_caregiver') }}">
                    <input type="text" placeholder="Nome completo" name="name" required />
                    <input type="text" placeholder="CPF" name="cpf" required />
                    <input type="text" placeholder="Telefone" name="phone" required />
                    <input type="email" placeholder="Email" name="email" required />
                    <input type="password" placeholder="Senha" name="password" required />
                    <input type="text" placeholder="Especialidade" name="specialty" required />
                    <input type="text" placeholder="Experiência" name="experience" />
                    <input type="text" placeholder="Formação" name="education" />
                    <input type="text" placeholder="Área de atuação" name="expertiseArea" />
                    <input type="text" placeholder="Habilidades" name="skills" />
                    <button type="submit">Cadastrar</button>
                </form>
                <button type="button" class="toggle-btn" onclick="toggleCard()">Sou Responsável</button>
            </div>
        </div>
    </div>
</section>

<script>
    function toggleCard() {
        const card = document.getElementById('card');
        card.classList.toggle('flip');
    }
    // Código JavaScript omitido para brevidade
</script>
```

**Detalhes importantes:**
- O template usa um efeito de "flip card" para alternar entre os formulários de registro para responsáveis e cuidadores.
- Cada formulário é enviado para uma rota diferente: `register.register_responsible` ou `register.register_caregiver`.
- O formulário de cuidador tem campos adicionais para informações profissionais.
- Usa JavaScript para implementar o efeito de alternância entre os formulários.

### Migrações de Banco de Dados

#### `migrations/versions/3c65ead452be_criação_inicial_das_tabelas.py`

Este arquivo contém a migração inicial que cria as tabelas do banco de dados.

```python
"""Criação inicial das tabelas

Revision ID: 3c65ead452be
Revises: 
Create Date: 2023-05-03 05:33:07.771969

"""
from alembic import op
import sqlalchemy as sa


# identificadores de revisão, usados pelo Alembic
revision = '3c65ead452be'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### comandos gerados automaticamente pelo Alembic - ajuste se necessário! ###
    op.create_table('caregiver',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('cpf', sa.String(length=14), nullable=False),
    sa.Column('phone', sa.String(length=20), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('password', sa.String(length=200), nullable=False),
    sa.Column('specialty', sa.String(length=100), nullable=False),
    sa.Column('experience', sa.Integer(), nullable=False),
    sa.Column('education', sa.String(length=100), nullable=False),
    sa.Column('expertise_area', sa.String(length=100), nullable=False),
    sa.Column('skills', sa.String(length=200), nullable=False),
    sa.Column('rating', sa.Float(), nullable=False),
    sa.Column('address', sa.String(length=200), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('cpf'),
    sa.UniqueConstraint('email')
    )
    # Outras tabelas omitidas para brevidade
    # ### fim dos comandos Alembic ###


def downgrade():
    # ### comandos gerados automaticamente pelo Alembic - ajuste se necessário! ###
    op.drop_table('elderly')
    op.drop_table('contract')
    op.drop_table('responsible')
    op.drop_table('caregiver')
    # ### fim dos comandos Alembic ###
```

**Detalhes importantes:**
- Este arquivo foi gerado pelo Alembic, a ferramenta de migração usada pelo Flask-Migrate.
- Define duas funções: `upgrade()` para aplicar a migração e `downgrade()` para revertê-la.
- A função `upgrade()` cria as tabelas `caregiver`, `responsible`, `contract` e `elderly` com suas colunas e restrições.
- A função `downgrade()` remove as tabelas na ordem inversa para manter a integridade referencial.

#### `migrations/env.py`

Este arquivo configura o ambiente de migração do Alembic.

```python
from __future__ import with_statement

import logging
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from flask import current_app

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
config.set_main_option(
    'sqlalchemy.url',
    str(current_app.extensions['migrate'].db.get_engine().url).replace(
        '%', '%%'))
target_metadata = current_app.extensions['migrate'].db.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    # this callback is used to prevent an auto-migration from being generated
    # when there are no changes to the schema
    # reference: http://alembic.zzzcomputing.com/en/latest/cookbook.html
    def process_revision_directives(context, revision, directives):
        if getattr(config.cmd_opts, 'autogenerate', False):
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []
                logger.info('No changes in schema detected.')

    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            process_revision_directives=process_revision_directives,
            **current_app.extensions['migrate'].configure_args
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

**Detalhes importantes:**
- Este arquivo configura o ambiente para as migrações do Alembic.
- Define duas funções para executar migrações: `run_migrations_offline()` e `run_migrations_online()`.
- A função `run_migrations_online()` inclui um callback `process_revision_directives()` que evita a geração de migrações vazias.
- O arquivo obtém a URL do banco de dados da aplicação Flask atual.

### Arquivos Estáticos

A aplicação usa arquivos estáticos como imagens para exibir fotos de cuidadores e dos criadores do projeto. Esses arquivos estão armazenados no diretório `app/static/images/`.

Para acessar esses arquivos nos templates, a aplicação usa a função `url_for()` do Flask:

```html
<img src="{{ url_for('static', filename='images/breno.jpg') }}" class="rounded-circle mb-2" alt="Breno Siqueira" width="150" height="150">
```

### Configuração e Ambiente

A aplicação usa variáveis de ambiente para configuração, carregadas do arquivo `.env` usando a biblioteca `python-dotenv`. As principais configurações são:

- `SECRET_KEY`: Chave secreta usada para sessões e cookies
- `DATABASE_URL`: URL de conexão com o banco de dados PostgreSQL

Se essas variáveis não estiverem definidas, a aplicação usa valores padrão.

### Autenticação e Gerenciamento de Sessão

Atualmente, a aplicação tem formulários de login e registro, mas a lógica de autenticação não está completamente implementada. O sistema permite o registro de usuários (cuidadores e responsáveis), mas não há verificação de credenciais no login nem gerenciamento de sessão.

Para implementar a autenticação completa, seria necessário:

1. Adicionar hash de senhas antes de armazená-las no banco de dados
2. Verificar credenciais no login
3. Usar Flask-Login ou uma solução similar para gerenciar sessões
4. Adicionar proteção de rotas para usuários autenticados

### Tratamento de Erros

A aplicação tem tratamento básico de erros no serviço `ResponsibleService`, que faz rollback da transação em caso de erro ao salvar um responsável. No entanto, não há tratamento global de erros como páginas personalizadas para erros 404 ou 500.

Para melhorar o tratamento de erros, seria recomendável:

1. Adicionar manipuladores de erro para códigos HTTP comuns
2. Implementar logging de erros
3. Adicionar tratamento de exceções em todas as operações de banco de dados

### Desenvolvimento vs. Produção

A aplicação não tem configurações específicas para ambientes de desenvolvimento e produção. Para uma configuração mais robusta, seria recomendável:

1. Criar classes de configuração para diferentes ambientes
2. Usar variáveis de ambiente para distinguir entre ambientes
3. Configurar logging apropriado para cada ambiente
4. Usar um servidor WSGI como Gunicorn para produção

### Dependências

As dependências do projeto estão listadas no arquivo `requirements.txt`. As principais são:

- **Flask**: Framework web para Python
- **Flask-SQLAlchemy**: Integração do SQLAlchemy com Flask para ORM
- **Flask-Migrate**: Integração do Alembic com Flask para migrações de banco de dados
- **python-dotenv**: Carregamento de variáveis de ambiente de arquivos `.env`
- **psycopg2**: Driver PostgreSQL para Python

### Testes

O projeto tem alguns testes no diretório `test/`, mas não há uma cobertura completa. Para melhorar os testes, seria recomendável:

1. Adicionar testes unitários para todos os modelos e serviços
2. Adicionar testes de integração para as rotas
3. Configurar um ambiente de teste separado
4. Usar fixtures para configurar dados de teste

#### `test/test_caregiver_model.py`

Este arquivo contém testes para o modelo `Caregiver`.

```python
import unittest
import sys
import os

# Adicionar o diretório raiz ao path do Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models.caregiver import Caregiver

class TestCaregiverModel(unittest.TestCase):
    def setUp(self):
        # Configurar o app para testes
        self.app = create_app()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['TESTING'] = True
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        # Limpar após cada teste
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_caregiver(self):
        # Criar um cuidador de teste
        caregiver = Caregiver(
            name="Teste da Silva",
            cpf="123.456.789-00",
            phone="(11) 98765-4321",
            email="teste@example.com",
            password="senha123",
            specialty="Enfermagem",
            experience=5,
            education="Técnico em Enfermagem",
            expertise_area="Idosos",
            skills="Primeiros socorros, Medicação",
            rating=4.5,
            address="Rua Teste, 123"
        )

        # Adicionar ao banco de dados
        db.session.add(caregiver)
        db.session.commit()

        # Recuperar do banco de dados
        saved_caregiver = Caregiver.query.filter_by(email="teste@example.com").first()

        # Verificar se foi salvo corretamente
        self.assertIsNotNone(saved_caregiver)
        self.assertEqual(saved_caregiver.name, "Teste da Silva")
        self.assertEqual(saved_caregiver.cpf, "123.456.789-00")
        self.assertEqual(saved_caregiver.experience, 5)
        self.assertEqual(saved_caregiver.rating, 4.5)

if __name__ == '__main__':
    unittest.main()
```

**Detalhes importantes:**
- O teste configura um ambiente de teste com um banco de dados SQLite em memória.
- Usa os métodos `setUp()` e `tearDown()` para configurar e limpar o ambiente de teste.
- Testa a criação e recuperação de um objeto `Caregiver`.
- Verifica se os atributos do objeto recuperado correspondem aos valores originais.

## Sugestões de Melhorias

1. **Segurança**:
   - Implementar hash de senhas com bcrypt ou similar
   - Adicionar proteção CSRF nos formulários
   - Implementar autenticação completa com Flask-Login

2. **Estrutura**:
   - Organizar as rotas em módulos mais específicos
   - Adicionar uma camada de repositório entre os serviços e o banco de dados
   - Implementar validação de formulários com WTForms

3. **Funcionalidades**:
   - Adicionar perfis de usuário
   - Implementar sistema de avaliação para cuidadores
   - Adicionar funcionalidade de busca e filtros
   - Implementar sistema de mensagens entre responsáveis e cuidadores

4. **Experiência do Usuário**:
   - Melhorar o design responsivo
   - Adicionar feedback visual para ações do usuário
   - Implementar paginação para listas longas

## Conclusão

O ProjectCare é uma aplicação Flask bem estruturada que segue boas práticas de desenvolvimento web. Utiliza uma arquitetura em camadas com modelos, serviços e rotas bem definidos, e aproveita recursos modernos do Flask como blueprints e o padrão de fábrica de aplicação.

A aplicação tem um bom potencial para crescer e se tornar uma plataforma completa para conectar responsáveis por idosos a cuidadores profissionais. Com algumas melhorias de segurança e funcionalidades adicionais, pode se tornar uma solução robusta para esse nicho de mercado.
