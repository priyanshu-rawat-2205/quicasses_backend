from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

assessment_bp = Blueprint('assessment', __name__)

@assessment_bp.route('/', methods=['POST'])
@jwt_required()
def create():
    from app.models import db, Assessment

    data = request.get_json()

    if not data.get('title') or not data.get('questions'):
        return jsonify({'msg':'title and questions are required'}), 400
    
    user_uuid = get_jwt_identity()

    new_assessment = Assessment(title=data.get('title'), description=data.get('description'), creator_id=user_uuid, questions=data.get('questions'))

    db.session.add(new_assessment)
    db.session.commit()

    return jsonify(new_assessment.to_dict()), 201    
    
