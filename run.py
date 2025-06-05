import os
import sys

# Adiciona o diretório raiz ao path para permitir importações
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
import logging

app = create_app()

# Ativa logs detalhados do Flask e SQLAlchemy
logging.basicConfig(level=logging.DEBUG)
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
