# Diretrizes de Desenvolvimento - ProjectCare

Este documento contém informações relevantes para o desenvolvimento do projeto ProjectCare.

## Instruções de Configuração e Build

### Requisitos

- Python 3.8+
- PostgreSQL
- Dependências listadas em `requirements.txt`

### Configuração do Ambiente

1. Clone o repositório e navegue até a pasta do projeto
2. Crie um ambiente virtual Python:
   ```
   python -m venv .venv
   .venv\Scripts\activate
   ```
3. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```
4. Configure as variáveis de ambiente criando um arquivo `.env` na raiz do projeto:
   ```
   DATABASE_URL=postgresql://usuario:senha@localhost:5432/ProjectCare
   SECRET_KEY=sua_chave_secreta
   ```

   Nota: Se não for definida a variável `DATABASE_URL`, o sistema usará a conexão padrão: `postgresql://postgres:@localhost:5432/ProjectCare`

### Migrações de Banco de Dados

O projeto utiliza Flask-Migrate para gerenciar migrações de banco de dados:

1. Inicializar migrações (se ainda não existirem):
   ```
   flask db init
   ```

2. Criar uma nova migração após alterações nos modelos:
   ```
   flask db migrate -m "descrição da migração"
   ```

3. Aplicar migrações pendentes:
   ```
   flask db upgrade
   ```

### Executando o Projeto

Para iniciar o servidor de desenvolvimento:

```
python -m app.run
```

O servidor será iniciado em modo de desenvolvimento (debug=True).

## Informações de Testes

### Configuração de Testes

O projeto utiliza o framework `unittest` para testes. Os testes são armazenados no diretório `test/`.

Para executar testes, é necessário garantir que o diretório raiz do projeto esteja no `PYTHONPATH`. Os testes são configurados para usar um banco de dados SQLite em memória para isolamento.

### Executando Testes

Para executar um teste específico:

```
python test\nome_do_arquivo_de_teste.py
```

Para executar todos os testes (requer pytest):

```
pytest test\
```

**Nota**: Ao executar os testes, você pode ver um aviso de depreciação relacionado ao `datetime.datetime.utcnow()`. Este aviso não afeta a funcionalidade dos testes, mas indica que em versões futuras do Python esta função será removida. Considere atualizar o código para usar `datetime.datetime.now(datetime.UTC)` em uma futura refatoração.

### Teste de Conexão com o Banco de Dados

O projeto inclui um script para testar a conexão com o banco de dados:

```
python test\teste_db.py
```

Este script verifica se a variável de ambiente `DATABASE_URL` está definida e tenta estabelecer uma conexão com o banco de dados. É útil para diagnosticar problemas de conexão.

Atualmente, o projeto está configurado para usar um banco de dados PostgreSQL hospedado no Render.com. Você pode configurar seu próprio banco de dados PostgreSQL local ou remoto alterando a variável `DATABASE_URL` no arquivo `.env`.

### Criando Novos Testes

1. Crie um novo arquivo no diretório `test/` com o prefixo `test_`.
2. Importe o módulo `unittest` e as classes/funções que deseja testar.
3. Adicione o código para incluir o diretório raiz no path do Python:
   ```python
   import sys
   import os
   sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
   ```
4. Crie uma classe que herda de `unittest.TestCase`.
5. Implemente os métodos `setUp` e `tearDown` para configurar e limpar o ambiente de teste.
6. Adicione métodos de teste com o prefixo `test_`.

### Exemplo de Teste

```python
import unittest
import sys
import os

# Adicionar o diretório raiz ao path do Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models.caregiver import Caregiver

class TestCaregiverModel(unittest.TestCase):
    def setUp(self):
        # Configurar o app para testes
        self.app = create_app()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['TESTING'] = True
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        # Limpar após cada teste
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_caregiver(self):
        # Criar um cuidador de teste
        caregiver = Caregiver(
            name="Teste da Silva",
            cpf="123.456.789-00",
            phone="(11) 98765-4321",
            email="teste@example.com",
            password="senha123",
            specialty="Enfermagem",
            experience=5,
            education="Técnico em Enfermagem",
            expertise_area="Idosos",
            skills="Primeiros socorros, Medicação",
            rating=4.5,
            address="Rua Teste, 123"
        )

        # Adicionar ao banco de dados
        db.session.add(caregiver)
        db.session.commit()

        # Recuperar do banco de dados
        saved_caregiver = Caregiver.query.filter_by(email="teste@example.com").first()

        # Verificar se foi salvo corretamente
        self.assertIsNotNone(saved_caregiver)
        self.assertEqual(saved_caregiver.name, "Teste da Silva")
        self.assertEqual(saved_caregiver.cpf, "123.456.789-00")
        self.assertEqual(saved_caregiver.experience, 5)
        self.assertEqual(saved_caregiver.rating, 4.5)

if __name__ == '__main__':
    unittest.main()
```

## Informações Adicionais de Desenvolvimento

### Estrutura do Projeto

- `app/`: Diretório principal da aplicação
  - `models/`: Modelos de dados (SQLAlchemy)
  - `routes/`: Rotas da aplicação (Blueprints Flask)
  - `services/`: Camada de serviço para lógica de negócios
  - `static/`: Arquivos estáticos (imagens, CSS, JS)
  - `templates/`: Templates HTML (Jinja2)
  - `__init__.py`: Configuração e inicialização da aplicação
  - `run.py`: Script para executar a aplicação
- `migrations/`: Migrações de banco de dados
- `test/`: Testes automatizados
- `config.py`: Configurações da aplicação (atualmente comentado)

### Padrões de Código

- **Estilo de Código**: O projeto segue as convenções PEP 8 para Python.
- **Docstrings**: Métodos e classes devem incluir docstrings descritivos.
- **Type Hints**: O código utiliza type hints para melhorar a legibilidade e permitir verificação estática de tipos.
- **Padrão de Arquitetura**: O projeto segue uma arquitetura em camadas:
  - Modelos (Models): Representação dos dados
  - Serviços (Services): Lógica de negócios
  - Rotas (Routes): Endpoints da API e renderização de templates

### Banco de Dados

- O projeto utiliza PostgreSQL como banco de dados principal.
- SQLAlchemy é usado como ORM para interação com o banco de dados.
- As tabelas são criadas automaticamente na inicialização da aplicação se não existirem.
- Relacionamentos entre tabelas são definidos usando relações SQLAlchemy.

### Blueprints

A aplicação utiliza Blueprints do Flask para organizar as rotas:
- `home_bp`: Página inicial
- `caregivers_bp`: Gerenciamento de cuidadores
- `contact_bp`: Página de contato
- `login_bp`: Autenticação
- `register_bp`: Registro de usuários

### Segurança

- Senhas são armazenadas no banco de dados (recomenda-se implementar hash de senhas).
- A chave secreta da aplicação deve ser definida através da variável de ambiente `SECRET_KEY`.
