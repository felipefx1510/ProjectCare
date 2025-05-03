from db import db
from .room import room_category  # Importa a tabela associativa já criada

class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    # Relacionamento Many-to-Many com Room
    rooms = db.relationship(
        'Room',
        secondary=room_category,
        lazy='subquery',
        backref=db.backref('categories', lazy=True)
    )

    def __init__(self, name, rooms=None):
        self.name = name
        self.rooms = rooms or []