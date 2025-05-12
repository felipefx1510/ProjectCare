# app/routes/register.py
from flask import Blueprint, render_template, request, redirect, url_for, session
from app.models.user import User
from app.models.caregiver import Caregiver
from app.models.responsible import Responsible
from app.models.elderly import Elderly
from app.services import user_service, caregiver_service, responsible_service, elderly_service
from datetime import datetime

register_bp = Blueprint("register", __name__, url_prefix="/register")


@register_bp.route("/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get('name')
        cpf = request.form.get('cpf')
        phone = request.form.get('phone')
        email = request.form.get('email')
        password = request.form.get('password')
        address = request.form.get('address')
        city = request.form.get('city')
        state = request.form.get('state')
        birthdate = request.form.get('birthdate')
        gender = request.form.get('gender')

        user = User(name=name, cpf=cpf, phone=phone, email=email, password=password,
                    address=address, city=city, state=state, birthdate=birthdate, gender=gender)
        user_service.save(user)

        # Armazenar o ID do usuário na sessão para uso posterior
        session['user_id'] = user.id

        # Redirecionar para a página de seleção de perfil
        return redirect(url_for('register.select_profile'))

    return render_template("register/register.html")


@register_bp.route("/select-profile", methods=["GET"])
def select_profile():
    return render_template("login/select_profile.html")


@register_bp.route('/caregiver', methods=['GET', 'POST'])
def register_caregiver():
    if request.method == "POST":
        user_id = session.get('user_id')
        if not user_id:
            return redirect(url_for('login.login'))

        user = user_service.get_by_id(user_id)

        specialty = request.form.get('specialty')
        experience = request.form.get('experience')
        education = request.form.get('education')
        expertise_area = request.form.get('expertise')
        skills = request.form.get('skills')

        caregiver = Caregiver(
            user=user,
            specialty=specialty,
            experience=experience,
            education=education,
            expertise_area=expertise_area,
            skills=skills
        )

        caregiver_service.save(caregiver)
        return redirect(url_for('login.login'))

    return render_template("login/register_caregiver.html")


@register_bp.route('/responsible', methods=['GET', 'POST'])
def register_responsible():
    if request.method == "POST":
        user_id = session.get('user_id')
        if not user_id:
            return redirect(url_for('login.login'))

        user = user_service.get_by_id(user_id)

        responsible = Responsible(user=user)
        responsible_service.save(responsible)

        return redirect(url_for('login.login'))

    return render_template("login/register_responsible.html")


@register_bp.route('/elderly', methods=['GET', 'POST'])
def register_elderly():
    if request.method == "POST":
        user_id = session.get('user_id')
        if not user_id:
            return redirect(url_for('login.login'))

        user = user_service.get_by_id(user_id)

        birthdate = datetime.strptime(request.form.get('birthdate'), '%Y-%m-%d').date()
        gender = request.form.get('gender')
        responsible_id = request.form.get('responsible_id')

        responsible = responsible_service.get_by_id(responsible_id)

        elderly = Elderly(
            user=user,
            birthdate=birthdate,
            gender=gender,
            responsible=responsible
        )

        elderly_service.save(elderly)
        return redirect(url_for('login.login'))

    # Buscar todos os responsáveis para o formulário
    responsibles = responsible_service.get_all()
    return render_template("login/register_elderly.html", responsibles=responsibles)
