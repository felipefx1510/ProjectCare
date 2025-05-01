from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from sqlalchemy import text

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

@app.route("/")
def hello():
    return "Olá mundo!"

@app.route("/test-db")
def test():
    try:
        db.session.execute(text("SELECT 1"))
        return "Banco de dados conectado!"
    except Exception as e:
        return f"Erro ao conectar ao banco de dados: {e}"       

if __name__ == "__main__":
    app.run() 