# ProjectCare - Technical Documentation

## Overview

ProjectCare is a web application designed to connect caregivers with elderly people who need care. The platform serves as a marketplace where responsible people (family members or guardians) can find and hire qualified caregivers for their elderly relatives.

### Problem Statement

Many elderly people require specialized care, but finding qualified caregivers can be challenging for family members. ProjectCare aims to solve this problem by:

1. Providing a platform where caregivers can register and showcase their qualifications
2. Allowing responsible people to search for and connect with caregivers
3. Facilitating the creation and management of care contracts
4. Ensuring a safe and reliable caregiving experience

## Technologies Used

### Core Technologies

- **Flask**: A lightweight Python web framework that provides tools and libraries for building web applications
  - Used for routing, request handling, and template rendering
  - Blueprints are used to organize the application into modular components

- **SQLAlchemy**: An Object-Relational Mapping (ORM) library for Python
  - Allows interaction with the database using Python objects instead of raw SQL
  - Handles database connections, queries, and transactions

- **PostgreSQL**: A powerful, open-source relational database system
  - Stores all application data (users, caregivers, contracts, etc.)
  - Provides reliability and support for complex queries

### Additional Technologies

- **Flask-Migrate**: An extension that handles SQLAlchemy database migrations
  - Uses Alembic under the hood to manage database schema changes
  - Provides commands for creating and applying migrations

- **Jinja2**: A template engine for Python
  - Used to render HTML templates with dynamic data
  - Supports template inheritance, loops, conditionals, and more

- **python-dotenv**: A library for loading environment variables from a .env file
  - Used to manage configuration settings like database connection strings and secret keys

## Project Structure

### Top-Level Directories and Files

- **app/**: The main application package
  - Contains all the application code, including models, routes, and templates
  
- **migrations/**: Contains database migration files
  - Generated and managed by Flask-Migrate
  - Tracks changes to the database schema over time
  
- **test/**: Contains test files for the application
  - Uses the unittest framework for testing
  - Includes tests for models and other components
  
- **.junie/**: Documentation directory
  - Contains guidelines and explanations for developers
  
- **config.py**: Configuration file (currently commented out)
  - Would normally contain application configuration settings
  
- **requirements.txt**: Lists all Python dependencies
  - Used to install required packages with pip
  
- **.env**: Environment variables file (not tracked in git)
  - Contains sensitive configuration like database credentials and secret keys

### App Directory Structure

- **models/**: Database models
  - Each file defines a different database table and its relationships
  
- **routes/**: Route handlers (controllers)
  - Organized into blueprints for different parts of the application
  
- **services/**: Business logic
  - Contains services that handle operations on models
  
- **static/**: Static files (CSS, JavaScript, images)
  - Served directly to the client
  
- **templates/**: HTML templates
  - Organized by blueprint/feature
  
- **__init__.py**: Application factory
  - Creates and configures the Flask application
  
- **run.py**: Entry point for running the application

## File-by-File Explanation

### App Package

#### app/__init__.py

This file contains the application factory function `create_app()` which:
- Creates a new Flask application
- Configures the application (secret key, database URI, etc.)
- Initializes extensions (SQLAlchemy, Flask-Migrate)
- Creates database tables if they don't exist
- Registers blueprints for different parts of the application

```python
def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev_key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:Soldier2003!@localhost:5432/ProjectCare')
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Register blueprints
    # ...
    
    return app
```

#### app/run.py

A simple script that creates the application and runs it in development mode:

```python
from . import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
```

### Models

#### app/models/caregiver.py

Defines the `Caregiver` model, representing healthcare providers in the system:
- Personal information (name, CPF, phone, email, address)
- Professional information (specialty, experience, education, expertise_area, skills, rating)
- Relationship with contracts

```python
class Caregiver(db.Model):
    __tablename__ = "caregiver"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    # ... other fields ...
    
    # Relationship with contracts
    contracts = db.relationship("Contract", back_populates="caregiver", cascade="all, delete-orphan")
```

#### app/models/elderly.py

Defines the `Elderly` model, representing elderly people who need care:
- Personal information (name, birthdate, gender, address)
- Relationship with responsible people

```python
class Elderly(db.Model):
    __tablename__ = "elderly"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    # ... other fields ...
    
    # Relationship with responsible people
    responsible_id = db.Column(db.Integer, db.ForeignKey("responsible.id"), nullable=False)
    responsible = db.relationship("Responsible", back_populates="elderly")
```

#### app/models/responsible.py

Defines the `Responsible` model, representing people responsible for elderly individuals:
- Personal information (name, CPF, phone, email)
- Relationships with elderly people and contracts

```python
class Responsible(db.Model):
    __tablename__ = "responsible"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    # ... other fields ...
    
    # Relationships
    elderly = db.relationship("Elderly", back_populates="responsible", cascade="all, delete-orphan")
    contracts = db.relationship("Contract", back_populates="responsible", cascade="all, delete-orphan")
```

#### app/models/contract.py

Defines the `Contract` model, representing agreements between caregivers and responsible people:
- Contract details (start_date, end_date)
- Relationships with caregivers and responsible people

```python
class Contract(db.Model):
    __tablename__ = "contract"
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    
    # Relationships
    responsible_id = db.Column(db.Integer, db.ForeignKey("responsible.id"), nullable=False)
    caregiver_id = db.Column(db.Integer, db.ForeignKey("caregiver.id"), nullable=False)
    responsible = db.relationship("Responsible", back_populates="contracts")
    caregiver = db.relationship("Caregiver", back_populates="contracts")
```

### Routes (Blueprints)

#### app/routes/home.py

Defines the blueprint for the home page:
- Creates a blueprint with the URL prefix "/"
- Defines a route for the root URL that renders the home template

```python
home_bp = Blueprint("home", __name__, url_prefix="/")

@home_bp.route("/", methods=["GET"])
def home():
    return render_template("home/home.html")
```

#### app/routes/caregivers.py

Defines the blueprint for caregiver-related routes:
- Creates a blueprint with the URL prefix "/caregivers"
- Defines a route for listing all caregivers

```python
caregivers_bp = Blueprint("caregivers", __name__, url_prefix="/caregivers")

@caregivers_bp.route("/", methods=["GET"])
def list_caregivers():
    caregivers = caregiver_service.get_all_caregivers()
    return render_template("caregivers/list.html", caregivers=caregivers)
```

#### app/routes/contact.py

Defines the blueprint for the contact page:
- Creates a blueprint with the URL prefix "/contact"
- Defines a route for the contact page

```python
contact_bp = Blueprint("contact", __name__, url_prefix="/contact")

@contact_bp.route("/", methods=["GET"])
def contact():
    return render_template("contact/contact.html")
```

#### app/routes/login.py

Defines the blueprint for user authentication:
- Creates a blueprint with the URL prefix "/login"
- Defines a route for the login page that handles both GET and POST requests
- Currently, the authentication logic is not fully implemented

```python
login_bp = Blueprint("login", __name__, url_prefix="/login")

@login_bp.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Authentication logic would go here
        return redirect(url_for('home.home'))
    return render_template("login/login.html")
```

#### app/routes/register.py

Defines the blueprint for user registration:
- Creates a blueprint with the URL prefix "/register"
- Defines routes for registering responsible people and caregivers

```python
register_bp = Blueprint("register", __name__, url_prefix="/register")

@register_bp.route("/", methods=["GET", "POST"])
def register():
    return render_template("login/register.html")

@register_bp.route('/responsible', methods=['POST'])
def register_responsible():
    # Get form data and create a Responsible object
    # ...
    return redirect(url_for('login.login'))

@register_bp.route('/caregiver', methods=['POST'])
def register_caregiver():
    # Get form data and create a Caregiver object
    # ...
    return redirect(url_for('login.login'))
```

### Templates

The application uses Jinja2 templates organized by feature:
- **home/home.html**: The home page template
- **caregivers/list.html**: Template for listing caregivers
- **contact/contact.html**: The contact page template
- **login/login.html**: The login page template
- **login/register.html**: The registration page template
- **fragments/navbar.html**: A reusable navigation bar template

### Static Files

The application includes static files like images in the `app/static/images/` directory.

## Database Structure

### Models and Relationships

The database has four main tables:
1. **caregiver**: Stores information about caregivers
2. **elderly**: Stores information about elderly people
3. **responsible**: Stores information about responsible people
4. **contract**: Stores information about contracts between caregivers and responsible people

The relationships between these tables are:
- A responsible person can be associated with multiple elderly people (one-to-many)
- A responsible person can have multiple contracts (one-to-many)
- A caregiver can have multiple contracts (one-to-many)
- A contract connects one caregiver with one responsible person (many-to-one for both)

### Migrations

Database migrations are managed using Flask-Migrate:
- Migration files are stored in the `migrations/versions/` directory
- Each migration file represents a change to the database schema
- Migrations can be created using `flask db migrate -m "description"`
- Migrations can be applied using `flask db upgrade`

## Authentication Flow

The authentication flow is not fully implemented yet, but the structure is in place:
1. Users (caregivers or responsible people) register through the registration page
2. Registration data is processed by the appropriate route handler
3. User information is saved to the database
4. Users are redirected to the login page
5. The login page would authenticate users (not implemented yet)
6. After successful authentication, users would be redirected to the home page

## Configuration

The application uses environment variables for configuration:
- **DATABASE_URL**: The PostgreSQL connection string
- **SECRET_KEY**: A secret key for securing sessions and cookies

These variables can be set in a `.env` file in the project root directory.

If the `DATABASE_URL` is not set, the application uses a default connection string:
```
postgresql://postgres:Soldier2003!@localhost:5432/ProjectCare
```

## Running the Application

### Development

To run the application in development mode:
1. Create and activate a virtual environment:
   ```
   python -m venv .venv
   .venv\Scripts\activate
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up environment variables in a `.env` file
4. Run the application:
   ```
   python -m app.run
   ```

The application will start in debug mode, which provides:
- Automatic reloading when code changes
- Detailed error pages
- The interactive debugger

### Production

For production deployment, you would typically:
1. Use a WSGI server like Gunicorn instead of the built-in Flask server
2. Set `debug=False` to disable the interactive debugger
3. Use environment variables for configuration instead of a `.env` file
4. Consider using a reverse proxy like Nginx in front of the application

## Areas for Improvement

1. **Authentication**: The authentication system is not fully implemented. Consider using Flask-Login or another authentication library.

2. **Password Security**: Passwords are currently stored in plain text. They should be hashed using a library like Werkzeug's security functions or passlib.

3. **Form Validation**: There's no validation for form inputs. Consider using Flask-WTF for form handling and validation.

4. **Error Handling**: The application doesn't have comprehensive error handling. Add try-except blocks and error pages.

5. **Testing**: While there's a test directory, more comprehensive tests would improve reliability.

6. **Configuration**: Consider using the commented-out `config.py` file for a more structured configuration approach.

7. **API Documentation**: If the application exposes APIs, consider adding documentation using Swagger/OpenAPI.

8. **Logging**: Add logging to help with debugging and monitoring.

9. **Frontend Framework**: Consider using a frontend framework like React or Vue.js for a more interactive user experience.

10. **Containerization**: Consider using Docker to containerize the application for easier deployment.