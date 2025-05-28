# This file makes the services directory a Python package
from app.services.caregiver_service import CaregiverService
from app.services.elderly_service import ElderlyService
from app.services.responsible_service import ResponsibleService
from app.services.user_service import UserService

# Create service instances
caregiver_service = CaregiverService()
responsible_service = ResponsibleService()
elderly_service = ElderlyService()
user_service = UserService()
