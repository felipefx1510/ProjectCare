# app/models/user.py
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from datetime import datetime
from app import db

#em qualquer lugar do código que o db.algo existir, o algo é um método do SQLAlchemy com parametros

ph = PasswordHasher(
    time_cost=5,        # Quantidade de iterações (quanto maior, mais seguro, mas mais lento)
    memory_cost=131072,  # Quantidade de memória usada em KiB (128 MiB)
    parallelism=10,      # Número de threads (maior paralelismo = mais rápido)
    hash_len=64,        # Comprimento do hash gerado
    salt_len=16         # Comprimento do salt gerado
)

class User(db.Model):
    __tablename__ = "users"
    __table_args__ = (
        db.CheckConstraint("gender IN ('Masculino', 'Feminino', 'Outro')", name="ck_user_gender"),
    )
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    cep = db.Column(db.String(10), nullable=True)
    address = db.Column(db.String(255), nullable=False)
    number = db.Column(db.String(20), nullable=True)
    neighborhood = db.Column(db.String(100), nullable=True)
    complement = db.Column(db.String(100), nullable=True)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    #timestamp
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # relações
    caregiver = db.relationship("Caregiver", back_populates="user", uselist=False)
    responsible = db.relationship("Responsible", back_populates="user", uselist=False)
    # elderly = db.relationship("Elderly", back_populates="user", uselist=False)  #elderly sem relação

    def __init__(self, name, cpf, gender, birthdate, phone, email, password, cep=None, address=None, number=None, neighborhood=None, complement=None, city=None, state=None):
        self.name = name
        self.cpf = cpf
        self.gender = gender
        self.birthdate = birthdate
        self.phone = phone
        self.email = email
        self.set_password(password)
        self.cep = cep
        self.address = address
        self.number = number
        self.neighborhood = neighborhood
        self.complement = complement
        self.city = city
        self.state = state

    def set_password(self, password):
        """Hash the password and store it."""
        self.password_hash = ph.hash(password)
        
    def check_password(self, password):
        """Verifica a senha fornecida com o hash armazenado."""
        try:
            ph.verify(self.password_hash, password)
            return True
        except VerifyMismatchError:
            return False
    
    def __repr__(self):
        return f"<User {self.name}>"
