# app/routes/login.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.services import user_service, caregiver_service, responsible_service

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
            # Verifica perfis
            caregiver = caregiver_service.get_caregiver_by_id(user.id) if user else None
            if not caregiver and user:
                caregiver = caregiver_service.get_caregiver_by_email(user.email)
            responsible = responsible_service.get_responsible_by_id(user.id) if user else None
            if not responsible and user:
                responsible = responsible_service.get_responsible_by_email(user.email)
            if caregiver and responsible:
                # Usuário tem ambos os perfis, redireciona para escolha
                return redirect(url_for('login.select_acting_profile'))
            elif caregiver:
                session['acting_profile'] = 'caregiver'
            elif responsible:
                session['acting_profile'] = 'responsible'
            else:
                session['acting_profile'] = None
            flash('Login realizado com sucesso', 'success')
            return redirect(url_for('home.home'))
        else:
            flash('Email ou senha inválidos', 'danger')
        
    return render_template("login/login.html")


@login_bp.route("/select-acting-profile", methods=["GET", "POST"])
def select_acting_profile():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login.login'))
    user = user_service.get_by_id(user_id)
    caregiver = caregiver_service.get_caregiver_by_id(user_id) if user else None
    if not caregiver and user:
        caregiver = caregiver_service.get_caregiver_by_email(user.email)
    responsible = responsible_service.get_responsible_by_id(user_id) if user else None
    if not responsible and user:
        responsible = responsible_service.get_responsible_by_email(user.email)
    if request.method == "POST":
        profile = request.form.get('acting_profile')
        if profile in ['caregiver', 'responsible']:
            session['acting_profile'] = profile
            return redirect(url_for('home.home'))
        flash('Selecione um perfil válido.', 'warning')
    return render_template(
        "profile/select_acting_profile.html",
        has_caregiver=bool(caregiver),
        has_responsible=bool(responsible)
    )


@login_bp.route("/logout")
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home.home'))
