from app import db
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    uuid = db.Column(db.String(36), default=lambda: str(uuid4()), unique=True, primary_key=True, nullable=False)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    @property
    def password(self):
        raise AttributeError("Password is not readable!")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.email}>"