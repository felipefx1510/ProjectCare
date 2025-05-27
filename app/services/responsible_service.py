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
        Retrieve a responsible by their email (busca pelo user.email).
        """
        from app.models.user import User
        user = User.query.filter_by(email=email).first()
        if not user:
            return None
        return Responsible.query.filter_by(user_id=user.id).first()
    
    def get_responsible_by_user_id(self, user_id: int):
        """
        Retrieve a responsible by their user_id (FK para users.id).
        """
        return Responsible.query.filter_by(user_id=user_id).first()
