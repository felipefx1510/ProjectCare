# app/routes/login.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.services.user_service import UserService
from app.services.authentication_service import AuthenticationService

login_bp = Blueprint("login", __name__, url_prefix="/login")


@login_bp.route("/", methods=["GET", "POST"])
def login():
    # Verifica se usuário já está logado
    if 'user_id' in session:
        return redirect(url_for('home.home'))
    
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Validação básica de entrada
        if not email or not password:
            flash('Email e senha são obrigatórios', 'warning')
            return redirect(url_for('login.login'))
          # Processar login usando o serviço de autenticação
        success, redirect_url, message = AuthenticationService.process_login(email, password)
        
        if not success:
            flash(message, 'danger')
            return redirect(redirect_url)
        
        # Login bem-sucedido
        flash(message, 'success')
        return redirect(redirect_url)
    
    return render_template("login/login.html")


@login_bp.route("/select-acting-profile", methods=["GET", "POST"])
def select_acting_profile():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login.login'))
        
    user = UserService.get_by_id(user_id)
    if not user:
        return redirect(url_for('login.login'))
    
    # Usa o serviço de autenticação para buscar perfis (elimina duplicação)
    user_profile = AuthenticationService.get_user_profiles(user)
    
    if request.method == "POST":
        profile = request.form.get('acting_profile')
        if profile == 'caregiver':
            if user_profile.has_caregiver:
                session['acting_profile'] = 'caregiver'
                flash('Você está atuando como Cuidador.', 'success')
                return redirect(url_for('home.home'))
            else:
                return redirect(url_for('register.register_caregiver'))
        elif profile == 'responsible':
            if user_profile.has_responsible:
                session['acting_profile'] = 'responsible'
                flash('Você está atuando como Responsável.', 'success')
                return redirect(url_for('home.home'))
            else:
                return redirect(url_for('register.register_responsible'))
        else:
            flash('Selecione um perfil válido.', 'warning')
    
    return render_template(
        "login/select_acting_profile.html",
        has_caregiver=user_profile.has_caregiver,
        has_responsible=user_profile.has_responsible
    )


@login_bp.route("/logout")
def logout():
    # Usa o serviço de autenticação para limpeza da sessão
    AuthenticationService.clear_session()
    flash('Você saiu da sua conta com sucesso.', 'info')
    return redirect(url_for('home.home'))
