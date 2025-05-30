# from flask import Blueprint, render_template, request, redirect, url_for, session, flash
# from app.services.user_service import UserService
# from app.services.caregiver_service import CaregiverService
# from app.services.responsible_service import ResponsibleService
# from app.services.authentication_service import AuthenticationService

# user_bp = Blueprint("user", __name__, url_prefix="/user")

# @user_bp.route("/profiles", methods=["GET", "POST"])
# def manage_profiles():
#     user_id = session.get('user_id')
#     if not user_id:
#         return redirect(url_for('login.login'))
    
#     user = UserService.get_by_id(user_id)
#     if not user:
#         return redirect(url_for('login.login'))
    
#     # Usar o método do authentication_service para buscar perfis
#     user_profile = AuthenticationService.get_user_profiles(user)
    
#     has_caregiver = user_profile.has_caregiver
#     has_responsible = user_profile.has_responsible
#     acting_profile = session.get('acting_profile')

#     if request.method == "POST":
#         selected_profile = request.form.get('selected_profile')
#         if selected_profile in ['caregiver', 'responsible']:
#             if (selected_profile == 'caregiver' and has_caregiver) or (selected_profile == 'responsible' and has_responsible):
#                 session['acting_profile'] = selected_profile
#                 flash(f'Agora você está atuando como {"Cuidador" if selected_profile=="caregiver" else "Responsável"}.', 'success')
#                 return redirect(url_for('home.home'))
#             else:
#                 flash('Perfil selecionado não disponível para sua conta.', 'danger')
#         else:
#             flash('Selecione um perfil válido.', 'warning')

#     return render_template(
#         "user/manage_profiles.html",
#         has_caregiver=has_caregiver,
#         has_responsible=has_responsible,
#         acting_profile=acting_profile
#     )
