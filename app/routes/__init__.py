from flask import Blueprint, Flask, jsonify
from .auth import auth_bp
from .assessment import assessment_bp

main_bp = Blueprint('main', __name__,)

@main_bp.route('/', methods=['GET'])
def index():
    return jsonify({'msg':'welcome to quicasses'})

def register_blueprints(app: Flask):
    app.register_blueprint(main_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(assessment_bp, url_prefix='/api/assessment')
    