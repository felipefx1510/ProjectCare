from flask import Blueprint, render_template, session

home_bp = Blueprint("home", __name__, url_prefix="/")

@home_bp.route("/", methods=["GET"])
def home():
    return render_template("home/home.html")

