from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Enum

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(Enum('free', 'subscribed', 'admin', name='role_types'), nullable=False, default='free')
    created_at = db.Column(db.DateTime, default=datetime.now)
    edited_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    assistants = db.relationship('Assistant', backref='user', lazy=True)

class Assistant(db.Model):
    __tablename__ = 'assistants'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    assistant_id = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    model = db.Column(db.String(255), nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    edited_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)