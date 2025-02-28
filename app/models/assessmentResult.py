from sqlalchemy.dialects.mssql import JSON
from datetime import datetime
from app import db

class AssessmentResult(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    assessment_uuid = db.Column(db.String(36), db.ForeignKey('assessment.uuid', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('user.uuid', ondelete="CASCADE"), nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    correct_answers = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Float, nullable=False)  
    submitted_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    answers = db.Column(JSON, nullable=False)

    user = db.relationship("User", backref="assessment_results")
    assessment = db.relationship('Assessment', backref=db.backref('results', lazy=True))

    def to_dict(self):
        """Convert object to dictionary for API response"""
        return {
            "id": self.id,
            "assessment_uuid": self.assessment_uuid,
            "user_id": self.user_id,
            "total_questions": self.total_questions,
            'answers': self.answers,
            "correct_answers": self.correct_answers,
            "score": self.score,
            "submitted_at": self.submitted_at.isoformat()
        }
