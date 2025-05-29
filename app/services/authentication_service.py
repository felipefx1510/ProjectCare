# app/services/authentication_service.py
from flask import session, url_for
from app.services import caregiver_service, responsible_service, user_service
from dataclasses import dataclass
from typing import Optional, Tuple, Any


@dataclass
class UserProfile:
    """Encapsula informações de perfil do usuário"""
    caregiver: Optional[Any] = None
    responsible: Optional[Any] = None
    
    @property
    def has_caregiver(self) -> bool:
        return self.caregiver is not None
    
    @property
    def has_responsible(self) -> bool:
        return self.responsible is not None
    
    @property
    def has_both_profiles(self) -> bool:
        return self.has_caregiver and self.has_responsible
    
    @property
    def has_no_profiles(self) -> bool:
        return not self.has_caregiver and not self.has_responsible
    
    @property
    def single_profile_type(self) -> Optional[str]:
        """Retorna o tipo do perfil único, se houver apenas um"""
        if self.has_caregiver and not self.has_responsible:
            return 'caregiver'
        elif self.has_responsible and not self.has_caregiver:
            return 'responsible'
        return None


class AuthenticationService:
    """
    Serviço responsável por toda lógica de autenticação
    Aplica princípios POO: Encapsulamento, SRP, DRY
    """
    
    @staticmethod
    def validate_credentials(email: str, password: str) -> Tuple[bool, Optional[Any]]:
        """
        Valida credenciais do usuário
        Returns: (is_valid, user_object)
        """
        if not email or not password:
            return False, None
            
        user = user_service.get_by_email(email)
        if not user or not user.check_password(password):
            return False, None
            
        return True, user
    
    @staticmethod
    def get_user_profiles(user: Any) -> UserProfile:
        """
        Busca todos os perfis de um usuário
        Encapsula a lógica de busca dupla (por ID e email)
        """
        # Busca perfil de cuidador
        caregiver = caregiver_service.get_caregiver_by_id(user.id)
        if not caregiver:
            caregiver = caregiver_service.get_caregiver_by_email(user.email)
        
        # Busca perfil de responsável
        responsible = responsible_service.get_responsible_by_id(user.id)
        if not responsible:
            responsible = responsible_service.get_responsible_by_email(user.email)
        
        return UserProfile(caregiver=caregiver, responsible=responsible)
    
    @staticmethod
    def setup_session(user_id: int, profile_type: Optional[str] = None):
        """
        Configura a sessão do usuário
        Encapsula toda lógica de gerenciamento de sessão
        """
        session['user_id'] = user_id
        session['acting_profile'] = profile_type
    
    @staticmethod
    def determine_login_redirect(user_profile: UserProfile, user_id: int) -> str:
        """
        Determina para onde redirecionar após autenticação
        Centraliza toda lógica de redirecionamento
        """
        if user_profile.has_no_profiles:
            return url_for('register.select_profile')
        elif user_profile.has_both_profiles:
            return url_for('login.select_acting_profile')
        else:            # Usuário tem apenas um perfil
            profile_type = user_profile.single_profile_type
            AuthenticationService.setup_session(user_id, profile_type)
            return url_for('home.home')
    
    @staticmethod
    def process_login(email: str, password: str) -> Tuple[bool, str, str]:
        """
        Processa todo o fluxo de login
        Returns: (success, redirect_url, message)
        """
        # 1. Validar credenciais
        is_valid, user = AuthenticationService.validate_credentials(email, password)
        if not is_valid or user is None:
            return False, url_for('login.login'), 'Email ou senha inválidos'
        
        # 2. Configurar sessão básica
        AuthenticationService.setup_session(user.id)
        
        # 3. Buscar perfis
        user_profile = AuthenticationService.get_user_profiles(user)
        
        # 4. Determinar redirecionamento
        redirect_url = AuthenticationService.determine_login_redirect(user_profile, user.id)
        
        return True, redirect_url, 'Login realizado com sucesso'
    
    @staticmethod
    def clear_session():
        """
        Limpa completamente a sessão do usuário
        Encapsula lógica de logout
        """
        session.pop('user_id', None)
        session.pop('acting_profile', None)
