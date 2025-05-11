from flask import Blueprint, render_template

contact_bp = Blueprint("contact", __name__, url_prefix="/contact")

@contact_bp.route("/", methods=["GET"])
def contact():
    """
    Contact page.
    """
    return render_template("contact/contact.html")
