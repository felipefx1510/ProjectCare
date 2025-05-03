from flask import Blueprint, render_template, request, redirect, url_for
from app.models.caregiver import Caregiver
from app.models.responsible import Responsible
from app.services import caregiver_service, responsible_service

#bp
register_bp = Blueprint("register", __name__, url_prefix="/register")

@register_bp.route("/", methods=["GET", "POST"])
def register():
   if request.method == "POST":
       pass
    return render_template("register/register.html")
@register_bp.route('/responsible', methods=['POST'])
def register_responsible():
    """
    Register a new responsible.
    """
    name = request.form.get('name')
    cpf = request.form.get('cpf')
    phone = request.form.get('phone')
    email = request.form.get('email')
    password = request.form.get('password')
    
    responsible = Responsible(name=name, cpf=cpf, phone=phone, email=email, password=password)
    responsible_service.save(responsible)
    
    return redirect(url_for('login.login'))

@register_bp.route('/caregiver', methods=['POST'])
def register_caregiver():
    """
    Register a new caregiver.
    """
    name = request.form.get('name')
    cpf = request.form.get('cpf')
    phone = request.form.get('phone')
    email = request.form.get('email')
    password = request.form.get('password')
    specialty = request.form.get('specialty')
    experience = request.form.get('experience')
    education = request.form.get('education')
    expertise_area = request.form.get('expertise')
    skills = request.form.get('skills')
    
    caregiver = Caregiver(
        name=name,
        cpf=cpf,
        phone=phone,
        email=email,
        password=password,
        specialty=specialty,
        experience=experience,
        education=education,
        expertise_area=expertise_area,
        skills=skills,
        rating=0.0
    )
    
    caregiver_service.save(caregiver)
    # Redirect to the login page after successful registration
    return redirect(url_for('login.login'))