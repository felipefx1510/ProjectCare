from flask import render_template

class HomeController:
    @staticmethod
    def register_routes(app):
        @app.route("/")
        def home():
            return render_template("home.html")