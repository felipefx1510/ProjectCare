# app/services/elderly_service.py
from app import db
from app.models.elderly import Elderly
from typing import Optional, List
from dataclasses import dataclass


@dataclass
class ElderlySearchResult:
    """Encapsula resultado de busca de idoso"""
    found: bool
    elderly: Optional[Elderly] = None
    elderly_list: Optional[List[Elderly]] = None
    message: str = ""


class ElderlyService:
    """
    Serviço responsável por operações relacionadas a idosos
    Aplica princípios POO: Encapsulamento, SRP, DRY
    """
    
    @staticmethod
    def save(elderly: Elderly) -> Elderly:
        """
        Salva um novo idoso no banco de dados
        
        Args:
            elderly: Instância do idoso a ser salva
            
        Returns:
            Elderly: Idoso salvo
        """
        try:
            db.session.add(elderly)
            db.session.commit()
            return elderly
        except Exception as e:
            db.session.rollback()
            raise

    @staticmethod
    def get_all() -> List[Elderly]:
        """
        Busca todos os idosos do banco de dados
        
        Returns:
            Lista de todos os idosos
        """
        return Elderly.query.all()

    # @staticmethod
    # def get_by_id(elderly_id: int) -> Optional[Elderly]:
    #     """
    #     Busca idoso por ID
        
    #     Args:
    #         elderly_id: ID do idoso
            
    #     Returns:
    #         Elderly ou None se não encontrado
    #     """
    #     return Elderly.query.get(elderly_id)

    @staticmethod
    def get_by_user_id(user_id: int) -> Optional[Elderly]:
        """
        Busca idoso pelo user_id (FK para users.id)
        
        Args:
            user_id: ID do usuário associado
            
        Returns:
            Elderly ou None se não encontrado
        """
        return Elderly.query.filter_by(user_id=user_id).first()

    @staticmethod
    def get_by_responsible_id(responsible_id: int) -> List[Elderly]:
        """
        Busca todos os idosos associados a um responsável específico
        
        Args:
            responsible_id: ID do responsável
            
        Returns:
            Lista de idosos associados ao responsável
        """
        return Elderly.query.filter_by(responsible_id=responsible_id).all()
    
    @staticmethod
    def find_elderly_by_responsible(responsible_id: int) -> ElderlySearchResult:
        """
        Busca idosos por responsável com resultado encapsulado
        Centraliza lógica de busca e validação
        
        Args:
            responsible_id: ID do responsável
            
        Returns:
            ElderlySearchResult com o resultado da busca
        """
        elderly_list = ElderlyService.get_by_responsible_id(responsible_id)
        
        if elderly_list:
            return ElderlySearchResult(
                found=True,
                elderly_list=elderly_list,
                message=f"Encontrados {len(elderly_list)} idoso(s) para o responsável"
            )
        
        return ElderlySearchResult(
            found=False,
            message="Nenhum idoso encontrado para este responsável"
        )
    
    @staticmethod
    def exists_by_user_id(user_id: int) -> bool:
        """
        Verifica se existe idoso para o user_id informado
        
        Args:
            user_id: ID do usuário
            
        Returns:
            bool: True se existe, False caso contrário
        """
        return Elderly.query.filter_by(user_id=user_id).first() is not None
    
    @staticmethod
    def exists_by_responsible_id(responsible_id: int) -> bool:
        """
        Verifica se existem idosos para o responsible_id informado
        
        Args:
            responsible_id: ID do responsável
            
        Returns:
            bool: True se existem, False caso contrário
        """
        return len(Elderly.query.filter_by(responsible_id=responsible_id).all()) > 0
    
    @staticmethod
    def count_by_responsible_id(responsible_id: int) -> int:
        """
        Conta quantos idosos estão associados a um responsável
        
        Args:
            responsible_id: ID do responsável
            
        Returns:
            int: Número de idosos associados
        """
        return Elderly.query.filter_by(responsible_id=responsible_id).count()
    
    @staticmethod
    def update(elderly: Elderly) -> Elderly:
        """
        Atualiza idoso existente no banco de dados
        
        Args:
            elderly: Idoso com dados atualizados
            
        Returns:
            Elderly: Idoso atualizado
        """
        try:
            db.session.merge(elderly)
            db.session.commit()
            return elderly
        except Exception as e:
            db.session.rollback()
            raise
    
    @staticmethod
    def delete(elderly: Elderly) -> None:
        """
        Remove idoso do banco de dados
        
        Args:
            elderly: Idoso a ser removido
        """
        try:
            db.session.delete(elderly)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise
