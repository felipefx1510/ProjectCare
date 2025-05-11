import unittest
import sys
import os

# Adicionar o diretório raiz ao path do Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models.caregiver import Caregiver

class TestCaregiverModel(unittest.TestCase):
    def setUp(self):
        # Configurar o app para testes
        self.app = create_app()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['TESTING'] = True
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        # Limpar após cada teste
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_caregiver(self):
        # Criar um cuidador de teste
        caregiver = Caregiver(
            name="Teste da Silva",
            cpf="123.456.789-00",
            phone="(11) 98765-4321",
            email="teste@example.com",
            password="senha123",
            specialty="Enfermagem",
            experience=5,
            education="Técnico em Enfermagem",
            expertise_area="Idosos",
            skills="Primeiros socorros, Medicação",
            rating=4.5,
            address="Rua Teste, 123"
        )

        # Adicionar ao banco de dados
        db.session.add(caregiver)
        db.session.commit()

        # Recuperar do banco de dados
        saved_caregiver = Caregiver.query.filter_by(email="teste@example.com").first()

        # Verificar se foi salvo corretamente
        self.assertIsNotNone(saved_caregiver)
        self.assertEqual(saved_caregiver.name, "Teste da Silva")
        self.assertEqual(saved_caregiver.cpf, "123.456.789-00")
        self.assertEqual(saved_caregiver.experience, 5)
        self.assertEqual(saved_caregiver.rating, 4.5)

if __name__ == '__main__':
    unittest.main()
