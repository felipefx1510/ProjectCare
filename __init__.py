from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    #config app
    if config_class:
        app.config.from_object(config_class)
    else:
        app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev_key)'
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:Soldier2003!@localhost:5432/ProjectCare')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
    #extensions
    db.init_app(app)
    migrate.init_app(app, db)

    #reg blueprints
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
    
    return app