# app/models/elderly.py
from datetime import date
from app import db


class Elderly(db.Model):
    __tablename__ = "elderly"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(20), nullable=True)
    birthdate = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    address_elderly = db.Column(db.String(255), nullable=True)
    city_elderly = db.Column(db.String(100), nullable=True)
    state_elderly = db.Column(db.String(100), nullable=True)
    photo_url = db.Column(db.String(255), nullable=True)
    medical_conditions = db.Column(db.Text, nullable=True)
    allergies = db.Column(db.Text, nullable=True)
    medications_in_use = db.Column(db.Text, nullable=True)
    mobility_level = db.Column(db.String(40), nullable=True)
    specific_care_needs = db.Column(db.Text, nullable=True)
    emergency_contact_name = db.Column(db.String(100), nullable=True)
    emergency_contact_phone = db.Column(db.String(30), nullable=True)
    emergency_contact_relationship = db.Column(db.String(50), nullable=True)
    health_plan_name = db.Column(db.String(100), nullable=True)
    health_plan_number = db.Column(db.String(50), nullable=True)
    additional_notes = db.Column(db.Text, nullable=True)

    # Chave estrangeira para o responsável
    responsible_id = db.Column(db.Integer, db.ForeignKey("responsible.id"), nullable=False)

    # Relações
    responsible = db.relationship("Responsible", back_populates="elderly")

    def __init__(self, name, birthdate, gender, responsible, cpf=None, address_elderly=None, city_elderly=None, state_elderly=None, photo_url=None, medical_conditions=None, allergies=None, medications_in_use=None, mobility_level=None, specific_care_needs=None, emergency_contact_name=None, emergency_contact_phone=None, emergency_contact_relationship=None, health_plan_name=None, health_plan_number=None, additional_notes=None):
        self.name = name
        self.cpf = cpf
        self.birthdate = birthdate
        self.gender = gender
        self.address_elderly = address_elderly
        self.city_elderly = city_elderly
        self.state_elderly = state_elderly
        self.photo_url = photo_url
        self.medical_conditions = medical_conditions
        self.allergies = allergies
        self.medications_in_use = medications_in_use
        self.mobility_level = mobility_level
        self.specific_care_needs = specific_care_needs
        self.emergency_contact_name = emergency_contact_name
        self.emergency_contact_phone = emergency_contact_phone
        self.emergency_contact_relationship = emergency_contact_relationship
        self.health_plan_name = health_plan_name
        self.health_plan_number = health_plan_number
        self.additional_notes = additional_notes
        self.responsible = responsible

    def __repr__(self):
        return f"<Elderly {self.name}>"
