<<<<<<< HEAD
from flask import Flask, render_template
=======
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
>>>>>>> ee7f7ed0c13ecd43596e39693f8de18364c0176f

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(
        debug=True,
    ) 