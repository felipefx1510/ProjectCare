from flask import Blueprint, render_template, session

home_bp = Blueprint("home", __name__, url_prefix="/")

@home_bp.route("/", methods=["GET"])
def home():
    """Retorna a página inicial do sistema.
    Esta rota é acessível sem autenticação e serve como ponto de entrada para o usuário.
    """
    return render_template("home/home.html")

