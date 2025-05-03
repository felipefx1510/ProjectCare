# app_factory.py
from flask import Flask
from config import Config
from db import db
from controllers.category_controller import CategoryController
from controllers.home_controller import HomeController

class AppFactory:
    @staticmethod
    def create_app():
        app = Flask(__name__)
        app.config.from_object(Config)
        db.init_app(app)

        # Registrar rotas
        HomeController.register_routes(app)
        CategoryController.register_routes(app)
        

        return app
