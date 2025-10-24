"""
Authentication module for Urban Mobility Backend System
Handles user authentication, password hashing, and role-based access control
"""

import sqlite3
import bcrypt
import getpass
from database import get_connection, close_connection

def hash_password(password):
    """Hash password using bcrypt"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)

def verify_password(stored_password, provided_password):
    """Verify password against stored hash"""
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password)

def authenticate_user(username, password):
    """Authenticate user and return role if successful"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Look for user with plain text username first
        cursor.execute('SELECT password_hash, role FROM Users WHERE username = ?', (username,))
        result = cursor.fetchone()
        
        if result:
            # Handle Super Admin hardcoded password
            if username == 'super_admin' and password == 'Admin_123?':
                return result[1]  # Return user role
            elif verify_password(result[0], password):
                return result[1]  # Return user role
        return None
    except Exception as e:
        print(f"Authentication error: {e}")
        return None
    finally:
        close_connection(conn)

def login():
    """Handle user login process"""
    print("\n=== LOGIN ===")
    username = input("Enter username: ").strip()
    password = getpass.getpass("Enter password: ")
    
    role = authenticate_user(username, password)
    if role:
        print(f"Login successful! Welcome, {username} ({role})")
        return username, role
    else:
        print("Authentication failed. Invalid username or password.")
        return None, None

def change_password(username):
    """Allow user to change their own password"""
    print("\n=== CHANGE PASSWORD ===")
    current_password = getpass.getpass("Enter current password: ")
    
    # Verify current password
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('SELECT password_hash FROM Users WHERE username = ?', (username,))
        result = cursor.fetchone()
        
        if not result or not verify_password(result[0], current_password):
            print("Current password is incorrect.")
            return False
        
        # Get new password
        new_password = getpass.getpass("Enter new password: ")
        confirm_password = getpass.getpass("Confirm new password: ")
        
        if new_password != confirm_password:
            print("Passwords do not match.")
            return False
        
        # Validate new password
        if not validate_password(new_password):
            print("Password does not meet requirements.")
            return False
        
        # Update password
        hashed_password = hash_password(new_password)
        cursor.execute('UPDATE Users SET password_hash = ? WHERE username = ?', 
                      (hashed_password, username))
        conn.commit()
        
        print("Password changed successfully!")
        return True
        
    except Exception as e:
        print(f"Error changing password: {e}")
        return False
    finally:
        close_connection(conn)

def validate_password(password):
    """Validate password according to requirements"""
    if len(password) < 12 or len(password) > 30:
        return False
    
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in "~!@#$%&_-+=`|\\(){}[]:;'<>,.?/" for c in password)
    
    return has_lower and has_upper and has_digit and has_special
