from app.database.connection import get_db_connection
import sqlite3

class User:
    """User model for database operations"""
    
    @staticmethod
    def get_all():
        """Get all users (excluding passwords)"""
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, name, email FROM users")
                users = cursor.fetchall()
                return [dict(user) for user in users]
        except sqlite3.Error:
            return None
    
    @staticmethod
    def get_by_id(user_id):
        """Get user by ID (excluding password)"""
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, name, email FROM users WHERE id = ?", (user_id,))
                user = cursor.fetchone()
                return dict(user) if user else None
        except sqlite3.Error:
            return None
    
    @staticmethod
    def get_by_email(email):
        """Get user by email (including password for login)"""
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
                user = cursor.fetchone()
                return dict(user) if user else None
        except sqlite3.Error:
            return None
    
    @staticmethod
    def create(name, email, hashed_password):
        """Create a new user"""
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                    (name, email, hashed_password)
                )
                conn.commit()
                return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None  # Email already exists
        except sqlite3.Error:
            return None
    
    @staticmethod
    def update(user_id, name, email):
        """Update user information"""
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE users SET name = ?, email = ? WHERE id = ?",
                    (name, email, user_id)
                )
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.IntegrityError:
            return None  # Email already exists
        except sqlite3.Error:
            return False
    
    @staticmethod
    def delete(user_id):
        """Delete a user"""
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error:
            return False
    
    @staticmethod
    def search_by_name(name):
        """Search users by name"""
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, name, email FROM users WHERE name LIKE ?", (f'%{name}%',))
                users = cursor.fetchall()
                return [dict(user) for user in users]
        except sqlite3.Error:
            return None
    
    @staticmethod
    def exists(user_id):
        """Check if user exists"""
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
                return cursor.fetchone() is not None
        except sqlite3.Error:
            return False 