from flask import Flask
from app.config import Config
from app.database.connection import init_database
from app.routes.user_routes import user_bp

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize database
    if not init_database():
        raise RuntimeError("Failed to initialize database")
    
    # Register blueprints
    app.register_blueprint(user_bp)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {'status': 'error', 'message': 'Resource not found'}, 404

    @app.errorhandler(500)
    def internal_error(error):
        return {'status': 'error', 'message': 'Internal server error'}, 500
    
    return app 