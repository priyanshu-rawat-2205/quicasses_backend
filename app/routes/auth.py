from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from datetime import timedelta
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    from app.models import db, User

    data = request.json

    if not data or not data.get('username') or not data.get('password') or not data.get('email'):
        return jsonify({'message':'Invalid input'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message':'Email already exists'}), 400
    
    new_user = User(username=data['username'], email=data['email'], password=data['password'])

    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered succesfully'}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    from app.models import User

    data = request.json

    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'message':'Invalid input'})
    
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not user.verify_password(data['password']):
        return jsonify({'message': 'Invalid username or password'})
    
    access_token = create_access_token(identity=user.id, expires_delta=timedelta(hours=24))
    
    return jsonify({
        'message':'Login successful',
        'access_token':access_token
    })
