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

@assessment_bp.route('/', methods=['GET'])
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


@assessment_bp.route('/submit-assessment', methods=['POST'])
@jwt_required()
def submit_assessment():
    from app.models import Assessment, db, AssessmentResult

    # data = request.json
    # assessment_id = data.get("uuid")
    # user_id = get_jwt_identity()
    # user_answers = data.get("answers")  # { questionIndex: selectedOptionIndex }

    # if not assessment_id or user_answers is None:
    #     return jsonify({"error": "Invalid data"}), 400

    # # assessment = assessments.get(assessment_id)
    # assessment = Assessment.query.filter_by(uuid=assessment_id).first()

    # if not assessment:
    #     return jsonify({"error": "Assessment not found"}), 404

    # correct_count = 0
    # total_questions = len(assessment.questions)

    # for idx, question in enumerate(assessment.questions):
    #     correct_option = question["correctOption"]
    #     selected_option = user_answers.get(str(idx))

    #     if selected_option == correct_option:
    #         correct_count += 1

    # # score = (correct_count / total_questions) * 100  # Percentage score
    # score = (correct_count / total_questions) * 100 if total_questions > 0 else 0

    # result = AssessmentResult(
    #     assessment_uuid=assessment_id,
    #     user_id=user_id,
    #     total_questions=total_questions,
    #     correct_answers=correct_count,
    #     score=score
    # )

    # db.session.add(result)
    # db.session.commit()

    # return jsonify(result.to_dict()), 200

    current_user = get_jwt_identity()
    data = request.json  # Expecting {"answers": [{"question_id": 1, "selected_option": 2}, ...]}
    assessment_id = data.get("uuid")

    # Fetch assessment
    assessment = Assessment.query.get(assessment_id)
    if not assessment:
        return jsonify({"error": "Assessment not found"}), 404

    # Calculate Score
    total_questions = len(assessment.questions)
    correct_answers = 0

    for user_answer in data.get("answers", []):
        question_id = user_answer.get('question_id')
        selected_option = user_answer["selected_option"]
        
        # Find the correct answer for the question
        question = next((q for q in assessment.questions if q.get("question_id") == question_id), None)
        if question and question["correct_option"] == selected_option:
            correct_answers += 1

    score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0

    # Save the assessment result along with answers
    assessment_result = AssessmentResult(
        assessment_uuid=assessment_id,
        user_id=current_user,
        score=score,
        answers=data.get("answers", []),  # Store answers as JSON
        total_questions=total_questions,
        correct_answers=correct_answers
    )
    db.session.add(assessment_result)
    db.session.commit()

    return jsonify(assessment_result.to_dict()), 200


@assessment_bp.route('/results/<uuid:uuid>', methods=['GET'])
@jwt_required()
def get_assessment_results(uuid):
    from app.models import AssessmentResult, Assessment, User

    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    user_name = user.username
    
    assessment = Assessment.query.get(uuid)
    if not assessment:
        return jsonify({"error": "Assessment not found"}), 404

    assessment_title = assessment.title

    # Check if the current user is the creator of the assessment
    if assessment.creator_id != user_id:
        return jsonify({"error": "Unauthorized access"}), 403

    results = AssessmentResult.query.filter_by(assessment_uuid=str(uuid)).all()
    if(len(results) == 0):
        return jsonify({"msg": "No results found for this assessment"}), 404


    return jsonify([{
        'assessment_uuid': result.assessment_uuid,
        'assessment_title': assessment_title,
        'submitted_by': user_name,
        'user_id': result.user_id,
        'total_questions': result.total_questions,
        'correct_answers': result.correct_answers,
        'score': result.score,
        'submitted_at': result.submitted_at,
        'answers': result.answers
        } for result in results]), 200

