from flask import Blueprint, render_template
from app.services import caregiver_service, elderly_service

caregivers_bp = Blueprint("caregivers", __name__, url_prefix="/caregivers")

@caregivers_bp.route("/", methods=["GET"])
def list_caregivers():
    """
    Retorna a pagina de listagem de cuidadores
    """
    caregivers = caregiver_service.get_all_caregivers()
    return render_template("list/caregiver_list.html", caregivers=caregivers)

@caregivers_bp.route("/elderly", methods=["GET"])
def list_elderly():
    """
    Retorna a pagina de listagem de idosos disponíveis para cuidadores.
    """
    elderly_list = elderly_service.get_all()
    return render_template("list/elderly_list.html", elderly_list=elderly_list)
