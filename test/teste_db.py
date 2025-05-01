from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

# Carrega variáveis do .env
load_dotenv()

# Pega a URL do banco
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("❌ Variável DATABASE_URL não definida no .env")
    exit(1)

# Cria engine SQLAlchemy
engine = create_engine(DATABASE_URL)

# Testa a conexão
try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("✅ Conexão com o banco de dados bem-sucedida!")
except Exception as e:
    print(f"❌ Erro ao conectar: {e}")
