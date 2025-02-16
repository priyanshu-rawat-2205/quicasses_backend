from flask import jsonify
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request

def redirect_if_authenticated(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            return jsonify({"message": "You are already logged in!"}), 403 
        except Exception:
            return fn(*args, **kwargs)
    return wrapper
