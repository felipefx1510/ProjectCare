# app/models/contract.py
from datetime import datetime
from app import db


class Contract(db.Model):
    __tablename__ = "contract"
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)

    # Chaves estrangeiras
    responsible_id = db.Column(db.Integer, db.ForeignKey("responsible.id"), nullable=False)
    caregiver_id = db.Column(db.Integer, db.ForeignKey("caregiver.id"), nullable=False)

    # Relações
    responsible = db.relationship("Responsible", back_populates="contracts")
    caregiver = db.relationship("Caregiver", back_populates="contracts")

    def __init__(self, responsible, caregiver, start_date=None, end_date=None):
        self.responsible = responsible
        self.caregiver = caregiver
        self.start_date = start_date or datetime.utcnow()
        self.end_date = end_date

    def __repr__(self):
        return f"<Contract {self.id}: {self.caregiver.user.name} - {self.responsible.user.name}>"
