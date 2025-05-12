# app/routes/login.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.services import user_service

login_bp = Blueprint("login", __name__, url_prefix="/login")


@login_bp.route("/", methods=["GET", "POST"])
def login():
    if 'user_id' in session:
        return redirect(url_for('home.home'))
    
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('Email e senha são obrigatórios', 'warning')
            return redirect(url_for('login.login'))

        user = user_service.get_by_email(email)
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            flash('Login realizado com sucesso', 'success')
            return redirect(url_for('home.home'))
        else:
            flash('Email ou senha inválidos', 'danger')
        
    return render_template("login/login.html")


@login_bp.route("/logout")
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home.home'))
