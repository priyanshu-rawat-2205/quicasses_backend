from flask import Blueprint
from .auth import auth_bp

main_bp = Blueprint('main', __name__)

def register_blueprints(app):
    app.register_blueprint(auth_bp)