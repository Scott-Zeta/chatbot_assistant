import jwt as jwt
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from config.settings import Config
from app.models.db import db, User

class UserService:
  def create_user(self, email, password):
    if User.query.filter_by(email=email).first():
        return {'error': 'User already exists'}, 409

    hashed_pw = generate_password_hash(password)
    new_user = User(email=email, password=hashed_pw)

    db.session.add(new_user)
    db.session.commit()

    return {'message': 'User registered successfully'}, 201
  
  def authenticate_user(self, email, password):
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return {'error': 'Invalid credentials'}, 401

    token = jwt.encode({
        'user_id': str(user.id),
        'role': user.role,
        'exp': datetime.now() + timedelta(hours=int(Config.JWT_EXPIRATION_TIME))
    }, Config.JWT_SECRET_KEY, algorithm='HS256')

    return {'token': token}, 200