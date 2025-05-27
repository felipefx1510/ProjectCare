from flask import Blueprint, render_template
from app.services import caregiver_service, elderly_service

caregivers_bp = Blueprint("caregivers", __name__, url_prefix="/caregivers")

@caregivers_bp.route("/", methods=["GET"])
def list_caregivers():
    """
    List all caregivers.
    """
    caregivers = caregiver_service.get_all_caregivers()
    return render_template("list/caregiver_list.html", caregivers=caregivers)

@caregivers_bp.route("/elderly", methods=["GET"])
def list_elderly():
    """
    Lista todos os idosos disponíveis para cuidadores.
    """
    elderly_list = elderly_service.get_all()
    return render_template("list/elderly_list.html", elderly_list=elderly_list)
