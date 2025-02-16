import redis
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from app.routes import register_blueprints
from app.config import Config
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager


db = SQLAlchemy()
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    #flask-sqlalchemy integration
    db.init_app(app)
 
    #jwt app init
    jwt.init_app(app)

    #flask-migrate integration
    Migrate(app, db)


    #model import
    from app import models  # noqa: F401

    #fix all CORS errors
    CORS(app)

    #register all route blueprints
    register_blueprints(app)

    return app

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return redis_client.get(jti) is not None 