from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

load_dotenv(override=True) #override para sobescrever as variaveis

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    # Verifica se as variáveis obrigatórias estão definidas
    required_env_vars = ['SECRET_KEY', 'DATABASE_URL']
    for var in required_env_vars:
        if not os.getenv(var):
            raise RuntimeError(f"A variável de ambiente '{var}' não está definida. Verifique o arquivo .env.")    # Configuração do app
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Configurações de conexão para PostgreSQL/Neon
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,  # Verifica conexões antes de usar
        'pool_recycle': 300,    # Recicla conexões a cada 5 minutos
        'pool_timeout': 20,     # Timeout para obter conexão do pool
        'max_overflow': 0,      # Não permite conexões extras além do pool
        'pool_size': 5,         # Tamanho do pool de conexões
        'connect_args': {
            'connect_timeout': 10,  # Timeout para conectar
            'options': '-c timezone=America/Sao_Paulo'
        }
    }

    # Extensões
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        db.create_all()  # Cria as tabelas no banco de dados se não existirem

    
    @app.context_processor
    def inject_user():
        """
        Injeta o usuário na sessão para acesso em templates.
        """
        if 'user_id' in session:
            return {'navbar_template': 'fragments/navbar_login.html'}
        return {'navbar_template': 'fragments/navbar.html'}    # Registro de blueprints
    from app.routes.home import home_bp
    from app.routes.caregivers import caregivers_bp
    from app.routes.contact import contact_bp
    from app.routes.login import login_bp
    from app.routes.register import register_bp
    from app.routes.responsible_dashboard import responsible_dashboard_bp
    from app.routes.api import api_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(caregivers_bp)
    app.register_blueprint(contact_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(register_bp)
    app.register_blueprint(responsible_dashboard_bp)
    app.register_blueprint(api_bp)

    return app

