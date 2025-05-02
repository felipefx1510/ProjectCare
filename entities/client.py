from app import db

class Client(db.Model):
    __tablename__ = 'client'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)

    reservations = db.relationship(
        'Reservation',
        backref='client',
        cascade='all, delete-orphan',
        lazy=True
    )

    def __init__(self, name, email, reservations=None):
        self.name = name
        self.email = email
        self.reservations = reservations or []
