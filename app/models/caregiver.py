# app/models/caregiver.py
from app import db

#em qualquer lugar do código que o db.algo existir, o algo é um método do SQLAlchemy com parametros

class Caregiver(db.Model):
    __tablename__ = "caregiver"
    id = db.Column(db.Integer, primary_key=True)
    specialty = db.Column(db.String(100), nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    education = db.Column(db.String(100), nullable=False)
    expertise_area = db.Column(db.String(100), nullable=False)
    skills = db.Column(db.String(200), nullable=False)
    rating = db.Column(db.Float, nullable=False, default=0.0)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates="caregiver")

    contracts = db.relationship("Contract", back_populates="caregiver", cascade="all, delete-orphan")

    def __init__(self, user, specialty, experience, education, expertise_area, skills, rating=0.0):
        self.user = user
        self.specialty = specialty
        self.experience = experience
        self.education = education
        self.expertise_area = expertise_area
        self.skills = skills
        self.rating = rating

    def __repr__(self):
        return f"<Caregiver {self.user.name}>"
