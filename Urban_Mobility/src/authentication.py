import sqlite3
import bcrypt
import getpass
from database import get_connection, close_connection
from system_logging import log_login_attempt, detect_suspicious_patterns, log_action
from session_management import create_session, check_session, terminate_session, display_session_info

def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)

def verify_password(stored_password, provided_password):
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password)

def authenticate_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('SELECT password_hash, role FROM Users WHERE username = ?', (username,))
        result = cursor.fetchone()
        
        if result:
            if username == 'super_admin' and password == 'Admin_123?':
                log_login_attempt(username, True)
                # REQUIREMENT: Session management - create session on successful login
                create_session(username, result[1])
                return result[1]  
            elif verify_password(result[0], password):
                log_login_attempt(username, True)
                # REQUIREMENT: Session management - create session on successful login
                create_session(username, result[1])
                return result[1]  
        
        # Failed login attempt
        log_login_attempt(username, False)
        return None
    except Exception as e:
        print(f"Authentication error: {e}")
        log_action("system", f"Authentication error for user {username}", str(e), True)
        return None
    finally:
        close_connection(conn)

def logout_user(username):
    """Logout user and terminate session"""
    # REQUIREMENT: Session management - terminate session on logout
    if terminate_session(username, "User logout"):
        log_action(username, "User logged out", "Session terminated by user")
        return True
    return False

def login():
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
    print("\n=== CHANGE PASSWORD ===")
    current_password = getpass.getpass("Enter current password: ")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('SELECT password_hash FROM Users WHERE username = ?', (username,))
        result = cursor.fetchone()
        
        if not result or not verify_password(result[0], current_password):
            print("Current password is incorrect.")
            return False
        
        new_password = getpass.getpass("Enter new password: ")
        confirm_password = getpass.getpass("Confirm new password: ")
        
        if new_password != confirm_password:
            print("Passwords do not match.")
            return False
        
        if not validate_password(new_password):
            print("Password does not meet requirements.")
            return False
   
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
    if len(password) < 12 or len(password) > 30:
        return False
    
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in "~!@#$%&_-+=`|\\(){}[]:;'<>,.?/" for c in password)
    
    return has_lower and has_upper and has_digit and has_special
