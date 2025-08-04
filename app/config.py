import os

class Config:
    """Application configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'users.db')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    HOST = os.getenv('HOST', '127.0.0.1')  # Changed from 0.0.0.0 for security
    PORT = int(os.getenv('PORT', 5000))     # Changed from 5009 to standard 5000
    
    # Password requirements
    MIN_PASSWORD_LENGTH = 8
    REQUIRE_UPPERCASE = True
    REQUIRE_LOWERCASE = True
    REQUIRE_NUMBERS = True
    REQUIRE_SPECIAL_CHARS = True
    
    # Name validation
    MIN_NAME_LENGTH = 2
    MAX_NAME_LENGTH = 50 