from flask import Blueprint, render_template
from app.services import caregiver_service

caregivers_bp = Blueprint("caregivers", __name__, url_prefix="/caregivers")

@caregivers_bp.route("/", methods=["GET"])
def list_caregivers():
    """
    List all caregivers.
    """
    caregivers = caregiver_service.get_all_caregivers()
    return render_template("caregivers/list.html", caregivers=caregivers)
