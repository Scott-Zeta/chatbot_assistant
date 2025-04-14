from werkzeug.security import generate_password_hash
from config.settings import Config
from app.modules.db import db, User

class UserService:
  def create_user(self, email, password):
    if User.query.filter_by(email=email).first():
        return {'error': 'User already exists'}, 409

    hashed_pw = generate_password_hash(password)
    new_user = User(email=email, password=hashed_pw)

    db.session.add(new_user)
    db.session.commit()

    return {'message': 'User registered successfully'}, 201
  
  def authenticate_user():
    """Authenticates a user"""
    pass