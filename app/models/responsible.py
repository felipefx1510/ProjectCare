# app/models/responsible.py
from app import db

class Responsible(db.Model):
    __tablename__ = "responsible"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates="responsible")

    elderly = db.relationship("Elderly", back_populates="responsible", cascade="all, delete-orphan")
    contracts = db.relationship("Contract", back_populates="responsible", cascade="all, delete-orphan")

    relationship_with_elderly = db.Column(db.String(50), nullable=True)
    primary_need_description = db.Column(db.String(255), nullable=True)
    preferred_contact_method = db.Column(db.String(30), nullable=True)

    def __init__(self, user, relationship_with_elderly=None, primary_need_description=None, preferred_contact_method=None):
        self.user = user
        self.relationship_with_elderly = relationship_with_elderly
        self.primary_need_description = primary_need_description
        self.preferred_contact_method = preferred_contact_method

    def __repr__(self):
        return f"<Responsible {self.user.name}>"
