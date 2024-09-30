from flask import Flask
from flasgger import Swagger
from dotenv import load_dotenv
from .config import Config
from .utils import call_service_with_retries, token_required
from .auth.routes import auth_bp
from .students.routes import students_bp
from .grades.routes import grades_bp
from .restrictions.routes import restrictions_bp
from .misc.routes import misc_bp

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    swagger_config = {
        "swagger": "2.0",
        "info": {
            "title": "Student Management API",
            "description": "API to manage students, grades, and restrictions.",
            "version": "1.0.0"
        },
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "JWT Authorization header using the Bearer scheme. Example: 'Bearer {token}'"
            }
        },
        "security": [
            {
                "Bearer": []
            }
        ],
        "schemes": [
            "http",
            "https"
        ],
        "specs": [
            {
                "endpoint": 'apispec_1',
                "route": '/apispec_1.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "headers": [],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/"
    }

    Swagger(app, config=swagger_config)

    app.register_blueprint(auth_bp)
    app.register_blueprint(students_bp)
    app.register_blueprint(grades_bp)
    app.register_blueprint(restrictions_bp)
    app.register_blueprint(misc_bp)

    return app

app = create_app()
