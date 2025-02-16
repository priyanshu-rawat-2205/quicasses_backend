from sqlalchemy.dialects.mssql import JSON
from datetime import datetime
from app import db

class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    creater_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    questions = db.Column(JSON, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    creator = db.relationship('User', backref='assessment')

    def __init__(self, title, description, creator_id, questions):
        self.title = title
        self.description = description
        self.created_id = creator_id
        self.questions = questions

    def to_dict(self):
        """Convert model instance to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "creator_id": self.creator_id,
            "questions": self.questions,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
