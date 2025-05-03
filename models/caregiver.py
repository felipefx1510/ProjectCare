from datetime import datetime
from app import db

class Caregiver(db.Model):
    __tablename__ = "caregiver"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    specialty = db.Column(db.String(100), nullable=False)
    experience = db.Column(db.Integer, nullable=False)  # in years
    education = db.Column(db.String(100), nullable=False)
    expertise_area = db.Column(db.String(100), nullable=False)
    skills = db.Column(db.String(200), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

   #relation
   contracts = db.relationship("Contract", back_populates="caregiver", cascade="all, delete-orphan")
   
   def __init__(self, name, cpf, phone, email, password, specialty, experience, education, expertise_area, skills, rating, address):
    self.name = name
    self.cpf = cpf
    self.phone = phone
    self.email = email
    self.password = password
    self.specialty = specialty
    self.experience = experience
    self.education = education
    self.expertise_area = expertise_area
    self.skills = skills
    self.rating = rating
    self.address = address
    
    def __repr__(self):
        return f"<Caregiver {self.name}>"