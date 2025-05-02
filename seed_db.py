from app import app, db
from entities.room import Room
from entities.client import Client
from entities.category import Category

with app.app_context():
    # Adiciona categorias
    category1 = Category(name="Deluxe")
    category2 = Category(name="Standard")

    # Adiciona quartos
    room1 = Room(number="101", categories=[category1])
    room2 = Room(number="102", categories=[category2])

    # Adiciona clientes
    client1 = Client(name="John Doe", email="john@example.com")

    # Salva no banco
    db.session.add_all([category1, category2, room1, room2, client1])
    db.session.commit()
    print("✅ Dados iniciais adicionados com sucesso!")
