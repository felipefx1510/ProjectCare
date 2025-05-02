from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/categories")
def categories():
    return render_template("categories/categories.html")

@app.route("/categories/register")
def register_categorie():
    return render_template("categories/register.html")

@app.route("/categories/register/save", methods=["POST"])
def save_categorie():
    # Aqui você pode adicionar a lógica para salvar a categoria no banco de dados
    return render_template("categories/categories.html")


if __name__ == "__main__":
    app.run(debug=True)