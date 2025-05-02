from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/categories")
def categories():
    from entities.category import Category
    categories = Category.query.all()
    return render_template("categories.html", categories=categories)

if __name__ == "__main__":
    app.run(debug=True)