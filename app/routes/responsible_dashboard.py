# app/routes/responsible_dashboard.py
from flask import Blueprint, render_template, session, redirect, url_for, flash
from app.services import elderly_service, responsible_service

responsible_dashboard_bp = Blueprint("responsible_dashboard", __name__, url_prefix="/responsible")

@responsible_dashboard_bp.route("/my-elderly")
def my_elderly():
    if 'user_id' not in session or session.get('acting_profile') != 'responsible':
        flash('Acesso não autorizado.', 'danger')
        return redirect(url_for('login.login'))

    user_id = session['user_id']
    # Buscar o Responsible pelo user_id
    responsible = responsible_service.get_responsible_by_user_id(user_id)
    if not responsible:
        flash('Responsável não encontrado.', 'danger')
        return redirect(url_for('home.home'))

    elderly_list = elderly_service.get_by_responsible_id(responsible.id)
    return render_template("responsible/my_elderly_list.html", elderly_list=elderly_list)
