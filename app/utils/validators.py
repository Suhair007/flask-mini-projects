import re
from email_validator import validate_email, EmailNotValidError
from app.config import Config

def validate_email_format(email):
    """Validate email format using email-validator"""
    try:
        validate_email(email)
        return True, None
    except EmailNotValidError as e:
        return False, str(e)

def validate_password_strength(password):
    """Validate password strength"""
    errors = []
    
    if len(password) < Config.MIN_PASSWORD_LENGTH:
        errors.append(f"Password must be at least {Config.MIN_PASSWORD_LENGTH} characters long")
    
    if Config.REQUIRE_UPPERCASE and not re.search(r'[A-Z]', password):
        errors.append("Password must contain at least one uppercase letter")
    
    if Config.REQUIRE_LOWERCASE and not re.search(r'[a-z]', password):
        errors.append("Password must contain at least one lowercase letter")
    
    if Config.REQUIRE_NUMBERS and not re.search(r'\d', password):
        errors.append("Password must contain at least one number")
    
    if Config.REQUIRE_SPECIAL_CHARS and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        errors.append("Password must contain at least one special character")
    
    return len(errors) == 0, errors

def validate_name(name):
    """Validate user name"""
    if not name or not name.strip():
        return False, "Name cannot be empty"
    
    if len(name.strip()) < Config.MIN_NAME_LENGTH:
        return False, f"Name must be at least {Config.MIN_NAME_LENGTH} characters long"
    
    if len(name.strip()) > Config.MAX_NAME_LENGTH:
        return False, f"Name cannot exceed {Config.MAX_NAME_LENGTH} characters"
    
    # Check for valid characters (letters, spaces, hyphens, apostrophes)
    if not re.match(r"^[a-zA-Z\s\-']+$", name.strip()):
        return False, "Name can only contain letters, spaces, hyphens, and apostrophes"
    
    return True, None

def sanitize_input(data):
    """Sanitize input data by trimming whitespace"""
    if isinstance(data, str):
        return data.strip()
    return data

def validate_user_data(data, required_fields=None):
    """Comprehensive validation for user data"""
    if required_fields is None:
        required_fields = ['name', 'email', 'password']
    
    errors = []
    
    # Check for required fields
    for field in required_fields:
        if field not in data or not data[field]:
            errors.append(f"{field.capitalize()} is required")
    
    if errors:
        return False, errors
    
    # Sanitize inputs
    name = sanitize_input(data.get('name', ''))
    email = sanitize_input(data.get('email', ''))
    password = data.get('password', '')
    
    # Validate name
    name_valid, name_error = validate_name(name)
    if not name_valid:
        errors.append(name_error)
    
    # Validate email
    email_valid, email_error = validate_email_format(email)
    if not email_valid:
        errors.append(f"Email: {email_error}")
    
    # Validate password (only for create_user and login)
    if 'password' in required_fields:
        password_valid, password_errors = validate_password_strength(password)
        if not password_valid:
            errors.extend(password_errors)
    
    return len(errors) == 0, errors 