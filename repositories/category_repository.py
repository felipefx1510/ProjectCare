from entities.category import Category
from db import db

class CategoryRepository:
    @staticmethod
    def get_all():
        """Retorna todas as categorias."""
        return Category.query.all()

    @staticmethod
    def get_by_id(category_id):
        """Retorna uma categoria pelo ID."""
        return Category.query.get(category_id)

    @staticmethod
    def create(name):
        """Cria uma nova categoria."""
        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
        return category

    @staticmethod
    def delete(category_id):
        """Exclui uma categoria pelo ID."""
        category = Category.query.get(category_id)
        if category:
            db.session.delete(category)
            db.session.commit()
            return True
        return False