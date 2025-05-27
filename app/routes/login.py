# app/routes/login.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.services import caregiver_service, responsible_service, user_service

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
        if not user:
            flash('Email ou senha inválidos', 'danger')
            return redirect(url_for('login.login'))
        caregiver = caregiver_service.get_caregiver_by_id(user.id)
        if not caregiver:
            caregiver = caregiver_service.get_caregiver_by_email(user.email)
        responsible = responsible_service.get_responsible_by_id(user.id)
        if not responsible:
            responsible = responsible_service.get_responsible_by_email(user.email)
        session['user_id'] = user.id
        if not caregiver and not responsible:
            # Redireciona para seleção de perfil se não tiver nenhum perfil
            session['acting_profile'] = None
            return redirect(url_for('register.select_profile'))
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
        if profile == 'caregiver':
            if caregiver:
                session['acting_profile'] = 'caregiver'
                flash('Você está atuando como Cuidador.', 'success')
                return redirect(url_for('home.home'))
            else:
                return redirect(url_for('register.register_caregiver'))
        elif profile == 'responsible':
            if responsible:
                session['acting_profile'] = 'responsible'
                flash('Você está atuando como Responsável.', 'success')
                return redirect(url_for('home.home'))
            else:
                return redirect(url_for('register.register_responsible'))
        else:
            flash('Selecione um perfil válido.', 'warning')
    return render_template(
        "login/select_acting_profile.html",
        has_caregiver=bool(caregiver),
        has_responsible=bool(responsible)
    )


@login_bp.route("/logout")
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home.home'))
