from app import db

class Responsible(db.Model):
    __tablename__ = "responsible"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    # relations
    elderly = db.relationship("Elderly", back_populates="responsible", cascade="all, delete-orphan")
    contracts = db.relationship("Contract", back_populates="responsible", cascade="all, delete-orphan")

    def __init__(self, name, cpf, phone, email, password):
        self.name = name
        self.cpf = cpf
        self.phone = phone
        self.email = email
        self.password = password


    def __repr__(self):
        return f"<Responsible {self.name}>"