from app import db
from app.models.responsible import Responsible

class ResponsibleService:
    def save(self, responsible: Responsible):
        """
        Save a new responsible to the database.
        """
        try:
            db.session.add(responsible)
            db.session.commit()
            return responsible
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao salvar no banco de dados: {e}")
            raise
    
    def get_all_responsibles(self):
        """
        Retrieve all responsibles from the database.
        """
        return Responsible.query.all()
    
    def get_responsible_by_id(self, responsible_id: int):
        """
        Retrieve a responsible by their ID.
        """
        return Responsible.query.get(responsible_id)
    
    def get_responsible_by_email(self, email: str):
        """
        Retrieve a responsible by their email.
        """
        return Responsible.query.filter_by(email=email).first()
