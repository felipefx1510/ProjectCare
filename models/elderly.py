from datetime import date
from app import db

class Elderly(db.Model):
    __tablename__ = "elderly"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    
    #foreign key
    responsible_id = db.Column(db.Integer, db.ForeignKey("responsible.id"), nullable=False)
    
    #relations
    responsible = db.relationship("Responsible", back_populates="elderly")
    
    def __init__(self, name, birthdate, gender, address, responsible=None):
        self.name = name
        self.birthdate = birthdate
        self.gender = gender
        self.address = address
        self.responsible = responsible
        
    def __repr__(self):
        return f"<Elderly {self.name}>"