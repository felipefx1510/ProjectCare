# ProjectCare

ProjectCare é um sistema web para conectar responsáveis por idosos a cuidadores profissionais, facilitando o processo de contratação, acompanhamento e gerenciamento de cuidados domiciliares.

## Funcionalidades
- Cadastro de usuários como Responsável ou Cuidador
- Cadastro de idosos vinculados a responsáveis
- Listagem de cuidadores e idosos disponíveis
- Gerenciamento de contratos entre responsáveis e cuidadores
- Avaliação de cuidadores
- Interface moderna e responsiva

## Tecnologias Utilizadas
- Python 3
- Flask
- SQLAlchemy
- Flask-Migrate
- PostgreSQL
- Bootstrap 5

## Estrutura de Pastas
```
app/
  models/         # Modelos do banco de dados
  routes/         # Rotas e views Flask
  services/       # Lógica de negócio
  static/         # Arquivos estáticos (imagens, CSS)
  templates/      # Templates HTML (Jinja2)
  run.py          # Ponto de entrada da aplicação
config.py         # Configurações do projeto
requirements.txt  # Dependências Python
.env              # Variáveis de ambiente
```

## Instalação e Execução
1. Clone o repositório e acesse a pasta do projeto.
2. Crie um ambiente virtual e ative-o:
   ```pwsh
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
3. Instale as dependências:
   ```pwsh
   pip install -r requirements.txt
   ```
4. Configure o arquivo `.env` com as variáveis `DATABASE_URL` e `SECRET_KEY`.
5. Execute as migrações do banco de dados:
   ```pwsh
   flask db upgrade
   ```
6. Inicie o servidor Flask:
   ```pwsh
   python -m app.run
   ```
   
## Contato
- Breno Siqueira — brenosiqueira@hotmail.com
- Felipe Felix — felipefelix@hotmail.com

---
© 2025 ProjectCare. Todos os direitos reservados.
