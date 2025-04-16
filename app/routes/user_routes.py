from flask import Blueprint, request, jsonify, g
from app.services.user_service import UserService
from app.utils.auth import token_required

user_bp = Blueprint('user', __name__)

user_service = UserService()

@user_bp.route('/signup', methods=["POST"])
def signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400

    response, status_code = user_service.create_user(email, password)
    return jsonify(response), status_code
  
@user_bp.route('/login', methods=["POST"])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400

    response, status_code = user_service.authenticate_user(email, password)
    return jsonify(response), status_code

@user_bp.route('/profile', methods=["GET"])
@token_required
def profile():
    current_user = g.get('current_user')
    if not current_user:
        return jsonify({'error': 'User not found'}), 404
    user_info = user_service.get_current_user(current_user)
    return jsonify(user_info), 200



  
