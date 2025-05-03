from flask import Blueprint, render_template, request, redirect, url_for

login_bp = Blueprint("login", __name__, url_prefix="/login")

@login_bp.route("/", methods=["GET", "POST"])
def login():
    """
    Login page.
    """
    if request.method == "POST":
        # Here you would typically check the username and password
        # For now, we'll just redirect to the home page
        return render_template("login/login.html")

@login_bp.route("/", methods=["GET"])
def login_post():
    """
    Login page.
    """
    return render_template("login/login.html")