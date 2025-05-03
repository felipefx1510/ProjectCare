# controllers/category_controller.py
from flask import render_template, request, redirect, url_for
from repositories.category_repository import CategoryRepository

class CategoryController:
    @staticmethod
       
    def register_routes(app):
        @app.route("/categories")
        def list_categories():
            categories = CategoryRepository.get_all()
            return render_template("categories/categories.html", categories=categories)

        @app.route("/categories/register", methods=["GET", "POST"])
        def register_category():
            if request.method == "POST":
                name = request.form.get("name")
                CategoryRepository.create(name)
                return redirect(url_for("list_categories"))
            return render_template("categories/register.html")
