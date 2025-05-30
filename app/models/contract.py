# app/models/contract.py
from datetime import datetime
from app import db


class Contract(db.Model):
    __tablename__ = "contract"
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
      # Informações financeiras
    hourly_rate = db.Column(db.Numeric(10, 2), nullable=True)  # Valor por hora
    monthly_salary = db.Column(db.Numeric(10, 2), nullable=True)  # Salário mensal
    payment_frequency = db.Column(db.String(20), nullable=True)  # semanal, quinzenal, mensal
    
    # Status e controle
    status = db.Column(db.String(20), default='active', nullable=False)  # active, completed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Informações adicionais
    work_schedule = db.Column(db.Text, nullable=True)  # Horários de trabalho detalhados
    special_conditions = db.Column(db.Text, nullable=True)  # Condições especiais do contrato
    notes = db.Column(db.Text, nullable=True)  

    # Observações gerais
    # Chaves estrangeiras
    responsible_id = db.Column(db.Integer, db.ForeignKey("responsible.id"), nullable=False)
    caregiver_id = db.Column(db.Integer, db.ForeignKey("caregiver.id"), nullable=False)

    # Relações
    responsible = db.relationship("Responsible", back_populates="contracts")
    caregiver = db.relationship("Caregiver", back_populates="contracts")

    def __init__(self, responsible, caregiver, start_date=None, end_date=None, 
                 hourly_rate=None, monthly_salary=None, payment_frequency=None,
                 work_schedule=None, special_conditions=None, notes=None):
        self.responsible = responsible
        self.caregiver = caregiver
        self.start_date = start_date or datetime.utcnow()
        self.end_date = end_date
        self.hourly_rate = hourly_rate
        self.monthly_salary = monthly_salary
        self.payment_frequency = payment_frequency
        self.work_schedule = work_schedule
        self.special_conditions = special_conditions
        self.notes = notes
        self.status = 'active'  # Status padrão

    def __repr__(self):
        return f"<Contract {self.id}: {self.caregiver.user.name} - {self.responsible.user.name}>"
