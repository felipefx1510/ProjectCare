from app import db
from app.models.caregiver import Caregiver

class CaregiverService:
    def save(self, caregiver: Caregiver) -> None:
        """
        Save a new caregiver to the database.
        """
        db.session.add(caregiver)
        db.session.commit()
    
    def get_all_caregivers(self):
        """
        Retrieve all caregivers from the database.
        """
        return Caregiver.query.all()
    
    def get_caregiver_by_id(self, caregiver_id: int):
        """
        Retrieve a caregiver by their ID.
        """
        return Caregiver.query.get(caregiver_id)
    
    def get_caregiver_by_email(self, email: str):
        """
        Recupera um cuidador pelo email do usuário associado.
        """
        from app.models.user import User
        user = User.query.filter_by(email=email).first()
        if user:
            return Caregiver.query.filter_by(user_id=user.id).first()
        return None
