from functools import wraps
from flask import request, jsonify, g
from config.settings import Config
from app.models.db import User
import jwt


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            parts = request.headers['Authorization'].split()
            if len(parts) == 2 and parts[0].lower() == 'bearer':
                token = parts[1]

        if not token:
            return jsonify({'error': 'Token is missing'}), 401

        try:
            data = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
            g.current_user = User.query.get(data['user_id'])
            if not g.current_user:
                return jsonify({'error': 'User not found'}), 404
            g.user_role = data['role']
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 403

        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if g.user_role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated


def token_and_admin_required(f):
    @token_required
    @admin_required
    def wrapper(*args, **kwargs):
        return f(*args, **kwargs)
    return wrapper