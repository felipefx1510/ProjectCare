# app/routes/register.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.user import User
from app.models.caregiver import Caregiver
from app.models.responsible import Responsible
from app.models.elderly import Elderly
from app.services.user_service import UserService
from app.services.caregiver_service import CaregiverService
from app.services.responsible_service import ResponsibleService
from app.services.elderly_service import ElderlyService
from app.services.authentication_service import AuthenticationService
from datetime import datetime
import re

register_bp = Blueprint("register", __name__, url_prefix="/register")


def validar_cpf(cpf):
    """Valida o formato e dígitos verificadores do CPF"""
    cpf = re.sub(r'\D', '', cpf)
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    
    # Validação dos dígitos verificadores
    for i in range(9, 11):
        soma = sum(int(cpf[j]) * ((i + 1) - j) for j in range(i))
        digito = ((soma * 10) % 11) % 10
        if int(cpf[i]) != digito:
            return False
    return True


def validar_email(email):
    """Valida o formato do email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validar_telefone(telefone):
    """Valida o formato do telefone brasileiro"""
    telefone = re.sub(r'\D', '', telefone)
    return len(telefone) in [10, 11]


def validar_campo_obrigatorio(valor, nome_campo):
    """Valida se o campo obrigatório não está vazio"""
    if not valor or not valor.strip():
        raise ValueError(f'O campo {nome_campo} é obrigatório')
    return True


def validar_tamanho_string(valor, nome_campo, min_len, max_len):
    """Valida o tamanho de uma string"""
    if valor and (len(valor.strip()) < min_len or len(valor.strip()) > max_len):
        raise ValueError(f'O campo {nome_campo} deve ter entre {min_len} e {max_len} caracteres')
    return True


def validar_numero_positivo(valor, nome_campo):
    """Valida se o número é positivo"""
    try:
        num = float(valor)
        if num < 0:
            raise ValueError(f'O campo {nome_campo} deve ser um número positivo')
        return True
    except (ValueError, TypeError):
        raise ValueError(f'O campo {nome_campo} deve ser um número válido')


@register_bp.route("/", methods=["GET", "POST"])
def register():
    if 'user_id' in session: #verifica se o usuario já possui uma sessão ativa pelo context processor
        return redirect(url_for('home.home'))

    if request.method == "POST":
        try:
            # Coleta de dados do formulário
            name = request.form.get('name', '').strip()
            cpf = request.form.get('cpf', '').strip()
            phone = request.form.get('phone', '').strip()
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '')
            confirm_password = request.form.get('confirm_password', '')
            # Campos de endereço detalhados
            cep = request.form.get('cep', '').strip()
            address = request.form.get('address', '').strip()
            number = request.form.get('number', '').strip()
            neighborhood = request.form.get('neighborhood', '').strip()
            complement = request.form.get('complement', '').strip()
            city = request.form.get('city', '').strip()
            state = request.form.get('state', '').strip()
            birthdate = request.form.get('birthdate', '').strip()
            gender = request.form.get('gender', '').strip()

            # Validações de campos obrigatórios
            validar_campo_obrigatorio(name, 'Nome')
            validar_campo_obrigatorio(cpf, 'CPF')
            validar_campo_obrigatorio(phone, 'Telefone')
            validar_campo_obrigatorio(email, 'E-mail')
            validar_campo_obrigatorio(password, 'Senha')
            validar_campo_obrigatorio(address, 'Endereço')
            validar_campo_obrigatorio(city, 'Cidade')
            validar_campo_obrigatorio(state, 'Estado')
            validar_campo_obrigatorio(birthdate, 'Data de nascimento')
            validar_campo_obrigatorio(gender, 'Gênero')

            # Validações de formato
            if not validar_cpf(cpf):
                raise ValueError('CPF inválido')
            
            if not validar_email(email):
                raise ValueError('E-mail inválido')
            
            if not validar_telefone(phone):
                raise ValueError('Telefone inválido')

            # Validação de tamanho de campos
            validar_tamanho_string(name, 'Nome', 3, 100)
            validar_tamanho_string(address, 'Endereço', 3, 255)
            validar_tamanho_string(city, 'Cidade', 2, 100)
            validar_tamanho_string(state, 'Estado', 2, 100)

            # Validação de senha
            if len(password) < 8:
                raise ValueError('A senha deve ter pelo menos 8 caracteres')
            
            if password != confirm_password:
                raise ValueError('As senhas não coincidem')

            # Validação de gênero
            if gender not in ['Masculino', 'Feminino', 'Outro']:
                raise ValueError('Gênero inválido')

            # verifica se o usuario  já existe pelos campos que são únicos
            existing_user = UserService.get_by_email_or_phone_or_cpf(email=email, phone=phone, cpf=cpf)
            if existing_user:
                flash('Usuário já cadastrado com este CPF, e-mail ou telefone', 'danger')
                return redirect(url_for('register.register'))

            # Criação e salvamento do usuário
            user = User(
                name=name, cpf=cpf, phone=phone, email=email, password=password,
                cep=cep, address=address, number=number, neighborhood=neighborhood, 
                complement=complement, city=city, state=state, birthdate=birthdate, gender=gender
            )
            UserService.save(user)

            # salvar id
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
    
    user = UserService.get_by_id(user_id)
    if not user:
        flash('Usuário não encontrado', 'danger')
        return redirect(url_for('login.login'))
    
    return render_template("register/select.html", user=user)


@register_bp.route('/caregiver', methods=['GET', 'POST'])
def register_caregiver():
    if request.method == "POST":
        user_id = session.get('user_id')
        if not user_id:
            return redirect(url_for('login.login'))
        
        user = UserService.get_by_id(user_id)
        if not user:
            return redirect(url_for('login.login'))
        
        try:
            specialty = request.form.get('specialty', '').strip()
            experience = request.form.get('experience', '').strip()
            education = request.form.get('education', '').strip()
            expertise_area = request.form.get('expertise', '').strip()
            skills = request.form.get('skills', '').strip()
            dias = request.form.getlist('dias[]')
            periodos = request.form.getlist('periodos[]')
            inicio_imediato = request.form.get('inicio_imediato') == 'sim'
            pretensao = request.form.get('pretensao', '').strip()

            # Validações de campos obrigatórios
            validar_campo_obrigatorio(specialty, 'Especialidade')
            validar_campo_obrigatorio(experience, 'Experiência')
            validar_campo_obrigatorio(education, 'Formação')
            validar_campo_obrigatorio(expertise_area, 'Área de Atuação')
            validar_campo_obrigatorio(skills, 'Habilidades')
            validar_campo_obrigatorio(pretensao, 'Pretensão Salarial')

            # Validações de tamanho
            validar_tamanho_string(specialty, 'Especialidade', 2, 100)
            validar_tamanho_string(education, 'Formação', 2, 100)
            validar_tamanho_string(expertise_area, 'Área de Atuação', 2, 100)
            validar_tamanho_string(skills, 'Habilidades', 2, 500)

            # Validação de experiência (número inteiro positivo)
            try:
                experience_int = int(experience)
                if experience_int < 0:
                    raise ValueError('A experiência não pode ser negativa')
            except ValueError:
                raise ValueError('A experiência deve ser um número válido')

            # Validação de pretensão salarial
            validar_numero_positivo(pretensao, 'Pretensão Salarial')

            # Validação de disponibilidade
            if not dias:
                raise ValueError('Selecione pelo menos um dia disponível')
            if not periodos:
                raise ValueError('Selecione pelo menos um período disponível')
            
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
                experience=experience_int,
                education=education,
                expertise_area=expertise_area,
                skills=skills_full,
                dias_disponiveis=", ".join(dias) if dias else None,
                periodos_disponiveis=", ".join(periodos) if periodos else None,
                inicio_imediato=inicio_imediato,
                pretensao_salarial=float(pretensao) if pretensao else None
            )
            CaregiverService.save(caregiver)
            session['acting_profile'] = 'caregiver'
            flash('Perfil de Cuidador cadastrado e ativado com sucesso!', 'success')
            return redirect(url_for('home.home'))
        except ValueError as e:
            flash(str(e), 'danger')
            return render_template("register/register_caregiver.html")

    return render_template("register/register_caregiver.html")


@register_bp.route('/responsible', methods=['GET', 'POST'])
def register_responsible():
    if request.method == "POST":
        user_id = session.get('user_id')
        if not user_id:
            return redirect(url_for('login.login'))
        
        user = UserService.get_by_id(user_id)
        if not user:
            return redirect(url_for('login.login'))
        
        relationship_with_elderly = request.form.get('relationship_with_elderly')
        primary_need_description = request.form.get('primary_need_description')
        preferred_contact_method = request.form.get('preferred_contact_method')
        
        responsible = Responsible(
            user=user,
            relationship_with_elderly=relationship_with_elderly,
            primary_need_description=primary_need_description,
            preferred_contact_method=preferred_contact_method
        )
        ResponsibleService.save(responsible)
        session['acting_profile'] = 'responsible'
        flash('Perfil de Responsável cadastrado e ativado com sucesso!', 'success')
        return redirect(url_for('home.home'))

    return render_template("register/register_responsible.html")


@register_bp.route('/elderly', methods=['GET', 'POST'])
def register_elderly():
    if request.method == "POST":
        user_id = session.get('user_id')
        if not user_id:
            return redirect(url_for('login.login'))
        
        responsible = ResponsibleService.get_by_user_id(user_id)
        if not responsible:
            flash('Responsável não encontrado.', 'danger')
            return redirect(url_for('login.login'))

        try:
            name = request.form.get('name', '').strip()
            cpf = request.form.get('cpf', '').strip()
            birthdate = request.form.get('birthdate', '').strip()
            gender = request.form.get('gender', '').strip()
            # Campos de endereço detalhados para idoso
            cep_elderly = request.form.get('cep_elderly', '').strip()
            address_elderly = request.form.get('address_elderly', '').strip()
            number_elderly = request.form.get('number_elderly', '').strip()
            neighborhood_elderly = request.form.get('neighborhood_elderly', '').strip()
            complement_elderly = request.form.get('complement_elderly', '').strip()
            city_elderly = request.form.get('city_elderly', '').strip()
            state_elderly = request.form.get('state_elderly', '').strip()
            photo_url = request.form.get('photo_url', '').strip()
            medical_conditions = request.form.get('medical_conditions', '').strip()
            allergies = request.form.get('allergies', '').strip()
            medications_in_use = request.form.get('medications_in_use', '').strip()
            mobility_level = request.form.get('mobility_level', '').strip()
            specific_care_needs = request.form.get('specific_care_needs', '').strip()
            emergency_contact_name = request.form.get('emergency_contact_name', '').strip()
            emergency_contact_phone = request.form.get('emergency_contact_phone', '').strip()
            emergency_contact_relationship = request.form.get('emergency_contact_relationship', '').strip()
            health_plan_name = request.form.get('health_plan_name', '').strip()
            health_plan_number = request.form.get('health_plan_number', '').strip()
            additional_notes = request.form.get('additional_notes', '').strip()

            # Validações de campos obrigatórios
            validar_campo_obrigatorio(name, 'Nome')
            validar_campo_obrigatorio(birthdate, 'Data de nascimento')
            validar_campo_obrigatorio(gender, 'Gênero')

            # Validações de formato
            if cpf and not validar_cpf(cpf):
                raise ValueError('CPF inválido')

            # Validação de gênero
            if gender not in ['Masculino', 'Feminino', 'Outro']:
                raise ValueError('Gênero inválido')

            # Validações de tamanho
            validar_tamanho_string(name, 'Nome', 2, 100)

            # Validação de telefone de emergência
            if emergency_contact_phone and not validar_telefone(emergency_contact_phone):
                raise ValueError('Telefone de emergência inválido')

            elderly = Elderly(
                name=name,
                cpf=cpf if cpf else None,
                birthdate=birthdate,
                gender=gender,
                cep_elderly=cep_elderly if cep_elderly else None,
                address_elderly=address_elderly if address_elderly else None,
                number_elderly=number_elderly if number_elderly else None,
                neighborhood_elderly=neighborhood_elderly if neighborhood_elderly else None,
                complement_elderly=complement_elderly if complement_elderly else None,
                city_elderly=city_elderly if city_elderly else None,
                state_elderly=state_elderly if state_elderly else None,
                photo_url=photo_url if photo_url else None,
                medical_conditions=medical_conditions if medical_conditions else None,
                allergies=allergies if allergies else None,
                medications_in_use=medications_in_use if medications_in_use else None,
                mobility_level=mobility_level if mobility_level else None,
                specific_care_needs=specific_care_needs if specific_care_needs else None,
                emergency_contact_name=emergency_contact_name if emergency_contact_name else None,
                emergency_contact_phone=emergency_contact_phone if emergency_contact_phone else None,
                emergency_contact_relationship=emergency_contact_relationship if emergency_contact_relationship else None,
                health_plan_name=health_plan_name if health_plan_name else None,
                health_plan_number=health_plan_number if health_plan_number else None,
                additional_notes=additional_notes if additional_notes else None,
                responsible=responsible
            )
            ElderlyService.save(elderly)
            flash('Idoso cadastrado com sucesso!', 'success')
            return redirect(url_for('register.register_elderly'))
        except ValueError as e:
            flash(str(e), 'danger')
            return render_template("register/register_elderly.html")

    return render_template("register/register_elderly.html")
