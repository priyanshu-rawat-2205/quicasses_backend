from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from app.routes import register_blueprints
from app.config import Config
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    #jwt integration
    JWTManager(app)

    #flask-sqlalchemy integration
    db.init_app(app)

    #flask-migrate integration
    Migrate(app, db)

    
    #model import
    from app import models  # noqa: F401

    CORS(app)
    register_blueprints(app)

    return app