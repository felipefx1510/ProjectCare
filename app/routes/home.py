from flask import Blueprint, render_template, session

home_bp = Blueprint("home", __name__, url_prefix="/")

@home_bp.route("/", methods=["GET"])
def home():
    """
    Home page.
    """
    return render_template("home/home.html")

@home_bp.route("/logout", methods=["GET"])
def logout():
    session.pop('user_id', None)
    return render_template("home/home.html")
