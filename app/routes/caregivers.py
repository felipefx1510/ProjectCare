from flask import Blueprint, render_template
from app.services.caregiver_service import CaregiverService
from app.services.elderly_service import ElderlyService

caregivers_bp = Blueprint("caregivers", __name__, url_prefix="/caregivers")

@caregivers_bp.route("/", methods=["GET"])
def list_caregivers():
    """
    Retorna a pagina de listagem de cuidadores
    """
    caregivers = CaregiverService.get_all()
    return render_template("list/caregiver_list.html", caregivers=caregivers)

@caregivers_bp.route("/elderly", methods=["GET"])
def list_elderly():
    """
    Retorna a pagina de listagem de idosos disponíveis para cuidadores.
    """
    elderly_list = ElderlyService.get_all()
    return render_template("list/elderly_list.html", elderly_list=elderly_list)
