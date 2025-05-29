from flask import Blueprint, render_template

contact_bp = Blueprint("contact", __name__, url_prefix="/contact")

@contact_bp.route("/", methods=["GET"])
def contact():
    """
    Contact page.
    """
    return render_template("contact/contact.html")

#se eu quiser aceitar as solicitações de contato por exemplo, é só iniciar
#uma nova rota aqui
#@contact_bp.route("/submit", methods=["POST"])
# def submit_contact():
# logica
# return render_template("contact/contact.html", message="Contact submitted successfully.")