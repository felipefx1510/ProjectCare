from app import db

# Tabela associativa room_category
room_category = db.Table(
    'room_category',
    db.Column('room_id', db.Integer, db.ForeignKey('room.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True)
)

class Room(db.Model):
    __tablename__ = 'room'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(50), nullable=False)

    categories = db.relationship(
        'Category',
        secondary=room_category,
        lazy='subquery',
        backref=db.backref('rooms', lazy=True)
    )

    def __init__(self, number, categories=None):
        self.number = number
        self.categories = categories or []
