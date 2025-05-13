# app/services/user_service.py
from app import db
from app.models.user import User

def save(user):
    existing_user = get_by_email(user.email)
    if existing_user:
        raise ValueError("Email já existe em nosso sistema.")
    
    db.session.add(user)
    db.session.commit()
    return user

def get_by_id(user_id):
    """
    Get a user by ID.
    """
    return User.query.get(user_id)

def get_by_email(email):
    """
    Get a user by email.
    """
    return User.query.filter_by(email=email).first()

def get_by_email_or_phone_or_cpf(email=None, phone=None, cpf=None):
    """
    Get a user by email, phone, or CPF.
    """
    query = User.query
    if email:
        query = query.filter_by(email=email)
    if phone:
        query = query.filter_by(phone=phone)
    if cpf:
        query = query.filter_by(cpf=cpf)
    
    return query.first()

def get_all():
    """
    Get all users.
    """
    return User.query.all()

def delete(user):
    """
    Delete a user.
    """
    db.session.delete(user)
    db.session.commit()
