# app/services/caregiver_service.py
from app import db
from app.models.caregiver import Caregiver
from app.models.user import User
from typing import Optional, List
from dataclasses import dataclass


@dataclass
class CaregiverSearchResult:
    """Encapsula resultado de busca de cuidador"""
    found: bool
    caregiver: Optional[Caregiver] = None
    message: str = ""


class CaregiverService:
    """
    Serviço responsável por operações relacionadas a cuidadores
    Aplica princípios POO: Encapsulamento, SRP, DRY
    """
    
    @staticmethod
    def save(caregiver: Caregiver) -> Caregiver:
        """
        Salva um novo cuidador no banco de dados
        
        Args:
            caregiver: Instância do cuidador a ser salva
            
        Returns:
            Caregiver: Cuidador salvo
        """
        try:
            db.session.add(caregiver)
            db.session.commit()
            return caregiver
        except Exception as e:
            db.session.rollback()
            raise
    
    @staticmethod
    def get_all() -> List[Caregiver]:
        """
        Busca todos os cuidadores do banco de dados
        
        Returns:
            Lista de todos os cuidadores
        """
        return Caregiver.query.all()
    
    @staticmethod
    def get_by_id(caregiver_id: int) -> Optional[Caregiver]:
        """
        Busca cuidador por ID
        
        Args:
            caregiver_id: ID do cuidador
            
        Returns:
            Caregiver ou None se não encontrado
        """
        return Caregiver.query.get(caregiver_id)
    
    @staticmethod
    def get_by_email(email: str) -> Optional[Caregiver]:
        """
        Busca cuidador pelo email do usuário associado
        Encapsula lógica de busca através da relação User
        
        Args:
            email: Email do usuário
            
        Returns:
            Caregiver ou None se não encontrado
        """
        user = User.query.filter_by(email=email).first()
        if not user:
            return None
        return Caregiver.query.filter_by(user_id=user.id).first()
    
    @staticmethod
    def get_by_user_id(user_id: int) -> Optional[Caregiver]:
        """
        Busca cuidador pelo user_id (FK para users.id)
        
        Args:
            user_id: ID do usuário associado
            
        Returns:
            Caregiver ou None se não encontrado
        """
        return Caregiver.query.filter_by(user_id=user_id).first()
    
    
    # @staticmethod
    # def find_caregiver_by_user(user_id: int, email: str) -> CaregiverSearchResult:
    #     """
    #     Busca cuidador por ID de usuário ou email
    #     Centraliza lógica de busca dupla usada no authentication_service
        
    #     Args:
    #         user_id: ID do usuário
    #         email: Email do usuário
            
    #     Returns:
    #         CaregiverSearchResult com o resultado da busca
    #     """
    #     # Primeira tentativa: busca por ID
    #     caregiver = CaregiverService.get_by_user_id(user_id)
    #     if caregiver:
    #         return CaregiverSearchResult(
    #             found=True,
    #             caregiver=caregiver,
    #             message="Cuidador encontrado por ID de usuário"
    #         )
        
    #     # Segunda tentativa: busca por email
    #     caregiver = CaregiverService.get_by_email(email)
    #     if caregiver:
    #         return CaregiverSearchResult(
    #             found=True,
    #             caregiver=caregiver,
    #             message="Cuidador encontrado por email"
    #         )
        
    #     return CaregiverSearchResult(
    #         found=False,
    #         message="Cuidador não encontrado"
    #     )
    
    # @staticmethod
    # def exists_by_user_id(user_id: int) -> bool:
    #     """
    #     Verifica se existe cuidador para o user_id informado
        
    #     Args:
    #         user_id: ID do usuário
            
    #     Returns:
    #         bool: True se existe, False caso contrário
    #     """
    #     return Caregiver.query.filter_by(user_id=user_id).first() is not None
    
    # @staticmethod
    # def update(caregiver: Caregiver) -> Caregiver:
    #     """
    #     Atualiza cuidador existente no banco de dados
        
    #     Args:
    #         caregiver: Cuidador com dados atualizados
            
    #     Returns:
    #         Caregiver: Cuidador atualizado
    #     """
    #     try:
    #         db.session.merge(caregiver)
    #         db.session.commit()
    #         return caregiver
    #     except Exception as e:
    #         db.session.rollback()
    #         raise
    
    # @staticmethod
    # def delete(caregiver: Caregiver) -> None:
    #     """
    #     Remove cuidador do banco de dados
        
    #     Args:
    #         caregiver: Cuidador a ser removido
    #     """
    #     try:
    #         db.session.delete(caregiver)
    #         db.session.commit()
    #     except Exception as e:
    #         db.session.rollback()
    #         raise


# # Mantém compatibilidade com código existente que usa métodos de instância
# def get_caregiver_by_id(caregiver_id: int) -> Optional[Caregiver]:
#     """Função de compatibilidade para código legado"""
#     return CaregiverService.get_by_id(caregiver_id)


def get_caregiver_by_email(email: str) -> Optional[Caregiver]:
    """Função de compatibilidade para código legado"""
    return CaregiverService.get_by_email(email)
