# app/services/user_service.py
from app import db
from app.models.user import User

class UserService:
    def save(self, user: User):
        """
        Save a new user to the database.
        Validates email uniqueness before saving.
        """
        try:
            existing_user = self.get_by_email(user.email)
            if existing_user:
                raise ValueError("Email já existe em nosso sistema.")
            
            db.session.add(user)
            db.session.commit()
            return user
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao salvar usuário no banco de dados: {e}")
            raise

    def get_by_id(self, user_id: int):
        """
        Get a user by ID.
        """
        return User.query.get(user_id)

    def get_by_email(self, email: str):
        """
        Get a user by email.
        """
        return User.query.filter_by(email=email).first()

    def get_by_email_or_phone_or_cpf(self, email=None, phone=None, cpf=None):
        """
        Get a user by email, phone, or CPF.
        """
        query = User.query
        if email:
            query = query.filter_by(email=email)
        if phone:
            query = query.filter_by(phone=phone)
        if cpf:
            query = query.filter_by(cpf=cpf)
        
        return query.first()

    def get_all(self):
        """
        Get all users.
        """
        return User.query.all()

    def delete(self, user: User):
        """
        Delete a user from the database.
        """
        try:
            db.session.delete(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao deletar usuário do banco de dados: {e}")
            raise

    def update(self, user: User):
        """
        Update an existing user in the database.
        """
        try:
            db.session.merge(user)
            db.session.commit()
            return user
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao atualizar usuário no banco de dados: {e}")
            raise

    def exists_by_email(self, email: str):
        """
        Check if a user exists by email.
        """
        return User.query.filter_by(email=email).first() is not None

    def exists_by_cpf(self, cpf: str):
        """
        Check if a user exists by CPF.
        """
        return User.query.filter_by(cpf=cpf).first() is not None

    def exists_by_phone(self, phone: str):
        """
        Check if a user exists by phone.
        """
        return User.query.filter_by(phone=phone).first() is not None
