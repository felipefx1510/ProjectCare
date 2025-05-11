# app/services/user_service.py
from app import db
from app.models.user import User

def save(user):
    """
    Save a user to the database.
    """
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
