from flask_sqlalchemy import SQLAlchemy
import uuid
from passlib.hash import pbkdf2_sha256
from datetime import datetime

db = SQLAlchemy()

class Upload(db.Model):
    __tablename__ = 'uploads'
    
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True, nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    file_data = db.Column(db.LargeBinary, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    @staticmethod
    def create(filename, file_data, password):
        upload = Upload(
            uuid=str(uuid.uuid4()),
            filename=filename,
            file_data=file_data,
            password_hash=pbkdf2_sha256.hash(password)
        )
        return upload
    
    def check_password(self, password):
        return pbkdf2_sha256.verify(password, self.password_hash)