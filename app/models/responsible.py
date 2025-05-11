# app/models/responsible.py
from app import db

class Responsible(db.Model):
    __tablename__ = "responsible"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates="responsible")

    elderly = db.relationship("Elderly", back_populates="responsible", cascade="all, delete-orphan")
    contracts = db.relationship("Contract", back_populates="responsible", cascade="all, delete-orphan")

    def __init__(self, user):
        self.user = user

    def __repr__(self):
        return f"<Responsible {self.user.name}>"
