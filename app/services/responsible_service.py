# app/services/responsible_service.py
from app import db
from app.models.responsible import Responsible
from app.models.user import User
from typing import Optional, List
from dataclasses import dataclass


@dataclass
class ResponsibleSearchResult:
    """Encapsula resultado de busca de responsável"""
    found: bool
    responsible: Optional[Responsible] = None
    message: str = ""


class ResponsibleService:
    """
    Serviço responsável por operações relacionadas a responsáveis
    Aplica princípios POO: Encapsulamento, SRP, DRY
    """
    
    @staticmethod
    def save(responsible: Responsible) -> Responsible:
        """
        Salva um novo responsável no banco de dados
        
        Args:
            responsible: Instância do responsável a ser salva
            
        Returns:
            Responsible: Responsável salvo
        """
        try:
            db.session.add(responsible)
            db.session.commit()
            return responsible
        except Exception as e:
            db.session.rollback()
            raise
    
    @staticmethod
    def get_all() -> List[Responsible]:
        """
        Busca todos os responsáveis do banco de dados
        
        Returns:
            Lista de todos os responsáveis
        """
        return Responsible.query.all()
    
    @staticmethod
    def get_by_id(responsible_id: int) -> Optional[Responsible]:
        """
        Busca responsável por ID
        
        Args:
            responsible_id: ID do responsável
            
        Returns:
            Responsible ou None se não encontrado
        """
        return Responsible.query.get(responsible_id)
    
    @staticmethod
    def get_by_email(email: str) -> Optional[Responsible]:
        """
        Busca responsável pelo email do usuário associado
        Encapsula lógica de busca através da relação User
        
        Args:
            email: Email do usuário
            
        Returns:
            Responsible ou None se não encontrado
        """
        user = User.query.filter_by(email=email).first()
        if not user:
            return None
        return Responsible.query.filter_by(user_id=user.id).first()
    
    @staticmethod
    def get_by_user_id(user_id: int) -> Optional[Responsible]:
        """
        Busca responsável pelo user_id (FK para users.id)
        
        Args:
            user_id: ID do usuário associado
            
        Returns:
            Responsible ou None se não encontrado
        """
        return Responsible.query.filter_by(user_id=user_id).first()
    
    @staticmethod
    def find_responsible_by_user(user_id: int, email: str) -> ResponsibleSearchResult:
        """
        Busca responsável por ID de usuário ou email
        Centraliza lógica de busca dupla usada no authentication_service
        
        Args:
            user_id: ID do usuário
            email: Email do usuário
            
        Returns:
            ResponsibleSearchResult com o resultado da busca
        """
        # Primeira tentativa: busca por ID
        responsible = ResponsibleService.get_by_user_id(user_id)
        if responsible:
            return ResponsibleSearchResult(
                found=True,
                responsible=responsible,
                message="Responsável encontrado por ID de usuário"
            )
        
        # Segunda tentativa: busca por email
        responsible = ResponsibleService.get_by_email(email)
        if responsible:
            return ResponsibleSearchResult(
                found=True,
                responsible=responsible,
                message="Responsável encontrado por email"
            )
        
        return ResponsibleSearchResult(
            found=False,
            message="Responsável não encontrado"
        )
    
    @staticmethod
    def exists_by_user_id(user_id: int) -> bool:
        """
        Verifica se existe responsável para o user_id informado
        
        Args:
            user_id: ID do usuário
            
        Returns:
            bool: True se existe, False caso contrário
        """
        return Responsible.query.filter_by(user_id=user_id).first() is not None
    
    @staticmethod
    def update(responsible: Responsible) -> Responsible:
        """
        Atualiza responsável existente no banco de dados
        
        Args:
            responsible: Responsável com dados atualizados
            
        Returns:
            Responsible: Responsável atualizado
        """
        try:
            db.session.merge(responsible)
            db.session.commit()
            return responsible
        except Exception as e:
            db.session.rollback()
            raise
    
    @staticmethod
    def delete(responsible: Responsible) -> None:
        """
        Remove responsável do banco de dados
        
        Args:
            responsible: Responsável a ser removido
        """
        try:
            db.session.delete(responsible)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise


# Mantém compatibilidade com código existente que usa métodos de instância
def get_responsible_by_id(responsible_id: int) -> Optional[Responsible]:
    """Função de compatibilidade para código legado"""
    return ResponsibleService.get_by_id(responsible_id)


def get_responsible_by_email(email: str) -> Optional[Responsible]:
    """Função de compatibilidade para código legado"""
    return ResponsibleService.get_by_email(email)
