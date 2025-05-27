from . import create_app
import logging

app = create_app()

# Ativa logs detalhados do Flask e SQLAlchemy
logging.basicConfig(level=logging.DEBUG)
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

if __name__ == '__main__':
    app.run(debug=True)
