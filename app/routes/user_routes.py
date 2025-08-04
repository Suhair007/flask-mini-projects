from flask import Blueprint, request, jsonify
from app.models.user import User
from app.utils.validators import validate_user_data, sanitize_input
from app.utils.auth import hash_password, verify_password
from app.utils.responses import success_response, error_response
import json

# Create Blueprint
user_bp = Blueprint('users', __name__)

@user_bp.route('/')
def home():
    return "User Management System"

@user_bp.route('/users', methods=['GET'])
def get_all_users():
    users = User.get_all()
    if users is None:
        return error_response('Database error', 500)
    return success_response(data={'users': users})

@user_bp.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    # Validate user_id is a positive integer
    if not user_id.isdigit() or int(user_id) <= 0:
        return error_response('Invalid user ID', 400)
    
    user = User.get_by_id(user_id)
    if user:
        return success_response(data={'user': user})
    else:
        return error_response('User not found', 404)

@user_bp.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        if not data:
            return error_response('Invalid JSON data', 400)
        
        # Validate input data
        is_valid, errors = validate_user_data(data, ['name', 'email', 'password'])
        if not is_valid:
            return error_response('Validation failed', 400, errors)
        
        # Check if email already exists
        existing_user = User.get_by_email(data['email'].strip())
        if existing_user:
            return error_response('Email already exists', 409)
        
        # Sanitize and hash password
        name = sanitize_input(data['name'])
        email = sanitize_input(data['email'])
        hashed_password = hash_password(data['password'])
        
        user_id = User.create(name, email, hashed_password)
        if user_id is None:
            return error_response('Failed to create user', 500)
        
        return success_response(message='User created successfully', status_code=201)
        
    except json.JSONDecodeError:
        return error_response('Invalid JSON format', 400)

@user_bp.route('/user/<user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        # Validate user_id
        if not user_id.isdigit() or int(user_id) <= 0:
            return error_response('Invalid user ID', 400)
        
        data = request.get_json()
        if not data:
            return error_response('Invalid JSON data', 400)
        
        # Validate input data (name and email only for updates)
        is_valid, errors = validate_user_data(data, ['name', 'email'])
        if not is_valid:
            return error_response('Validation failed', 400, errors)
        
        # Check if user exists
        if not User.exists(user_id):
            return error_response('User not found', 404)
        
        # Check if email is already taken by another user
        existing_user = User.get_by_email(data['email'].strip())
        if existing_user and existing_user['id'] != int(user_id):
            return error_response('Email already exists', 409)
        
        # Sanitize and update
        name = sanitize_input(data['name'])
        email = sanitize_input(data['email'])
        
        result = User.update(user_id, name, email)
        if result is None:
            return error_response('Email already exists', 409)
        elif not result:
            return error_response('Failed to update user', 500)
        
        return success_response(message='User updated successfully')
        
    except json.JSONDecodeError:
        return error_response('Invalid JSON format', 400)

@user_bp.route('/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    # Validate user_id
    if not user_id.isdigit() or int(user_id) <= 0:
        return error_response('Invalid user ID', 400)
    
    # Check if user exists
    if not User.exists(user_id):
        return error_response('User not found', 404)
    
    if User.delete(user_id):
        return success_response(message='User deleted successfully')
    else:
        return error_response('Failed to delete user', 500)

@user_bp.route('/search', methods=['GET'])
def search_users():
    name = request.args.get('name')
    
    if not name or not name.strip():
        return error_response('Please provide a name to search', 400)
    
    # Sanitize search term
    search_term = sanitize_input(name)
    if len(search_term) < 2:
        return error_response('Search term must be at least 2 characters', 400)
    
    users = User.search_by_name(search_term)
    if users is None:
        return error_response('Database error', 500)
    
    return success_response(data={'users': users})

@user_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data:
            return error_response('Invalid JSON data', 400)
        
        # Validate required fields
        if not data.get('email') or not data.get('password'):
            return error_response('Email and password are required', 400)
        
        # Validate email format
        from app.utils.validators import validate_email_format
        email_valid, email_error = validate_email_format(data['email'].strip())
        if not email_valid:
            return error_response(f'Email: {email_error}', 400)
        
        email = sanitize_input(data['email'])
        password = data['password']
        
        user = User.get_by_email(email)
        
        if user:
            # Verify the password against the stored hash
            stored_password_hash = user['password']
            if verify_password(password, stored_password_hash):
                return success_response(
                    data={'user_id': user['id']},
                    message='Login successful'
                )
            else:
                return error_response('Invalid password', 401)
        else:
            return error_response('User not found', 404)
            
    except json.JSONDecodeError:
        return error_response('Invalid JSON format', 400) 