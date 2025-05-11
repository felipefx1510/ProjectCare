# app/models/elderly.py
from datetime import date
from app import db


class Elderly(db.Model):
    __tablename__ = "elderly"
    id = db.Column(db.Integer, primary_key=True)
    birthdate = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)

    # Chave estrangeira para o usuário
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # Chave estrangeira para o responsável
    responsible_id = db.Column(db.Integer, db.ForeignKey("responsible.id"), nullable=False)

    # Relações
    user = db.relationship("User", back_populates="elderly")
    responsible = db.relationship("Responsible", back_populates="elderly")

    def __init__(self, user, birthdate, gender, responsible=None):
        self.user = user
        self.birthdate = birthdate
        self.gender = gender
        self.responsible = responsible

    def __repr__(self):
        return f"<Elderly {self.user.name}>"
