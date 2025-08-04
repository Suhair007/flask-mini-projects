import sqlite3
from contextlib import contextmanager
from app.config import Config
from app.utils.auth import hash_password

@contextmanager
def get_db_connection():
    """Context manager for database connections"""
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # Enable dict-like access
    try:
        yield conn
    finally:
        conn.close()

def init_database():
    """Initialize database connection and create tables if needed"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL
                )
            ''')
            
            # Add sample users with hashed passwords
            sample_users = [
                ('John Doe', 'john@example.com', 'SecurePass123!'),
                ('Jane Smith', 'jane@example.com', 'MySecret456@'),
                ('Bob Johnson', 'bob@example.com', 'StrongPwd789#')
            ]
            
            for name, email, password in sample_users:
                hashed_password = hash_password(password)
                cursor.execute(
                    "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                    (name, email, hashed_password)
                )
            
            print("Sample users created with hashed passwords:")
            for name, email, _ in sample_users:
                print(f"  - {name} ({email})")
            
            conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Database initialization failed: {e}")
        return False 