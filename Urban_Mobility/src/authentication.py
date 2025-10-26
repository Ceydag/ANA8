import sqlite3
import bcrypt
import getpass
from database import get_connection, close_connection
from system_logging import log_login_attempt, log_action
from session_management import create_session, terminate_session

def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)

def verify_password(stored_password, provided_password):
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password)

def authenticate_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        from encryption import decrypt_data
        
        cursor.execute('SELECT username, password_hash, role, temp_password FROM Users')
        all_users = cursor.fetchall()
        
        for db_username, stored_password_hash, role, temp_password in all_users:
            try:
                decrypted_username = decrypt_data(db_username)
                
                if db_username == 'super_admin' or decrypted_username == 'super_admin':
                    if username == 'super_admin' and password == 'Admin_123?':
                        log_login_attempt(username, True)
                        create_session(username, role)
                        return username, role, bool(temp_password)
                
                if decrypted_username.lower() == username.lower():
                    if verify_password(stored_password_hash, password):
                        log_login_attempt(username, True)
                        create_session(username, role)
                        return username, role, bool(temp_password)
                    else:
                        break
                        
            except Exception as decrypt_error:
                if db_username == username and username == 'super_admin' and password == 'Admin_123?':
                    log_login_attempt(username, True)
                    create_session(username, role)
                    return username, role, bool(temp_password)
        
        log_login_attempt(username, False)
        return None, None
        
    except Exception as e:
        print(f"Authentication error: {e}")
        log_action("system", f"Authentication error for user {username}", str(e), True)
        return None, None
    finally:
        close_connection(conn)

def logout_user(username):
    if terminate_session(username, "User logout"):
        log_action(username, "User logged out", "Session terminated by user")
        return True
    return False

def login():
    print("\n=== LOGIN ===")
    username = input("Enter username: ").strip()
    password = getpass.getpass("Enter password: ")
    
    auth_result = authenticate_user(username, password)
    if auth_result and auth_result[0]:
        username, role, has_temp_password = auth_result
        print(f"Login successful! Welcome, {username} ({role})")
        
        if has_temp_password:
            print("\n" + "="*60)
            print("You are currently using a temporary password.")
            print("You MUST change your password immediately for security reasons.")
            print("="*60)
            
            # Force password change (no current password required)
            if change_temp_password(username):
                print("Password changed successfully!")
                print("You can now continue using the system.")
            else:
                print("Password change failed. Please try again.")
                return None, None
        
        # Check for unread suspicious activities for System Admins and Super Admins
        if role in ["System Admin", "Super Admin"]:
            from system_logging import display_alert_if_suspicious
            display_alert_if_suspicious(username)
        
        return username, role
    else:
        print("Authentication failed. Invalid username or password.")
        return None, None

def change_temp_password(username):
    """Change password for users with temporary password (no current password required)"""
    print("\n=== CHANGE TEMPORARY PASSWORD ===")
    print("You are changing your temporary password.")
    print("Please enter a new secure password.")
    print("\nPassword Requirements:")
    print("• Length: 12-30 characters")
    print("• Must contain at least one lowercase letter (a-z)")
    print("• Must contain at least one uppercase letter (A-Z)")
    print("• Must contain at least one digit (0-9)")
    print("• Must contain at least one special character (~!@#$%&_-+=`|\\(){}[]:;'<>,.?/)")
    
    new_password = getpass.getpass("Enter new password: ")
    confirm_password = getpass.getpass("Confirm new password: ")
    
    if new_password != confirm_password:
        print("Passwords do not match.")
        return False
    
    if not new_password:
        print("Password cannot be empty.")
        return False
    
    # Validate password strength
    if not validate_password(new_password):
        print("Password validation failed: Invalid password format")
        print("Please ensure your password meets all the requirements listed above.")
        return False
    
    # Hash and update password
    hashed_password = hash_password(new_password)
    
    from crud_operations import update_user_password
    if update_user_password(username, hashed_password, username):
        print("Password changed successfully!")
        return True
    else:
        print("Failed to update password.")
        return False

def change_password(username):
    print("\n=== CHANGE PASSWORD ===")
    current_password = getpass.getpass("Enter current password: ")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        from encryption import decrypt_data
        
        # Find the user by decrypting all usernames
        cursor.execute('SELECT id, username, password_hash FROM Users')
        all_users = cursor.fetchall()
        
        user_id = None
        stored_password_hash = None
        
        for existing_id, existing_username, password_hash in all_users:
            try:
                # Try to decrypt the username
                decrypted_username = decrypt_data(existing_username)
                if decrypted_username.lower() == username.lower():
                    user_id = existing_id
                    stored_password_hash = password_hash
                    break
            except:
                # If decryption fails, check if it's a non-encrypted username (like super_admin)
                if existing_username.lower() == username.lower():
                    user_id = existing_id
                    stored_password_hash = password_hash
                    break
        
        if not user_id or not stored_password_hash:
            print("User not found.")
            return False
        
        if not verify_password(stored_password_hash, current_password):
            print("Current password is incorrect.")
            return False
        
        print("\nPassword Requirements:")
        print("• Length: 12-30 characters")
        print("• Must contain at least one lowercase letter (a-z)")
        print("• Must contain at least one uppercase letter (A-Z)")
        print("• Must contain at least one digit (0-9)")
        print("• Must contain at least one special character (~!@#$%&_-+=`|\\(){}[]:;'<>,.?/)")
        
        new_password = getpass.getpass("Enter new password: ")
        confirm_password = getpass.getpass("Confirm new password: ")
        
        if new_password != confirm_password:
            print("Passwords do not match.")
            return False
        
        if not validate_password(new_password):
            print("Password validation failed: Invalid password format")
            print("Please ensure your password meets all the requirements listed above.")
            return False
   
        hashed_password = hash_password(new_password)
        cursor.execute('UPDATE Users SET password_hash = ?, temp_password = 0 WHERE id = ?', 
                      (hashed_password, user_id))
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
