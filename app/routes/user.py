from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.services import caregiver_service, responsible_service, user_service

user_bp = Blueprint("user", __name__, url_prefix="/user")

@user_bp.route("/profiles", methods=["GET", "POST"])
def manage_profiles():
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
    has_caregiver = bool(caregiver)
    has_responsible = bool(responsible)
    acting_profile = session.get('acting_profile')

    if request.method == "POST":
        selected_profile = request.form.get('selected_profile')
        if selected_profile in ['caregiver', 'responsible']:
            if (selected_profile == 'caregiver' and has_caregiver) or (selected_profile == 'responsible' and has_responsible):
                session['acting_profile'] = selected_profile
                flash(f'Agora você está atuando como {"Cuidador" if selected_profile=="caregiver" else "Responsável"}.', 'success')
                return redirect(url_for('home.home'))
            else:
                flash('Perfil selecionado não disponível para sua conta.', 'danger')
        else:
            flash('Selecione um perfil válido.', 'warning')

    return render_template(
        "user/manage_profiles.html",
        has_caregiver=has_caregiver,
        has_responsible=has_responsible,
        acting_profile=acting_profile
    )
