# This file makes the services directory a Python package
from app.services.caregiver_service import CaregiverService
from app.services.elderly_service import ElderlyService
from app.services.responsible_service import ResponsibleService
from app.services.user_service import UserService
from app.services.authentication_service import AuthenticationService
from app.services.viacep_service import ViaCepService

# Instâncias de compatibilidade para código legado
# DEPRECATED: Use as classes estáticas diretamente
class LegacyCaregiverService:
    def get_caregiver_by_id(self, caregiver_id: int):
        return CaregiverService.get_by_id(caregiver_id)
    
    def get_caregiver_by_email(self, email: str):
        return CaregiverService.get_by_email(email)
    
    def get_all_caregivers(self):
        return CaregiverService.get_all()
    
    def save(self, caregiver):
        return CaregiverService.save(caregiver)

class LegacyResponsibleService:
    def get_responsible_by_id(self, responsible_id: int):
        return ResponsibleService.get_by_id(responsible_id)
    
    def get_responsible_by_email(self, email: str):
        return ResponsibleService.get_by_email(email)
    
    def get_responsible_by_user_id(self, user_id: int):
        return ResponsibleService.get_by_user_id(user_id)
    
    def save(self, responsible):
        return ResponsibleService.save(responsible)

class LegacyUserService:
    def get_by_id(self, user_id: int):
        return UserService.get_by_id(user_id)
    
    def get_by_email(self, email: str):
        return UserService.get_by_email(email)
    
    def get_by_email_or_phone_or_cpf(self, email=None, phone=None, cpf=None):
        return UserService.get_by_email_or_phone_or_cpf(email, phone, cpf)
    
    def save(self, user):
        return UserService.save(user)

class LegacyElderlyService:
    def get_all(self):
        return ElderlyService.get_all()
    
    def get_by_responsible_id(self, responsible_id: int):
        return ElderlyService.get_by_responsible_id(responsible_id)
    
    def save(self, elderly):
        return ElderlyService.save(elderly)

# Instâncias de compatibilidade
caregiver_service = LegacyCaregiverService()
responsible_service = LegacyResponsibleService()
elderly_service = LegacyElderlyService()
user_service = LegacyUserService()
