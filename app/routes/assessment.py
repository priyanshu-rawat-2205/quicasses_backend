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


#Read by ID   
@assessment_bp.route("/<uuid:uuid>", methods=['GET'])
@jwt_required()
def read(uuid):
    from app.models import Assessment

    assessment = Assessment.query.get(uuid)
    if not assessment:
        return jsonify({"msg": "Assessment not found"}), 404
    return jsonify(assessment.to_dict()), 200


@assessment_bp.route("/<uuid:uuid>", methods=["PUT"])
@jwt_required()
def update(uuid):
    from app.models import db, Assessment

    assessment = Assessment.query.get(uuid)
    if not assessment:
        return jsonify({"msg": "Assessment not found"}), 404

    user_id = get_jwt_identity()
    if assessment.creator_id != user_id:
        return jsonify({"msg": "Unauthorized"}), 403

    data = request.get_json()
    assessment.title = data.get("title", assessment.title)
    assessment.description = data.get("description", assessment.description)
    assessment.questions = data.get("questions", assessment.questions)

    db.session.commit()
    return jsonify(assessment.to_dict()), 200


@assessment_bp.route("/<uuid:uuid>", methods=["DELETE"])
@jwt_required()
def delete(uuid):
    from app.models import db, Assessment

    assessment = Assessment.query.get(uuid)
    if not assessment:
        return jsonify({"msg": "Assessment not found"}), 404

    user_id = get_jwt_identity()
    if assessment.creator_id != user_id:
        return jsonify({"msg": "Unauthorized"}), 403

    db.session.delete(assessment)
    db.session.commit()
    return jsonify({"msg": "Assessment deleted successfully"}), 200

@assessment_bp.route('/my-assessments', methods=['GET'])
@jwt_required()  
def read_my_assessments():
    from app.models import Assessment

    user_id = get_jwt_identity()
    assessments = Assessment.query.filter_by(creator_id=user_id).all()

    if not assessments:
        return jsonify({'msg':'You have not created any assessments.'})

    return jsonify([{
        "uuid": assessment.uuid,
        "title": assessment.title,
        "description": assessment.description,
        "questions": assessment.questions,
        "created_at": assessment.created_at
    } for assessment in assessments]), 200