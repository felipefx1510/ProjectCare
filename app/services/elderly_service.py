# app/services/elderly_service.py
from app import db
from app.models.elderly import Elderly


class ElderlyService:
    def save(self, elderly: Elderly):
        """
        Save a new elderly to the database.
        """
        try:
            db.session.add(elderly)
            db.session.commit()
            return elderly
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao salvar no banco de dados: {e}")
            raise

    def get_all(self):
        """
        Retrieve all elderly from the database.
        """
        return Elderly.query.all()

    def get_by_id(self, elderly_id: int):
        """
        Retrieve an elderly by their ID.
        """
        return Elderly.query.get(elderly_id)

    def get_by_user_id(self, user_id: int):
        """
        Retrieve an elderly by their user ID.
        """
        return Elderly.query.filter_by(user_id=user_id).first()

    def get_by_responsible_id(self, responsible_id: int):
        """
        Retrieve all elderly associated with a specific responsible ID.
        """
        return Elderly.query.filter_by(responsible_id=responsible_id).all()
