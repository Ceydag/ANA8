"""
CRUD operations for Urban Mobility Backend System
Handles Create, Read, Update, Delete operations for Users, Travellers, and Scooters
"""

import sqlite3
from database import get_connection, close_connection
from encryption import encrypt_data, decrypt_data
from system_logging import log_action
import re

# ============================================================================
# USER MANAGEMENT FUNCTIONS
# ============================================================================

def create_user(user_data, current_user):
    """Create a new user with encrypted sensitive data"""
    conn = None
    try:
        conn = get_connection()
        if not conn:
            print("❌ Failed to connect to database")
            return False
            
        cursor = conn.cursor()
        
        # Encrypt sensitive data
        encrypted_first_name = encrypt_data(user_data['first_name'])
        encrypted_last_name = encrypt_data(user_data['last_name'])
        
        # Insert user (username stored as plain text, names encrypted)
        cursor.execute('''
            INSERT INTO Users (username, password_hash, first_name, last_name, role, registration_date)
            VALUES (?, ?, ?, ?, ?, datetime('now'))
        ''', (
            user_data['username'],
            user_data['password_hash'],
            encrypted_first_name,
            encrypted_last_name,
            user_data['role']
        ))
        
        conn.commit()
        
        # Log the activity
        log_action(current_user, f"Created new {user_data['role']} user: {user_data['username']}")
        
        return True
        
    except sqlite3.OperationalError as e:
        if "database is locked" in str(e):
            print("❌ Database is locked. Attempting to unlock...")
            from database import unlock_database
            if unlock_database():
                print("✅ Database unlocked. Please try again.")
            else:
                print("❌ Could not unlock database. Please restart the application.")
        else:
            print(f"❌ Database error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error creating user: {e}")
        return False
    finally:
        if conn:
            close_connection(conn)

def list_users(current_user):
    """List all users with decrypted names"""
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
                # Decrypt names for display
                decrypted_first = decrypt_data(first_name)
                decrypted_last = decrypt_data(last_name)
                full_name = f"{decrypted_first} {decrypted_last}"
            except:
                # If decryption fails, show raw data
                full_name = f"{first_name} {last_name}"
            
            print(f"{username:<15} {full_name:<25} {role:<15} {reg_date:<20}")
        
        close_connection(conn)
        
    except Exception as e:
        print(f"❌ Error listing users: {e}")

def update_user_password(username, new_password_hash, current_user):
    """Update user password"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE Users 
            SET password_hash = ?
            WHERE username = ?
        ''', (new_password_hash, username))
        
        if cursor.rowcount > 0:
            conn.commit()
            close_connection(conn)
            log_action(current_user, f"Updated password for user: {username}")
            return True
        else:
            close_connection(conn)
            return False
            
    except Exception as e:
        print(f"❌ Error updating password: {e}")
        return False

def delete_user(username, current_user):
    """Delete a user"""
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
        print(f"❌ Error deleting user: {e}")
        return False

# ============================================================================
# TRAVELLER MANAGEMENT FUNCTIONS
# ============================================================================

def create_traveller(traveller_data):
    """Create a new traveller with encrypted sensitive data"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Generate unique customer ID
        import uuid
        customer_id = str(uuid.uuid4())[:8] + '-' + str(uuid.uuid4())[:1]
        
        # Encrypt sensitive data
        encrypted_first_name = encrypt_data(traveller_data['first_name'])
        encrypted_last_name = encrypt_data(traveller_data['last_name'])
        encrypted_email = encrypt_data(traveller_data['email'])
        encrypted_phone = encrypt_data(traveller_data['mobile_phone'])
        
        # Insert traveller
        cursor.execute('''
            INSERT INTO Travellers (
                customer_id, first_name, last_name, birthday, gender, street_name, house_number,
                zip_code, city, email, mobile_phone, driving_license, registration_date
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
        ''', (
            customer_id,
            encrypted_first_name,
            encrypted_last_name,
            traveller_data['birthday'],
            traveller_data['gender'],
            traveller_data['street_name'],
            traveller_data['house_number'],
            traveller_data['zip_code'],
            traveller_data['city'],
            encrypted_email,
            encrypted_phone,
            traveller_data['driving_license']
        ))
        
        conn.commit()
        close_connection(conn)
        return True
        
    except Exception as e:
        print(f"❌ Error creating traveller: {e}")
        return False

def list_travellers():
    """List all travellers with decrypted data"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT customer_id, first_name, last_name, email, mobile_phone, registration_date
            FROM Travellers
            ORDER BY registration_date DESC
        ''')
        
        travellers = cursor.fetchall()
        
        if not travellers:
            print("📋 No travellers found in the system.")
            return
        
        print("\n" + "=" * 100)
        print("    TRAVELLER LIST")
        print("=" * 100)
        print(f"{'Customer ID':<15} {'Name':<25} {'Email':<30} {'Phone':<15} {'Registered':<20}")
        print("-" * 100)
        
        for customer_id, first_name, last_name, email, phone, reg_date in travellers:
            try:
                # Decrypt sensitive data for display
                decrypted_first = decrypt_data(first_name)
                decrypted_last = decrypt_data(last_name)
                decrypted_email = decrypt_data(email)
                decrypted_phone = decrypt_data(phone)
                
                full_name = f"{decrypted_first} {decrypted_last}"
            except:
                # If decryption fails, show raw data
                full_name = f"{first_name} {last_name}"
                decrypted_email = email
                decrypted_phone = phone
            
            print(f"{customer_id:<15} {full_name:<25} {decrypted_email:<30} {decrypted_phone:<15} {reg_date:<20}")
        
        close_connection(conn)
        
    except Exception as e:
        print(f"❌ Error listing travellers: {e}")

def search_travellers(search_term):
    """Search travellers with decryption-first approach for partial matching"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Get all travellers
        cursor.execute('''
            SELECT customer_id, first_name, last_name, email, mobile_phone, registration_date
            FROM Travellers
        ''')
        
        all_travellers = cursor.fetchall()
        matching_travellers = []
        
        print(f"🔍 Searching for: '{search_term}'")
        print(f"📋 Checking {len(all_travellers)} travellers...")
        
        # Search in all travellers with decryption-first approach
        for customer_id, first_name, last_name, email, phone, reg_date in all_travellers:
            match_found = False
            
            # 1. Search in customer_id (not encrypted, supports partial matching)
            if search_term.lower() in str(customer_id).lower():
                match_found = True
            
            # 2. Decrypt sensitive data and search
            try:
                # Decrypt all sensitive fields
                decrypted_first = decrypt_data(first_name)
                decrypted_last = decrypt_data(last_name)
                decrypted_email = decrypt_data(email)
                decrypted_phone = decrypt_data(phone)
                
                # Check if decryption was successful (data should be different from encrypted)
                # and should be reasonable length (not 136+ character encrypted strings)
                search_lower = search_term.lower()
                
                # Search in first name
                if (decrypted_first and 
                    decrypted_first != first_name and 
                    len(decrypted_first) < 50 and  # Reasonable name length
                    search_lower in decrypted_first.lower()):
                    match_found = True
                    print(f"   ✅ Found match in first name: {decrypted_first}")
                
                # Search in last name
                if (decrypted_last and 
                    decrypted_last != last_name and 
                    len(decrypted_last) < 50 and  # Reasonable name length
                    search_lower in decrypted_last.lower()):
                    match_found = True
                    print(f"   ✅ Found match in last name: {decrypted_last}")
                
                # Search in email
                if (decrypted_email and 
                    decrypted_email != email and 
                    len(decrypted_email) < 100 and  # Reasonable email length
                    search_lower in decrypted_email.lower()):
                    match_found = True
                    print(f"   ✅ Found match in email: {decrypted_email}")
                
                # Search in phone
                if (decrypted_phone and 
                    decrypted_phone != phone and 
                    len(decrypted_phone) < 20 and  # Reasonable phone length
                    search_lower in decrypted_phone.lower()):
                    match_found = True
                    print(f"   ✅ Found match in phone: {decrypted_phone}")
                        
            except Exception as e:
                print(f"   ⚠️ Decryption error for traveller {customer_id}: {e}")
                # If decryption fails completely, skip this traveller
                continue
            
            # If match found, add to results
            if match_found:
                # Use decrypted data for display
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
                    customer_id, display_first, display_last, 
                    display_email, display_phone, reg_date
                ))
        
        # Display results
        if matching_travellers:
            print(f"✅ Found {len(matching_travellers)} matching traveller(s)\n")
            print("=" * 100)
            print(f"    SEARCH RESULTS FOR '{search_term}'")
            print("=" * 100)
            print(f"{'Customer ID':<15} {'Name':<25} {'Email':<30} {'Phone':<15} {'Registered':<20}")
            print("-" * 100)
            
            for customer_id, first_name, last_name, email, phone, reg_date in matching_travellers:
                full_name = f"{first_name} {last_name}"
                print(f"{customer_id:<15} {full_name:<25} {email:<30} {phone:<15} {reg_date:<20}")
        else:
            print(f"❌ No travellers found matching '{search_term}'")
            print("\n💡 Try searching with:")
            print("   - Customer ID (partial or full)")
            print("   - First or last name")
            print("   - Email address")
            print("   - Phone number")
        
        close_connection(conn)
        
    except Exception as e:
        print(f"❌ Error searching travellers: {e}")

def update_traveller(customer_id, update_data):
    """Update traveller information"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Encrypt sensitive data if provided
        if 'first_name' in update_data:
            update_data['first_name'] = encrypt_data(update_data['first_name'])
        if 'last_name' in update_data:
            update_data['last_name'] = encrypt_data(update_data['last_name'])
        if 'email' in update_data:
            update_data['email'] = encrypt_data(update_data['email'])
        if 'mobile_phone' in update_data:
            update_data['mobile_phone'] = encrypt_data(update_data['mobile_phone'])
        
        # Build update query
        set_clauses = []
        values = []
        
        for field, value in update_data.items():
            set_clauses.append(f"{field} = ?")
            values.append(value)
        
        values.append(customer_id)
        
        query = f"UPDATE Travellers SET {', '.join(set_clauses)} WHERE customer_id = ?"
        cursor.execute(query, values)
        
        if cursor.rowcount > 0:
            conn.commit()
            close_connection(conn)
            return True
        else:
            close_connection(conn)
            return False
            
    except Exception as e:
        print(f"❌ Error updating traveller: {e}")
        return False

def delete_traveller(customer_id):
    """Delete a traveller with improved error handling"""
    conn = None
    try:
        conn = get_connection()
        if not conn:
            print("❌ Failed to connect to database")
            return False
            
        cursor = conn.cursor()
        
        # First check if traveller exists
        cursor.execute('SELECT customer_id FROM Travellers WHERE customer_id = ?', (customer_id,))
        if not cursor.fetchone():
            print(f"❌ Traveller with customer ID '{customer_id}' not found")
            return False
        
        # Delete the traveller
        cursor.execute('DELETE FROM Travellers WHERE customer_id = ?', (customer_id,))
        
        if cursor.rowcount > 0:
            conn.commit()
            print(f"✅ Traveller with customer ID '{customer_id}' deleted successfully")
            return True
        else:
            print(f"❌ No traveller found with customer ID '{customer_id}'")
            return False
            
    except sqlite3.OperationalError as e:
        if "database is locked" in str(e):
            print("❌ Database is locked. Attempting to unlock...")
            from database import unlock_database
            if unlock_database():
                print("✅ Database unlocked. Please try again.")
            else:
                print("❌ Could not unlock database. Please restart the application.")
        else:
            print(f"❌ Database error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error deleting traveller: {e}")
        return False
    finally:
        if conn:
            close_connection(conn)

# ============================================================================
# SCOOTER MANAGEMENT FUNCTIONS
# ============================================================================

def create_scooter(scooter_data):
    """Create a new scooter with encrypted sensitive data"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Encrypt sensitive scooter data
        encrypted_brand = encrypt_data(scooter_data['brand'])
        encrypted_model = encrypt_data(scooter_data['model'])
        encrypted_serial = encrypt_data(scooter_data['serial_number'])
        
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
            scooter_data['latitude'],
            scooter_data['longitude'],
            scooter_data['out_of_service'],
            scooter_data['mileage'],
            scooter_data['last_maintenance_date']
        ))
        
        conn.commit()
        close_connection(conn)
        return True
        
    except Exception as e:
        print(f"❌ Error creating scooter: {e}")
        return False

def list_scooters():
    """List all scooters with decrypted data"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, brand, model, serial_number, state_of_charge, out_of_service, in_service_date
            FROM Scooters
            ORDER BY in_service_date DESC
        ''')
        
        scooters = cursor.fetchall()
        
        if not scooters:
            print("📋 No scooters found in the system.")
            return
        
        print("\n" + "=" * 100)
        print("    SCOOTER LIST")
        print("=" * 100)
        print(f"{'ID':<5} {'Brand':<15} {'Model':<20} {'Serial':<15} {'SoC':<5} {'Status':<12} {'In Service':<20}")
        print("-" * 100)
        
        for scooter_id, brand, model, serial, soc, out_of_service, in_service in scooters:
            # Decrypt sensitive data
            try:
                decrypted_brand = decrypt_data(brand)
                decrypted_model = decrypt_data(model)
                decrypted_serial = decrypt_data(serial)
                
                # Use decrypted data if successful, otherwise show encrypted
                display_brand = decrypted_brand if decrypted_brand else "Encrypted"
                display_model = decrypted_model if decrypted_model else "Encrypted"
                display_serial = decrypted_serial if decrypted_serial else "Encrypted"
            except:
                display_brand = "Encrypted"
                display_model = "Encrypted"
                display_serial = "Encrypted"
            
            status = "🚫 Out of Service" if out_of_service else "✅ Active"
            print(f"{scooter_id:<5} {display_brand:<15} {display_model:<20} {display_serial:<15} {soc}%{'':<4} {status:<12} {in_service:<20}")
        
        close_connection(conn)
        
    except Exception as e:
        print(f"❌ Error listing scooters: {e}")

def search_scooters(search_term):
    """Search scooters with partial matching support"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Get all scooters for comprehensive search
        cursor.execute('''
            SELECT id, brand, model, serial_number, state_of_charge, out_of_service, in_service_date
            FROM Scooters
        ''')
        
        all_scooters = cursor.fetchall()
        matching_scooters = []
        
        print(f"🔍 Searching for: '{search_term}'")
        print(f"📋 Checking {len(all_scooters)} scooters...")
        
        # Search with decryption-first approach for encrypted data
        search_lower = search_term.lower()
        for scooter_id, brand, model, serial, soc, out_of_service, in_service in all_scooters:
            match_found = False
            
            # 1. Search in scooter_id (not encrypted)
            if search_lower in str(scooter_id).lower():
                match_found = True
            
            # 2. Decrypt and search in sensitive fields
            try:
                decrypted_brand = decrypt_data(brand)
                decrypted_model = decrypt_data(model)
                decrypted_serial = decrypt_data(serial)
                
                # Search in decrypted data (partial matching)
                if (decrypted_brand and 
                    decrypted_brand != brand and 
                    len(decrypted_brand) < 50 and  # Reasonable brand length
                    search_lower in decrypted_brand.lower()):
                    match_found = True
                    print(f"   ✅ Found match in brand: {decrypted_brand}")
                
                if (decrypted_model and 
                    decrypted_model != model and 
                    len(decrypted_model) < 50 and  # Reasonable model length
                    search_lower in decrypted_model.lower()):
                    match_found = True
                    print(f"   ✅ Found match in model: {decrypted_model}")
                
                if (decrypted_serial and 
                    decrypted_serial != serial and 
                    len(decrypted_serial) < 30 and  # Reasonable serial length
                    search_lower in decrypted_serial.lower()):
                    match_found = True
                    print(f"   ✅ Found match in serial: {decrypted_serial}")
                        
            except Exception as e:
                print(f"   ⚠️ Decryption error for scooter {scooter_id}: {e}")
                # If decryption fails completely, skip this scooter
                continue
            
            if match_found:
                # Use decrypted data for display
                try:
                    display_brand = decrypt_data(brand) if decrypt_data(brand) else "Encrypted"
                    display_model = decrypt_data(model) if decrypt_data(model) else "Encrypted"
                    display_serial = decrypt_data(serial) if decrypt_data(serial) else "Encrypted"
                except:
                    display_brand = "Encrypted"
                    display_model = "Encrypted"
                    display_serial = "Encrypted"
                
                matching_scooters.append((
                    scooter_id, display_brand, display_model, display_serial, soc, out_of_service, in_service
                ))
        
        # Display results
        if matching_scooters:
            print(f"✅ Found {len(matching_scooters)} matching scooter(s)\n")
            print("=" * 100)
            print(f"    SEARCH RESULTS FOR '{search_term}'")
            print("=" * 100)
            print(f"{'ID':<5} {'Brand':<15} {'Model':<20} {'Serial':<15} {'SoC':<5} {'Status':<12} {'In Service':<20}")
            print("-" * 100)
            
            for scooter_id, brand, model, serial, soc, out_of_service, in_service in matching_scooters:
                status = "🚫 Out of Service" if out_of_service else "✅ Active"
                print(f"{scooter_id:<5} {brand:<15} {model:<20} {serial:<15} {soc}%{'':<4} {status:<12} {in_service:<20}")
        else:
            print(f"❌ No scooters found matching '{search_term}'")
            print("\n💡 Try searching with:")
            print("   - Brand name (e.g., 'Segway', 'NIU')")
            print("   - Model name (e.g., 'Ninebot', 'N1S')")
            print("   - Serial number (partial or full)")
            print("   - Partial matches work (e.g., 'seg' finds 'Segway')")
        
        close_connection(conn)
        
    except Exception as e:
        print(f"❌ Error searching scooters: {e}")

def update_scooter(scooter_id, update_data):
    """Update scooter information with encryption for sensitive fields"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Build update query with encryption for sensitive fields
        set_clauses = []
        values = []
        
        # Fields that should be encrypted
        encrypted_fields = ['brand', 'model', 'serial_number']
        
        for field, value in update_data.items():
            if field in encrypted_fields:
                # Encrypt sensitive fields
                encrypted_value = encrypt_data(str(value))
                set_clauses.append(f"{field} = ?")
                values.append(encrypted_value)
            else:
                # Non-sensitive fields remain unencrypted
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
        print(f"❌ Error updating scooter: {e}")
        return False

def delete_scooter(scooter_id):
    """Delete a scooter with improved error handling"""
    conn = None
    try:
        conn = get_connection()
        if not conn:
            print("❌ Failed to connect to database")
            return False
            
        cursor = conn.cursor()
        
        # First check if scooter exists
        cursor.execute('SELECT id FROM Scooters WHERE id = ?', (scooter_id,))
        if not cursor.fetchone():
            print(f"❌ Scooter with ID '{scooter_id}' not found")
            return False
        
        # Delete the scooter
        cursor.execute('DELETE FROM Scooters WHERE id = ?', (scooter_id,))
        
        if cursor.rowcount > 0:
            conn.commit()
            print(f"✅ Scooter with ID '{scooter_id}' deleted successfully")
            return True
        else:
            print(f"❌ No scooter found with ID '{scooter_id}'")
            return False
            
    except sqlite3.OperationalError as e:
        if "database is locked" in str(e):
            print("❌ Database is locked. Attempting to unlock...")
            from database import unlock_database
            if unlock_database():
                print("✅ Database unlocked. Please try again.")
            else:
                print("❌ Could not unlock database. Please restart the application.")
        else:
            print(f"❌ Database error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error deleting scooter: {e}")
        return False
    finally:
        if conn:
            close_connection(conn)