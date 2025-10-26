import sqlite3
from database import get_connection, close_connection
from encryption import encrypt_data, decrypt_data
from system_logging import log_action
from session_management import get_current_user_id
import re

def create_user(user_data, current_user):
    conn = None
    try:
        conn = get_connection()
        if not conn:
            print("Failed to connect to database")
            return False
            
        cursor = conn.cursor()

        # Check for existing username by decrypting all usernames
        cursor.execute('SELECT id, username FROM Users')
        all_users = cursor.fetchall()
        
        for existing_id, existing_username in all_users:
            try:
                # Try to decrypt the username
                decrypted_username = decrypt_data(existing_username)
                if decrypted_username.lower() == user_data['username'].lower():
                    print(f"ERROR: Username '{user_data['username']}' is already taken.")
                    return False
            except:
                # If decryption fails, check if it's a non-encrypted username (like super_admin)
                if existing_username.lower() == user_data['username'].lower():
                    print(f"ERROR: Username '{user_data['username']}' is already taken.")
                    return False
        
        encrypted_username = encrypt_data(user_data['username'])

        encrypted_first_name = encrypt_data(user_data['first_name'])
        encrypted_last_name = encrypt_data(user_data['last_name'])
        
    
        cursor.execute('''
            INSERT INTO Users (username, password_hash, first_name, last_name, role, registration_date)
            VALUES (?, ?, ?, ?, ?, datetime('now'))
        ''', (
            encrypted_username,
            user_data['password_hash'],
            encrypted_first_name,
            encrypted_last_name,
            user_data['role']
        ))
        
        conn.commit()
        
        log_action(current_user, f"Created new {user_data['role']} user: {user_data['username']}")
        
        return True
        
    except sqlite3.OperationalError as e:
        if "database is locked" in str(e):
            print("Database is locked. Attempting to unlock...")
            from database import unlock_database
            if unlock_database():
                print("Database unlocked. Please try again.")
            else:
                print("Could not unlock database. Please restart the application.")
        else:
            print(f"Database error: {e}")
        return False
    except Exception as e:
        print(f"Error creating user: {e}")
        return False
    finally:
        if conn:
            close_connection(conn)

    
def search_user(username):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT username, role FROM Users WHERE username = ?
        ''', (username,))
        
        user = cursor.fetchone()
        close_connection(conn)
        return user
        
    except Exception as e:
        print(f"Error searching user: {e}")
        return None

def list_users(current_user):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT username, first_name, last_name, role, registration_date
            FROM Users
            ORDER BY registration_date DESC
        ''')
        
        users = cursor.fetchall()
        
        if not users:
            print("📋 No users found in the system.")
            return
        
        print("\n" + "=" * 80)
        print("    USER LIST")
        print("=" * 80)
        print(f"{'Username':<15} {'Name':<25} {'Role':<15} {'Registered':<20}")
        print("-" * 80)
        
        for username, first_name, last_name, role, reg_date in users:
            try:
                decrypted_username = decrypt_data(username)
                decrypted_first = decrypt_data(first_name)
                decrypted_last = decrypt_data(last_name)
                full_name = f"{decrypted_first} {decrypted_last}"
            except:
                decrypted_username = username
                full_name = f"{first_name} {last_name}"
            
            print(f"{decrypted_username:<15} {full_name:<25} {role:<15} {reg_date:<20}")
        
        close_connection(conn)
        
    except Exception as e:
        print(f"Error listing users: {e}")

def list_system_admins(current_user):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, username, first_name, last_name, role, registration_date
            FROM Users
            WHERE role = 'System Admin' AND username != 'super_admin'
            ORDER BY registration_date DESC
        ''')
        
        users = cursor.fetchall()
        
        if not users:
            print("No System Administrators found in the system.")
            print("Note: Super Admin account is protected and not shown in this list.")
            return
        
        print("\n" + "=" * 90)
        print("    SYSTEM ADMINISTRATORS LIST")
        print("=" * 90)
        print(f"{'ID':<5} {'Username':<15} {'Name':<25} {'Role':<15} {'Registered':<20}")
        print("-" * 90)
        
        for user_id, username, first_name, last_name, role, reg_date in users:
            try:
                decrypted_username = decrypt_data(username)
                decrypted_first = decrypt_data(first_name)
                decrypted_last = decrypt_data(last_name)
                full_name = f"{decrypted_first} {decrypted_last}"
            except:
                decrypted_username = username
                full_name = f"{first_name} {last_name}"
            
            print(f"{user_id:<5} {decrypted_username:<15} {full_name:<25} {role:<15} {reg_date:<20}")
        
        close_connection(conn)
        
    except Exception as e:
        print(f"Error listing system administrators: {e}")

def list_service_engineers(current_user):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, username, first_name, last_name, role, registration_date
            FROM Users
            WHERE role = 'Service Engineer'
            ORDER BY registration_date DESC
        ''')
        
        users = cursor.fetchall()
        
        if not users:
            print("📋 No Service Engineers found in the system.")
            return
        
        print("\n" + "=" * 90)
        print("    SERVICE ENGINEERS LIST")
        print("=" * 90)
        print(f"{'ID':<5} {'Username':<15} {'Name':<25} {'Role':<15} {'Registered':<20}")
        print("-" * 90)
        
        for user_id, username, first_name, last_name, role, reg_date in users:
            try:
                decrypted_username = decrypt_data(username)
                decrypted_first = decrypt_data(first_name)
                decrypted_last = decrypt_data(last_name)
                full_name = f"{decrypted_first} {decrypted_last}"
            except:
                decrypted_username = username
                full_name = f"{first_name} {last_name}"
            
            print(f"{user_id:<5} {decrypted_username:<15} {full_name:<25} {role:<15} {reg_date:<20}")
        
        close_connection(conn)
        
    except Exception as e:
        print(f"Error listing service engineers: {e}")

def delete_user_by_id(user_id, current_user, allowed_role=None):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # First get user info for security checks
        cursor.execute('SELECT username, role FROM Users WHERE id = ?', (user_id,))
        user_info = cursor.fetchone()
        
        if not user_info:
            print(f"No user found with ID {user_id}")
            return False
        
        username, role = user_info
        
        # SECURITY CHECKS
        
        # 1. Never allow deletion of super_admin
        if username == 'super_admin':
            print(f"No user found with ID {user_id}")
            log_action(current_user, f"Attempted to delete super_admin - BLOCKED")
            return False
        
        # 2. Check if current user can delete this role
        if allowed_role and role != allowed_role:
            # Decrypt username for logging purposes only
            try:
                decrypted_username = decrypt_data(username)
            except:
                decrypted_username = username
            
            print(f"No user found with ID {user_id}")
            log_action(current_user, f"Attempted to delete {role} user {decrypted_username} - BLOCKED (wrong role)")
            return False
        
        # 3. Additional security: Prevent deletion of other System Admins by System Admins
        # But allow System Admins to delete their own account
        if current_user != 'super_admin' and role == 'System Admin':
            # Check if this is the current user trying to delete their own account
            current_user_id = get_current_user_id(current_user)
            if user_id != current_user_id:
                # Decrypt username for logging purposes only
                try:
                    decrypted_username = decrypt_data(username)
                except:
                    decrypted_username = username
                
                print(f"No user found with ID {user_id}")
                log_action(current_user, f"Attempted to delete System Admin {decrypted_username} - BLOCKED (insufficient privileges)")
                return False
        
        # Delete the user
        cursor.execute('DELETE FROM Users WHERE id = ?', (user_id,))
        
        if cursor.rowcount > 0:
            # Decrypt username for success message and logging
            try:
                decrypted_username = decrypt_data(username)
            except:
                decrypted_username = username
            
            conn.commit()
            log_action(current_user, f"Deleted {role} user: {decrypted_username}")
            print(f"User {decrypted_username} ({role}) deleted successfully!")
            return True
        else:
            print(f"Failed to delete user with ID {user_id}")
            return False
            
    except Exception as e:
        print(f"Error deleting user: {e}")
        return False
    finally:
        close_connection(conn)

def validate_user_exists_with_role(user_id, required_role):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Check if user exists with the specific role
        cursor.execute('SELECT username, role FROM Users WHERE id = ? AND role = ?', (user_id, required_role))
        user_info = cursor.fetchone()
        
        if not user_info:
            # Check if user exists at all
            cursor.execute('SELECT username, role FROM Users WHERE id = ?', (user_id,))
            user_exists = cursor.fetchone()
            
            if not user_exists:
                print(f"No user found with ID {user_id}")
                return False, None, None
            else:
                # User exists but wrong role - generic message
                print(f"No user found with ID {user_id}")
                return False, None, None
        
        username, role = user_info
        return True, username, role
        
    except Exception as e:
        print(f"Error validating user: {e}")
        return False, None, None
    finally:
        close_connection(conn)

def update_user_by_id(user_id, update_data, current_user, role):
    from database import get_connection, close_connection
    from encryption import encrypt_data, decrypt_data
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, username, role FROM Users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        
        if not user:
            print(f"No user found with ID {user_id}")
            return False
        
        if user[2] != role:
            print(f"No user found with ID {user_id}")
            return False
        
        if 'username' in update_data:
            new_username = update_data['username']
            
            # Get all users and check for username conflicts by decrypting them
            cursor.execute('SELECT id, username FROM Users WHERE id != ?', (user_id,))
            all_users = cursor.fetchall()
            
            for existing_id, existing_username in all_users:
                try:
                    # Try to decrypt the username
                    decrypted_username = decrypt_data(existing_username)
                    if decrypted_username.lower() == new_username.lower():
                        print(f"ERROR: Username '{new_username}' is already taken.")
                        return False
                except:
                    # If decryption fails, check if it's a non-encrypted username (like super_admin)
                    if existing_username.lower() == new_username.lower():
                        print(f"ERROR: Username '{new_username}' is already taken.")
                        return False
        
        set_clauses = []
        values = []
        
        for field, value in update_data.items():
            if field == 'username':
                set_clauses.append('username = ?')
                values.append(encrypt_data(value))
            elif field == 'first_name':
                set_clauses.append('first_name = ?')
                values.append(encrypt_data(value))
            elif field == 'last_name':
                set_clauses.append('last_name = ?')
                values.append(encrypt_data(value))
        
        if not set_clauses:
            print("ERROR: No valid fields to update.")
            return False
        
        values.append(user_id)
        query = f'UPDATE Users SET {", ".join(set_clauses)} WHERE id = ?'
        
        cursor.execute(query, values)
        conn.commit()
        
        from system_logging import log_action
        log_action(current_user, f"Updated {role} with ID {user_id}")
        
        print(f"✅ {role} updated successfully!")
        return True
        
    except Exception as e:
        print(f"ERROR updating user: {e}")
        return False
    finally:
        close_connection(conn)

def generate_temporary_password():
    """Generate a secure temporary password"""
    import random
    import string
    
    # Generate a 12-character password with mixed case, numbers, and special chars
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special_chars = "!@#$%&*"
    
    # Ensure at least one character from each category
    password = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(digits),
        random.choice(special_chars)
    ]
    
    # Fill the rest randomly
    all_chars = lowercase + uppercase + digits + special_chars
    for _ in range(8):  # 12 total - 4 already added = 8 more
        password.append(random.choice(all_chars))
    
    # Shuffle the password
    random.shuffle(password)
    return ''.join(password)

def reset_user_password(user_id, current_user):
    """Reset a user's password to a temporary password"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Get user info
        cursor.execute('SELECT username, role FROM Users WHERE id = ?', (user_id,))
        user_info = cursor.fetchone()
        
        if not user_info:
            print(f"No user found with ID {user_id}")
            return False
        
        username, role = user_info
        
        # Generate temporary password
        temp_password = generate_temporary_password()
        
        # Hash the temporary password
        from authentication import hash_password
        hashed_temp_password = hash_password(temp_password)
        
        # Update password and set temp_password flag
        cursor.execute('''
            UPDATE Users 
            SET password_hash = ?, temp_password = 1
            WHERE id = ?
        ''', (hashed_temp_password, user_id))
        
        if cursor.rowcount > 0:
            conn.commit()
            
            # Decrypt username for logging
            try:
                decrypted_username = decrypt_data(username)
            except:
                decrypted_username = username
            
            log_action(current_user, f"Reset password for {role}: {decrypted_username}")
            
            print(f"✅ Password reset successfully for {decrypted_username} ({role})")
            print(f"🔑 Temporary password: {temp_password}")
            print(f"⚠️  User must change password on next login!")
            return True
        else:
            print(f"ERROR: Failed to reset password for user ID {user_id}")
            return False
            
    except Exception as e:
        print(f"ERROR resetting password: {e}")
        return False
    finally:
        close_connection(conn)

def update_user_password(username, new_password_hash, current_user):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Find the user by decrypting all usernames
        cursor.execute('SELECT id, username FROM Users')
        all_users = cursor.fetchall()
        
        user_id = None
        for existing_id, existing_username in all_users:
            try:
                # Try to decrypt the username
                decrypted_username = decrypt_data(existing_username)
                if decrypted_username.lower() == username.lower():
                    user_id = existing_id
                    break
            except:
                # If decryption fails, check if it's a non-encrypted username (like super_admin)
                if existing_username.lower() == username.lower():
                    user_id = existing_id
                    break
        
        if not user_id:
            print(f"User not found.")
            return False
        
        # Update password using user ID
        cursor.execute('''
            UPDATE Users 
            SET password_hash = ?, temp_password = 0
            WHERE id = ?
        ''', (new_password_hash, user_id))
        
        if cursor.rowcount > 0:
            conn.commit()
            close_connection(conn)
            log_action(current_user, f"Updated password for user: {username}")
            return True
        else:
            close_connection(conn)
            return False
            
    except Exception as e:
        print(f"Error updating password: {e}")
        return False

def check_temp_password(username):
    """Check if user has a temporary password"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Find the user by decrypting all usernames
        cursor.execute('SELECT id, username, temp_password FROM Users')
        all_users = cursor.fetchall()
        
        for existing_id, existing_username, temp_password in all_users:
            try:
                # Try to decrypt the username
                decrypted_username = decrypt_data(existing_username)
                if decrypted_username.lower() == username.lower():
                    close_connection(conn)
                    return bool(temp_password)
            except:
                # If decryption fails, check if it's a non-encrypted username (like super_admin)
                if existing_username.lower() == username.lower():
                    close_connection(conn)
                    return bool(temp_password)
        
        close_connection(conn)
        return False
        
    except Exception as e:
        print(f"Error checking temp password: {e}")
        return False

def delete_user(username, current_user):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM Users WHERE username = ?', (username,))
        
        if cursor.rowcount > 0:
            conn.commit()
            close_connection(conn)
            log_action(current_user, f"Deleted user: {username}")
            return True
        else:
            close_connection(conn)
            return False
            
    except Exception as e:
        print(f"Error deleting user: {e}")
        return False


def create_traveller(traveller_data):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        encrypted_first_name = encrypt_data(traveller_data['first_name'])
        encrypted_last_name = encrypt_data(traveller_data['last_name'])
        encrypted_email = encrypt_data(traveller_data['email'])
        encrypted_phone = encrypt_data(traveller_data['mobile_phone'])
        encrypted_street = encrypt_data(traveller_data['street_name'])
        encrypted_house = encrypt_data(traveller_data['house_number'])
        encrypted_zip = encrypt_data(traveller_data['zip_code'])
        encrypted_city = encrypt_data(traveller_data['city'])
        encrypted_license = encrypt_data(traveller_data['driving_license'])

        cursor.execute('''
            INSERT INTO Travellers (
                first_name, last_name, birthday, gender, street_name, house_number,
                zip_code, city, email, mobile_phone, driving_license, registration_date
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
        ''', (
            encrypted_first_name,
            encrypted_last_name,
            traveller_data['birthday'],
            traveller_data['gender'],
            encrypted_street,
            encrypted_house,
            encrypted_zip,
            encrypted_city,
            encrypted_email,
            encrypted_phone,
            encrypted_license
        ))
        
        conn.commit()
        close_connection(conn)
        return True
        
    except Exception as e:
        print(f"Error creating traveller: {e}")
        return False
    


def list_travellers():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, first_name, last_name, email, mobile_phone, street_name, house_number, 
                   zip_code, city, driving_license, registration_date
            FROM Travellers
            ORDER BY registration_date DESC
        ''')
        
        travellers = cursor.fetchall()
        
        if not travellers:
            print("📋 No travellers found in the system.")
            return
        
        print("\n" + "=" * 120)
        print("    TRAVELLER LIST")
        print("=" * 120)
        print(f"{'ID':<5} {'Name':<25} {'Email':<25} {'Phone':<15} {'Address':<30} {'License':<15} {'Registered':<20}")
        print("-" * 120)
        
        for traveller_id, first_name, last_name, email, phone, street, house, zip_code, city, license, reg_date in travellers:
            try:
                decrypted_first = decrypt_data(first_name)
                decrypted_last = decrypt_data(last_name)
                decrypted_email = decrypt_data(email)
                decrypted_phone = decrypt_data(phone)
                decrypted_street = decrypt_data(street)
                decrypted_house = decrypt_data(house)
                decrypted_zip = decrypt_data(zip_code)
                decrypted_city = decrypt_data(city)
                decrypted_license = decrypt_data(license)
                
                full_name = f"{decrypted_first} {decrypted_last}"
                address = f"{decrypted_street} {decrypted_house}, {decrypted_zip} {decrypted_city}"
            except:
                full_name = f"{first_name} {last_name}"
                decrypted_email = email
                decrypted_phone = phone
                address = f"{street} {house}, {zip_code} {city}"
                decrypted_license = license
            
            print(f"{traveller_id:<5} {full_name:<25} {decrypted_email:<25} {decrypted_phone:<15} {address:<30} {decrypted_license:<15} {reg_date:<20}")
        
        close_connection(conn)
        
    except Exception as e:
        print(f"Error listing travellers: {e}")

def search_traveller_by_id(traveller_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT id FROM Travellers WHERE id = ?', (traveller_id,))
        traveller = cursor.fetchone()
        close_connection(conn)
        return traveller
        
    except Exception as e:
        print(f"Error searching traveller: {e}")
        return None
    
def search_travellers(search_term):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, first_name, last_name, email, mobile_phone, street_name, house_number,
                   zip_code, city, driving_license, registration_date
            FROM Travellers
        ''')
        
        all_travellers = cursor.fetchall()
        matching_travellers = []
        
        print(f"Searching for: '{search_term}'")
        print(f"Checking {len(all_travellers)} travellers...")
        
        for traveller_id, first_name, last_name, email, phone, street, house, zip_code, city, license, reg_date in all_travellers:
            match_found = False
            
            if search_term.lower() in str(traveller_id).lower():
                match_found = True
            
            try:
                decrypted_first = decrypt_data(first_name)
                decrypted_last = decrypt_data(last_name)
                decrypted_email = decrypt_data(email)
                decrypted_phone = decrypt_data(phone)
                decrypted_street = decrypt_data(street)
                decrypted_house = decrypt_data(house)
                decrypted_zip = decrypt_data(zip_code)
                decrypted_city = decrypt_data(city)
                decrypted_license = decrypt_data(license)

                search_lower = search_term.lower()
            
                if (decrypted_first and 
                    decrypted_first != first_name and 
                    len(decrypted_first) < 50 and  
                    search_lower in decrypted_first.lower()):
                    match_found = True
                    print(f"Found match in first name: {decrypted_first}")
                
                if (decrypted_last and 
                    decrypted_last != last_name and 
                    len(decrypted_last) < 50 and  
                    search_lower in decrypted_last.lower()):
                    match_found = True
                    print(f"Found match in last name: {decrypted_last}")
                
                if (decrypted_email and 
                    decrypted_email != email and 
                    len(decrypted_email) < 100 and 
                    search_lower in decrypted_email.lower()):
                    match_found = True
                    print(f"Found match in email: {decrypted_email}")
                
                if (decrypted_phone and 
                    decrypted_phone != phone and 
                    len(decrypted_phone) < 20 and
                    search_lower in decrypted_phone.lower()):
                    match_found = True
                    print(f"Found match in phone: {decrypted_phone}")
                
                if (decrypted_street and 
                    decrypted_street != street and 
                    len(decrypted_street) < 50 and
                    search_lower in decrypted_street.lower()):
                    match_found = True
                    print(f"Found match in street: {decrypted_street}")
                
                if (decrypted_city and 
                    decrypted_city != city and 
                    len(decrypted_city) < 50 and
                    search_lower in decrypted_city.lower()):
                    match_found = True
                    print(f"Found match in city: {decrypted_city}")
                
                if (decrypted_license and 
                    decrypted_license != license and 
                    len(decrypted_license) < 20 and
                    search_lower in decrypted_license.lower()):
                    match_found = True
                    print(f"Found match in license: {decrypted_license}")
                        
            except Exception as e:
                print(f"Decryption error for traveller {traveller_id}: {e}")
                continue
  
            if match_found:
                try:
                    display_first = decrypt_data(first_name) if decrypt_data(first_name) else "Encrypted"
                    display_last = decrypt_data(last_name) if decrypt_data(last_name) else "Encrypted"
                    display_email = decrypt_data(email) if decrypt_data(email) else "Encrypted"
                    display_phone = decrypt_data(phone) if decrypt_data(phone) else "Encrypted"
                except:
                    display_first = "Encrypted"
                    display_last = "Encrypted"
                    display_email = "Encrypted"
                    display_phone = "Encrypted"
                
                matching_travellers.append((
                    traveller_id, display_first, display_last, 
                    display_email, display_phone, reg_date
                ))

        if matching_travellers:
            print(f"Found {len(matching_travellers)} matching traveller(s)\n")
            print("=" * 100)
            print(f"    SEARCH RESULTS FOR '{search_term}'")
            print("=" * 100)
            print(f"{'ID':<5} {'Name':<25} {'Email':<30} {'Phone':<15} {'Registered':<20}")
            print("-" * 100)
            
            for traveller_id, first_name, last_name, email, phone, reg_date in matching_travellers:
                full_name = f"{first_name} {last_name}"
                print(f"{traveller_id:<5} {full_name:<25} {email:<30} {phone:<15} {reg_date:<20}")
        else:
            print(f"No travellers found matching '{search_term}'")
            print("\n Try searching with:")
            print("   - Traveller ID (partial or full)")
            print("   - First or last name")
            print("   - Email address")
            print("   - Phone number")
            print("   - Street name or city")
            print("   - Driving license number")
        
        close_connection(conn)
        
    except Exception as e:
        print(f"Error searching travellers: {e}")

def update_traveller(traveller_id, update_data):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # First validate that traveller exists
        cursor.execute('SELECT id FROM Travellers WHERE id = ?', (traveller_id,))
        traveller_exists = cursor.fetchone()
        
        if not traveller_exists:
            print(f"No traveller found with ID {traveller_id}")
            return False

        encrypted_fields = ['first_name', 'last_name', 'email', 'mobile_phone', 
                           'street_name', 'house_number', 'zip_code', 'city', 'driving_license']
        
        for field in encrypted_fields:
            if field in update_data:
                update_data[field] = encrypt_data(update_data[field])

        set_clauses = []
        values = []
        
        for field, value in update_data.items():
            set_clauses.append(f"{field} = ?")
            values.append(value)
        
        values.append(traveller_id)
        
        query = f"UPDATE Travellers SET {', '.join(set_clauses)} WHERE id = ?"
        cursor.execute(query, values)
        
        if cursor.rowcount > 0:
            conn.commit()
            close_connection(conn)
            return True
        else:
            close_connection(conn)
            return False
            
    except Exception as e:
        print(f"Error updating traveller: {e}")
        return False

def delete_traveller(traveller_id):
    conn = None
    try:
        conn = get_connection()
        if not conn:
            print("Failed to connect to database")
            return False
            
        cursor = conn.cursor()
        
        cursor.execute('SELECT id FROM Travellers WHERE id = ?', (traveller_id,))
        if not cursor.fetchone():
            print(f"Traveller with ID '{traveller_id}' not found")
            return False
        
        cursor.execute('DELETE FROM Travellers WHERE id = ?', (traveller_id,))
        
        if cursor.rowcount > 0:
            conn.commit()
            print(f"Traveller with ID '{traveller_id}' deleted successfully")
            return True
        else:
            print(f"No traveller found with ID '{traveller_id}'")
            return False
            
    except sqlite3.OperationalError as e:
        if "database is locked" in str(e):
            print("Database is locked. Attempting to unlock...")
            from database import unlock_database
            if unlock_database():
                print("Database unlocked. Please try again.")
            else:
                print("Could not unlock database. Please restart the application.")
        else:
            print(f"Database error: {e}")
        return False
    except Exception as e:
        print(f"Error deleting traveller: {e}")
        return False
    finally:
        if conn:
            close_connection(conn)

def create_scooter(scooter_data):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        encrypted_brand = encrypt_data(scooter_data['brand'])
        encrypted_model = encrypt_data(scooter_data['model'])
        encrypted_serial = encrypt_data(scooter_data['serial_number'])
        encrypted_latitude = encrypt_data(str(scooter_data['latitude']))
        encrypted_longitude = encrypt_data(str(scooter_data['longitude']))
        
        cursor.execute('''
            INSERT INTO Scooters (
                brand, model, serial_number, top_speed, battery_capacity, state_of_charge,
                target_range_min, target_range_max, latitude, longitude, out_of_service,
                mileage, last_maintenance_date, in_service_date
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
        ''', (
            encrypted_brand,
            encrypted_model,
            encrypted_serial,
            scooter_data['top_speed'],
            scooter_data['battery_capacity'],
            scooter_data['state_of_charge'],
            scooter_data['target_range_min'],
            scooter_data['target_range_max'],
            encrypted_latitude,
            encrypted_longitude,
            scooter_data['out_of_service'],
            scooter_data['mileage'],
            scooter_data['last_maintenance_date']
        ))
        
        conn.commit()
        close_connection(conn)
        return True
        
    except Exception as e:
        print(f"Error creating scooter: {e}")
        return False

def list_scooters():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, brand, model, serial_number, state_of_charge, out_of_service, 
                   latitude, longitude, in_service_date
            FROM Scooters
            ORDER BY in_service_date DESC
        ''')
        
        scooters = cursor.fetchall()
        
        if not scooters:
            print("No scooters found in the system.")
            return
        
        print("\n" + "=" * 120)
        print("    SCOOTER LIST")
        print("=" * 120)
        print(f"{'ID':<5} {'Brand':<15} {'Model':<20} {'Serial':<15} {'SoC':<5} {'Location':<20} {'Status':<12} {'In Service':<20}")
        print("-" * 120)
        
        for scooter_id, brand, model, serial, soc, out_of_service, lat, lon, in_service in scooters:
           
            try:
                decrypted_brand = decrypt_data(brand)
                decrypted_model = decrypt_data(model)
                decrypted_serial = decrypt_data(serial)
                decrypted_lat = decrypt_data(lat)
                decrypted_lon = decrypt_data(lon)
             
                display_brand = decrypted_brand if decrypted_brand else "Encrypted"
                display_model = decrypted_model if decrypted_model else "Encrypted"
                display_serial = decrypted_serial if decrypted_serial else "Encrypted"
                location = f"{decrypted_lat}, {decrypted_lon}" if decrypted_lat and decrypted_lon else "Encrypted"
            except:
                display_brand = "Encrypted"
                display_model = "Encrypted"
                display_serial = "Encrypted"
                location = "Encrypted"
            
            status = "Out of Service" if out_of_service else "Active"
            print(f"{scooter_id:<5} {display_brand:<15} {display_model:<20} {display_serial:<15} {soc}%{'':<4} {location:<20} {status:<12} {in_service:<20}")
        
        close_connection(conn)
        
    except Exception as e:
        print(f"Error listing scooters: {e}")

def search_scooters(search_term):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, brand, model, serial_number, state_of_charge, out_of_service, 
                   latitude, longitude, in_service_date
            FROM Scooters
        ''')
        
        all_scooters = cursor.fetchall()
        matching_scooters = []
        
        print(f"Searching for: '{search_term}'")
        print(f"Checking {len(all_scooters)} scooters...")
        
        search_lower = search_term.lower()
        for scooter_id, brand, model, serial, soc, out_of_service, lat, lon, in_service in all_scooters:
            match_found = False
            
            if search_lower in str(scooter_id).lower():
                match_found = True
            try:
                decrypted_brand = decrypt_data(brand)
                decrypted_model = decrypt_data(model)
                decrypted_serial = decrypt_data(serial)
                decrypted_lat = decrypt_data(lat)
                decrypted_lon = decrypt_data(lon)
             
                if (decrypted_brand and 
                    decrypted_brand != brand and 
                    len(decrypted_brand) < 50 and  
                    search_lower in decrypted_brand.lower()):
                    match_found = True
                    print(f"Found match in brand: {decrypted_brand}")
                
                if (decrypted_model and 
                    decrypted_model != model and 
                    len(decrypted_model) < 50 and 
                    search_lower in decrypted_model.lower()):
                    match_found = True
                    print(f"Found match in model: {decrypted_model}")
                
                if (decrypted_serial and 
                    decrypted_serial != serial and 
                    len(decrypted_serial) < 30 and  
                    search_lower in decrypted_serial.lower()):
                    match_found = True
                    print(f"Found match in serial: {decrypted_serial}")
                
                if (decrypted_lat and 
                    decrypted_lat != lat and 
                    len(decrypted_lat) < 20 and
                    search_lower in decrypted_lat.lower()):
                    match_found = True
                    print(f"Found match in latitude: {decrypted_lat}")
                
                if (decrypted_lon and 
                    decrypted_lon != lon and 
                    len(decrypted_lon) < 20 and
                    search_lower in decrypted_lon.lower()):
                    match_found = True
                    print(f"Found match in longitude: {decrypted_lon}")
                        
            except Exception as e:
                print(f"Decryption error for scooter {scooter_id}: {e}")
                continue
            
            if match_found:
                try:
                    display_brand = decrypt_data(brand) if decrypt_data(brand) else "Encrypted"
                    display_model = decrypt_data(model) if decrypt_data(model) else "Encrypted"
                    display_serial = decrypt_data(serial) if decrypt_data(serial) else "Encrypted"
                    display_lat = decrypt_data(lat) if decrypt_data(lat) else "Encrypted"
                    display_lon = decrypt_data(lon) if decrypt_data(lon) else "Encrypted"
                except:
                    display_brand = "Encrypted"
                    display_model = "Encrypted"
                    display_serial = "Encrypted"
                    display_lat = "Encrypted"
                    display_lon = "Encrypted"
                
                matching_scooters.append((
                    scooter_id, display_brand, display_model, display_serial, soc, out_of_service, 
                    display_lat, display_lon, in_service
                ))
        
        if matching_scooters:
            print(f"Found {len(matching_scooters)} matching scooter(s)\n")
            print("=" * 120)
            print(f"    SEARCH RESULTS FOR '{search_term}'")
            print("=" * 120)
            print(f"{'ID':<5} {'Brand':<15} {'Model':<20} {'Serial':<15} {'SoC':<5} {'Location':<20} {'Status':<12} {'In Service':<20}")
            print("-" * 120)
            
            for scooter_id, brand, model, serial, soc, out_of_service, lat, lon, in_service in matching_scooters:
                status = "Out of Service" if out_of_service else "Active"
                location = f"{lat}, {lon}" if lat != "Encrypted" and lon != "Encrypted" else "Encrypted"
                print(f"{scooter_id:<5} {brand:<15} {model:<20} {serial:<15} {soc}%{'':<4} {location:<20} {status:<12} {in_service:<20}")
        else:
            print(f"No scooters found matching '{search_term}'")
            print("\n Try searching with:")
            print("   - Brand name (e.g., 'Segway', 'NIU')")
            print("   - Model name (e.g., 'Ninebot', 'N1S')")
            print("   - Serial number (partial or full)")
            print("   - Latitude or longitude coordinates")
            print("   - Partial matches work (e.g., 'seg' finds 'Segway')")
        
        close_connection(conn)
        
    except Exception as e:
        print(f"Error searching scooters: {e}")

def update_scooter(scooter_id, update_data):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # First validate that scooter exists
        cursor.execute('SELECT id FROM Scooters WHERE id = ?', (scooter_id,))
        scooter_exists = cursor.fetchone()
        
        if not scooter_exists:
            print(f"No scooter found with ID {scooter_id}")
            return False
        set_clauses = []
        values = []
        encrypted_fields = ['brand', 'model', 'serial_number', 'latitude', 'longitude']
        
        for field, value in update_data.items():
            if field in encrypted_fields:
                encrypted_value = encrypt_data(str(value))
                set_clauses.append(f"{field} = ?")
                values.append(encrypted_value)
            else:
                set_clauses.append(f"{field} = ?")
                values.append(value)
        
        values.append(scooter_id)
        
        query = f"UPDATE Scooters SET {', '.join(set_clauses)} WHERE id = ?"
        cursor.execute(query, values)
        
        if cursor.rowcount > 0:
            conn.commit()
            close_connection(conn)
            return True
        else:
            close_connection(conn)
            return False
            
    except Exception as e:
        print(f"Error updating scooter: {e}")
        return False

def delete_scooter(scooter_id):
    conn = None
    try:
        conn = get_connection()
        if not conn:
            print("Failed to connect to database")
            return False
            
        cursor = conn.cursor()
        
        cursor.execute('SELECT id FROM Scooters WHERE id = ?', (scooter_id,))
        if not cursor.fetchone():
            print(f"Scooter with ID '{scooter_id}' not found")
            return False

        cursor.execute('DELETE FROM Scooters WHERE id = ?', (scooter_id,))
        
        if cursor.rowcount > 0:
            conn.commit()
            print(f"Scooter with ID '{scooter_id}' deleted successfully")
            return True
        else:
            print(f"No scooter found with ID '{scooter_id}'")
            return False
            
    except sqlite3.OperationalError as e:
        if "database is locked" in str(e):
            print("Database is locked. Attempting to unlock...")
            from database import unlock_database
            if unlock_database():
                print("Database unlocked. Please try again.")
            else:
                print("Could not unlock database. Please restart the application.")
        else:
            print(f"Database error: {e}")
        return False
    except Exception as e:
        print(f"Error deleting scooter: {e}")
        return False
    finally:
        if conn:
            close_connection(conn)