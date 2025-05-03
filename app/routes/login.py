from flask import Blueprint, render_template, request, redirect, url_for

login_bp = Blueprint("login", __name__, url_prefix="/login")

@login_bp.route("/", methods=["GET", "POST"])
def login():
    """
    Login page.
    """
    if request.method == "POST":
        # Aqui você pode adicionar a lógica de autenticação
        # Por enquanto, redireciona para a página inicial após o login
        return redirect(url_for('home.home'))
    
    # Retorna o template de login para o método GET
    return render_template("login/login.html")