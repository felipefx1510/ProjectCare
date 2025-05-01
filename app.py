from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from sqlalchemy import text

app = Flask(__name__)

@app.route("/")
def hello():
    return "Olá mundo!"

if __name__ == "__main__":
    app.run(
        debug=True,
    ) 