#!/usr/bin/env python3
"""
Startup script for the User Management System.
This script starts the Flask application with proper error handling.
"""

import sys
import os

def start_application():
    """Start the Flask application"""
    print("🎯 User Management System")
    print("=" * 40)
    
    try:
        # Add the current directory to Python path if needed
        script_dir = os.path.dirname(os.path.abspath(__file__))
        if script_dir not in sys.path:
            sys.path.insert(0, script_dir)
        
        # Import and create the application
        from app import create_app
        
        app = create_app()
        
        print("✅ Database initialized successfully!")
        print("🚀 Starting User Management System...")
        print("=" * 50)
        print(f"📍 Server will be available at: http://{app.config['HOST']}:{app.config['PORT']}")
        print("🛑 Press Ctrl+C to stop the server")
        print("-" * 50)
        
        # Start the Flask application
        app.run(
            host=app.config['HOST'],
            port=app.config['PORT'],
            debug=app.config['DEBUG']
        )
        
    except KeyboardInterrupt:
        print("\n\n🛑 Application stopped by user")
        return 0
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure all dependencies are installed: pip install -r requirements.txt")
        return 1
    except Exception as e:
        print(f"\n❌ Application error: {e}")
        return 1

if __name__ == '__main__':
    exit(start_application()) 