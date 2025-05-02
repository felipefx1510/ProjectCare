# filepath: p:\Python\Reservation\ProjectCare\init_db.py
from app import app, db
from entities.room import Room
from entities.client import Client
from entities.category import Category
from entities.reservation import Reservation

# Cria todas as tabelas dentro do contexto da aplicação
with app.app_context():
    db.create_all()
    print("✅ Banco de dados e tabelas criados com sucesso!")