from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt, jwt_required, get_jwt_identity
from datetime import timedelta
from app.utils import redirect_if_authenticated
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
@redirect_if_authenticated
def register():
    from app.models import db, User

    data = request.json

    if not data or not data.get('username') or not data.get('password') or not data.get('email'):
        return jsonify({'msg':'Invalid input'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'msg':'Email already exists'}), 400
    
    new_user = User(username=data['username'], email=data['email'], password=data['password'])

    db.session.add(new_user)
    db.session.commit()
    return jsonify({'msg': 'User registered succesfully'}), 201


@auth_bp.route('/login', methods=['POST'])
@redirect_if_authenticated
def login():
    from app.models import User

    data = request.json

    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'msg':'Invalid input'})
    
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not user.verify_password(data['password']):
        return jsonify({'msg': 'Invalid username or password'})
    
    access_token = create_access_token(identity=user.uuid, expires_delta=timedelta(hours=24))
    refresh_token = create_refresh_token(identity=user.uuid)
    
    return jsonify({
        'msg':'Login successful',
        'access_token':access_token,
        'refresh_token': refresh_token
    })


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    from app import redis_client
    jti = get_jwt()['jti']
    # exp = get_jwt()['exp']s

    redis_client.setex(jti, timedelta(hours=1), "revoked") 

    return jsonify({"msg": "Successfully logged out"}), 200


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    """Generate a new access token using the refresh token."""
    user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=user_id)

    return jsonify(access_token=new_access_token), 200