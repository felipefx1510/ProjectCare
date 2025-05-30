# app/services/user_service.py
from app import db
from app.models.user import User
from typing import Optional, List
from dataclasses import dataclass


@dataclass
class UserValidationResult:
    """Encapsula resultado de validação de usuário"""
    is_valid: bool
    message: str
    user: Optional[User] = None


class UserService:
    """
    Serviço responsável por operações relacionadas a usuários
    Aplica princípios POO: Encapsulamento, SRP, DRY
    """
    
    @staticmethod
    def save(user: User) -> User:
        """
        Salva um novo usuário no banco de dados
        Valida unicidade do email antes de salvar
        
        Args:
            user: Instância do usuário a ser salva
            
        Returns:
            User: Usuário salvo
            
        Raises:
            ValueError: Se email já existir
        """
        try:
            validation_result = UserService.validate_user_creation(user)
            if not validation_result.is_valid:
                raise ValueError(validation_result.message)
            
            db.session.add(user)
            db.session.commit()
            return user
        except Exception as e:
            db.session.rollback()
            raise
    
    @staticmethod
    def validate_user_creation(user: User) -> UserValidationResult:
        """
        Valida se um usuário pode ser criado
        Centraliza toda lógica de validação
        """
        if UserService.exists_by_email(user.email):
            return UserValidationResult(
                is_valid=False,
                message="Email já existe em nosso sistema."
            )
        
        if UserService.exists_by_cpf(user.cpf):
            return UserValidationResult(
                is_valid=False,
                message="CPF já existe em nosso sistema."
            )
        
        if UserService.exists_by_phone(user.phone):
            return UserValidationResult(
                is_valid=False,
                message="Telefone já existe em nosso sistema."
            )
        
        return UserValidationResult(
            is_valid=True,
            message="Usuário válido para criação"
        )

    @staticmethod
    def get_by_id(user_id: int) -> Optional[User]:
        """
        Busca usuário por ID
        
        Args:
            user_id: ID do usuário
            
        Returns:
            User ou None se não encontrado
        """
        return User.query.get(user_id)

    @staticmethod
    def get_by_email(email: str) -> Optional[User]:
        """
        Busca usuário por email
        
        Args:
            email: Email do usuário
            
        Returns:
            User ou None se não encontrado
        """
        return User.query.filter_by(email=email).first() #first = 1 resultado

    @staticmethod
    def get_by_cpf(cpf: str) -> Optional[User]:
        """
        Busca usuário por CPF
        
        Args:
            cpf: CPF do usuário
            
        Returns:
            User ou None se não encontrado
        """
        return User.query.filter_by(cpf=cpf).first()

    @staticmethod
    def get_by_phone(phone: str) -> Optional[User]:
        """
        Busca usuário por telefone
        
        Args:
            phone: Telefone do usuário
            
        Returns:
            User ou None se não encontrado
        """
        return User.query.filter_by(phone=phone).first()

    @staticmethod
    def get_by_email_or_phone_or_cpf(email: Optional[str] = None, 
                                    phone: Optional[str] = None, 
                                    cpf: Optional[str] = None) -> Optional[User]:
        """
        Busca usuário por email, telefone ou CPF
        Permite busca flexível com múltiplos critérios
        
        Args:
            email: Email para busca (opcional)
            phone: Telefone para busca (opcional)
            cpf: CPF para busca (opcional)
            
        Returns:
            User ou None se não encontrado
        """
        query = User.query
        
        if email:
            query = query.filter_by(email=email)
        if phone:
            query = query.filter_by(phone=phone)
        if cpf:
            query = query.filter_by(cpf=cpf)
        
        return query.first()

    @staticmethod
    def get_all() -> List[User]:
        """
        Busca todos os usuários
        
        Returns:
            Lista de todos os usuários
        """
        return User.query.all()

    @staticmethod
    def delete(user: User) -> None:
        """
        Remove usuário do banco de dados
        
        Args:
            user: Usuário a ser removido
        """
        try:
            db.session.delete(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise

    @staticmethod
    def update(user: User) -> User:
        """
        Atualiza usuário existente no banco de dados
        
        Args:
            user: Usuário com dados atualizados
            
        Returns:
            User: Usuário atualizado
        """
        try:
            db.session.merge(user)
            db.session.commit()
            return user
        except Exception as e:
            db.session.rollback()
            raise

    @staticmethod
    def exists_by_email(email: str) -> bool:
        """
        Verifica se existe usuário com o email informado
        
        Args:
            email: Email a ser verificado
            
        Returns:
            bool: True se existe, False caso contrário
        """
        return User.query.filter_by(email=email).first() is not None

    @staticmethod
    def exists_by_cpf(cpf: str) -> bool:
        """
        Verifica se existe usuário com o CPF informado
        
        Args:
            cpf: CPF a ser verificado
            
        Returns:
            bool: True se existe, False caso contrário
        """
        return User.query.filter_by(cpf=cpf).first() is not None

    @staticmethod
    def exists_by_phone(phone: str) -> bool:
        """
        Verifica se existe usuário com o telefone informado
        
        Args:
            phone: Telefone a ser verificado
            
        Returns:
            bool: True se existe, False caso contrário
        """
        return User.query.filter_by(phone=phone).first() is not None
