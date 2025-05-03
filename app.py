from flask import Flask, render_template, request, redirect, url_for
from config import Config
from db import db  # Importa o db do novo módulo
from repositories.category_repository import CategoryRepository

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)  # Inicializa o banco de dados com o app

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/categories")
def categories():
    categories = CategoryRepository.get_all()
    return render_template("categories/categories.html", categories=categories)

@app.route("/categories/register", methods=["GET", "POST"])
def register_category():
    if request.method == "POST":
        name = request.form.get("name")
        CategoryRepository.create(name)
        return redirect(url_for("categories"))
    return render_template("categories/register.html")


if __name__ == "__main__":
    app.run(debug=True)