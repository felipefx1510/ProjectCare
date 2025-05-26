# app/routes/register.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.user import User
from app.models.caregiver import Caregiver
from app.models.responsible import Responsible
from app.models.elderly import Elderly
from app.services import user_service, caregiver_service, responsible_service, elderly_service
from datetime import datetime

register_bp = Blueprint("register", __name__, url_prefix="/register")


@register_bp.route("/", methods=["GET", "POST"])
def register():
    if 'user_id' in session:
        return redirect(url_for('home.home'))

    if request.method == "POST":
        try:
            # Coleta de dados do formulário
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

            # Verifica se o usuário já existe
            existing_user = user_service.get_by_email_or_phone_or_cpf(email=email, phone=phone, cpf=cpf)
            if existing_user:
                flash('Usuário já cadastrado', 'danger')
                return redirect(url_for('register.register'))

            # Criação e salvamento do usuário
            user = User(
                name=name, cpf=cpf, phone=phone, email=email, password=password,
                address=address, city=city, state=state, birthdate=birthdate, gender=gender
            )
            user_service.save(user)

            # Armazenar o ID do usuário na sessão
            session['user_id'] = user.id

            flash('Usuário cadastrado com sucesso', 'success')
            return redirect(url_for('register.select_profile'))
        except ValueError as e:
            flash(str(e), 'danger')
        except Exception as e:
            flash('Ocorreu um erro ao cadastrar o usuário. Tente novamente.', 'danger')
            return redirect(url_for('register.register'))

    return render_template("register/register.html")


@register_bp.route("/select-profile", methods=["GET"])
def select_profile():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login.login'))
    user = user_service.get_by_id(user_id)
    if not user:
        flash('Usuário não encontrado', 'danger')
        return redirect(url_for('login.login'))
    return render_template("profile/select.html", user=user)


@register_bp.route("/add-profile", methods=["GET", "POST"])
def add_profile():
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
        if not caregiver and request.form.get('add_caregiver'):
            return redirect(url_for('register.register_caregiver'))
        if not responsible and request.form.get('add_responsible'):
            return redirect(url_for('register.register_responsible'))
        flash('Selecione um perfil para adicionar.', 'warning')
    return render_template(
        "profile/select.html",
        user=user,
        show_add_profile=True,
        has_caregiver=bool(caregiver),
        has_responsible=bool(responsible)
    )


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

        # Novos campos do formulário
        dias = request.form.getlist('dias[]')
        periodos = request.form.getlist('periodos[]')
        inicio_imediato = request.form.get('inicio_imediato') == 'sim'
        pretensao = request.form.get('pretensao')

        # Serializa as informações extras para o campo skills
        info_extra = []
        if dias:
            info_extra.append(f"Dias: {', '.join(dias)}")
        if periodos:
            info_extra.append(f"Períodos: {', '.join(periodos)}")
        info_extra.append(f"Início imediato: {'Sim' if inicio_imediato else 'Não'}")
        info_extra.append(f"Pretensão: R$ {pretensao}")
        skills_full = skills + " | " + " | ".join(info_extra)

        caregiver = Caregiver(
            user=user,
            specialty=specialty,
            experience=experience,
            education=education,
            expertise_area=expertise_area,
            skills=skills,
            dias_disponiveis=", ".join(dias) if dias else None,
            periodos_disponiveis=", ".join(periodos) if periodos else None,
            inicio_imediato=inicio_imediato,
            pretensao_salarial=float(pretensao) if pretensao else None
        )

        caregiver_service.save(caregiver)
        return redirect(url_for('login.login'))

    return render_template("register/register_caregiver.html")


@register_bp.route('/responsible', methods=['GET', 'POST'])
def register_responsible():
    if request.method == "POST":
        user_id = session.get('user_id')
        if not user_id:
            return redirect(url_for('login.login'))

        user = user_service.get_by_id(user_id)
        relationship_with_elderly = request.form.get('relationship_with_elderly')
        primary_need_description = request.form.get('primary_need_description')
        preferred_contact_method = request.form.get('preferred_contact_method')

        responsible = Responsible(
            user=user,
            relationship_with_elderly=relationship_with_elderly,
            primary_need_description=primary_need_description,
            preferred_contact_method=preferred_contact_method
        )
        responsible_service.save(responsible)
        return redirect(url_for('login.login'))

    return render_template("register/register_responsible.html")


@register_bp.route('/elderly', methods=['GET', 'POST'])
def register_elderly():
    if request.method == "POST":
        responsible_id = session.get('user_id')
        if not responsible_id:
            return redirect(url_for('login.login'))
        responsible = responsible_service.get_responsible_by_id(responsible_id)
        if not responsible:
            flash('Responsável não encontrado.', 'danger')
            return redirect(url_for('login.login'))

        name = request.form.get('name')
        cpf = request.form.get('cpf')
        birthdate = request.form.get('birthdate')
        gender = request.form.get('gender')
        address_elderly = request.form.get('address_elderly')
        city_elderly = request.form.get('city_elderly')
        state_elderly = request.form.get('state_elderly')
        photo_url = request.form.get('photo_url')
        medical_conditions = request.form.get('medical_conditions')
        allergies = request.form.get('allergies')
        medications_in_use = request.form.get('medications_in_use')
        mobility_level = request.form.get('mobility_level')
        specific_care_needs = request.form.get('specific_care_needs')
        emergency_contact_name = request.form.get('emergency_contact_name')
        emergency_contact_phone = request.form.get('emergency_contact_phone')
        emergency_contact_relationship = request.form.get('emergency_contact_relationship')
        health_plan_name = request.form.get('health_plan_name')
        health_plan_number = request.form.get('health_plan_number')
        additional_notes = request.form.get('additional_notes')

        elderly = Elderly(
            name=name,
            cpf=cpf,
            birthdate=birthdate,
            gender=gender,
            address_elderly=address_elderly,
            city_elderly=city_elderly,
            state_elderly=state_elderly,
            photo_url=photo_url,
            medical_conditions=medical_conditions,
            allergies=allergies,
            medications_in_use=medications_in_use,
            mobility_level=mobility_level,
            specific_care_needs=specific_care_needs,
            emergency_contact_name=emergency_contact_name,
            emergency_contact_phone=emergency_contact_phone,
            emergency_contact_relationship=emergency_contact_relationship,
            health_plan_name=health_plan_name,
            health_plan_number=health_plan_number,
            additional_notes=additional_notes,
            responsible=responsible
        )
        elderly_service.save(elderly)
        flash('Idoso cadastrado com sucesso!', 'success')
        return redirect(url_for('register.register_elderly'))

    return render_template("register/register_elderly.html")
