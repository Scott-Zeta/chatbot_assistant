from flask import Blueprint, request, jsonify
from app.services.user_service import UserService

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
    # Placeholder for login logic
    return "User login endpoint"
  
@user_bp.route('/logout', methods=["POST"])
def logout():
    # Placeholder for logout logic
    return "User logout endpoint"

@user_bp.route('/profile/<user_id>', methods=["GET"])
def get_user_profile(user_id):
    # Placeholder for getting user profile logic
    return f"User profile for user_id: {user_id}"
  
@user_bp.route('/profile', methods=["GET"])
def profile():
    # Placeholder for profile logic
    return "User profile endpoint"
  
