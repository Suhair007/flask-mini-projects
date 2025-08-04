from app import create_app

if __name__ == '__main__':
    app = create_app()
    print("🚀 Starting User Management System...")
    print(f"📍 Server will be available at: http://{app.config['HOST']}:{app.config['PORT']}")
    print("🛑 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']

    )
