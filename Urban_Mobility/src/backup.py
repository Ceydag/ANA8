import zipfile
import os
from datetime import datetime
import uuid
from database import get_connection, close_connection
from encryption import decrypt_data

def create_backup():
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"backup_{timestamp}.zip"
        
        with zipfile.ZipFile(backup_filename, 'w', zipfile.ZIP_DEFLATED) as backup_zip:
            
            if os.path.exists('urban_mobility.db'):
                backup_zip.write('urban_mobility.db')
           
            if os.path.exists('encrypted_logs.txt'):
                backup_zip.write('encrypted_logs.txt')
  
            if os.path.exists('encryption.key'):
                backup_zip.write('encryption.key')
        
        print(f"Backup created successfully: {backup_filename}")
        return backup_filename
    except Exception as e:
        print(f"Error creating backup: {e}")
        return None

def generate_restore_code(system_admin_username, backup_filename):
    try:
        restore_code = str(uuid.uuid4())[:8].upper()
        
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, username, role FROM Users')
        all_users = cursor.fetchall()
        
        user_found = None
        for user_id, encrypted_username, role in all_users:
            try:
                decrypted_username = decrypt_data(encrypted_username)
                if decrypted_username == system_admin_username:
                    user_found = (user_id, encrypted_username, role)
                    break
            except:
                if encrypted_username == system_admin_username:
                    user_found = (user_id, encrypted_username, role)
                    break
        
        if not user_found:
            print(f"User {system_admin_username} not found")
            close_connection(conn)
            return None
        
        user_id, encrypted_username, role = user_found
        
        try:
            decrypted_role = decrypt_data(role)
        except:
            decrypted_role = role
        
        if decrypted_role != 'System Admin':
            print(f"User {system_admin_username} is not a System Admin")
            close_connection(conn)
            return None
        
        from encryption import encrypt_data
        encrypted_code = encrypt_data(restore_code)
        encrypted_backup_filename = encrypt_data(backup_filename)
        encrypted_created_date = encrypt_data(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        encrypted_used = encrypt_data("0")
        
        cursor.execute('''
        INSERT INTO RestoreCodes (code, system_admin_username, backup_filename, created_date, used)
        VALUES (?, ?, ?, ?, ?)
        ''', (encrypted_code, encrypted_username, encrypted_backup_filename, encrypted_created_date, encrypted_used))
        
        conn.commit()
        close_connection(conn)
        
        print(f"Restore code generated: {restore_code}")
        print(f"This code is valid for backup: {backup_filename}")
        print("This code can only be used once!")
        
        return restore_code
    except Exception as e:
        print(f"Error generating restore code: {e}")
        return None

def restore_backup(restore_code, username):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, username, role FROM Users')
        all_users = cursor.fetchall()
        
        encrypted_username = None
        for user_id, encrypted_user, role in all_users:
            try:
                decrypted_user = decrypt_data(encrypted_user)
                if decrypted_user.lower() == username.lower():
                    encrypted_username = encrypted_user
                    break
            except:
                if encrypted_user.lower() == username.lower():
                    encrypted_username = encrypted_user
                    break
        
        if not encrypted_username:
            print("User not found")
            close_connection(conn)
            return False
        
        cursor.execute('''
        SELECT code, backup_filename, system_admin_username, used 
        FROM RestoreCodes 
        WHERE system_admin_username = ?
        ''', (encrypted_username,))
        
        all_codes = cursor.fetchall()
        result = None
        
        for code, backup_filename, admin_username, used in all_codes:
            try:
                decrypted_code = decrypt_data(code)
                if decrypted_code == restore_code:
                    result = (backup_filename, admin_username, used)
                    break
            except:
                if code == restore_code:
                    result = (backup_filename, admin_username, used)
                    break
        
        if not result:
            print("Invalid restore code or unauthorized user")
            return False
        
        backup_filename, admin_username, used = result
        
        try:
            decrypted_used = decrypt_data(str(used))
            is_used = decrypted_used == "1" or decrypted_used == "True" or used == 1
        except:
            is_used = used == 1 or used == "1"
        
        if is_used:
            print("Restore code has already been used")
            return False
        
        try:
            decrypted_backup_filename = decrypt_data(backup_filename)
        except:
            decrypted_backup_filename = backup_filename
        
        if not os.path.exists(decrypted_backup_filename):
            print(f"Backup file not found: {decrypted_backup_filename}")
            return False
        
        with zipfile.ZipFile(decrypted_backup_filename, 'r') as backup_zip:
            backup_zip.extractall('.')
        
        from encryption import encrypt_data
        encrypted_used = encrypt_data("1")
        
        # Find the code again to update it
        cursor.execute('SELECT code FROM RestoreCodes WHERE system_admin_username = ?', (encrypted_username,))
        all_codes = cursor.fetchall()
        matching_code = None
        for (code,) in all_codes:
            try:
                decrypted_code = decrypt_data(code)
                if decrypted_code == restore_code:
                    matching_code = code
                    break
            except:
                if code == restore_code:
                    matching_code = code
                    break
        
        if matching_code:
            cursor.execute('''
            UPDATE RestoreCodes 
            SET used = ? 
            WHERE code = ?
            ''', (encrypted_used, matching_code))
        
        conn.commit()
        close_connection(conn)
        
        print(f"Database restored successfully from {decrypted_backup_filename}")
        return True
        
    except Exception as e:
        print(f"Error restoring backup: {e}")
        return False

def list_backups():
    backup_files = []
    for file in os.listdir('.'):
        if file.startswith('backup_') and file.endswith('.zip'):
            backup_files.append(file)
    
    return sorted(backup_files, reverse=True) 

def revoke_restore_code(restore_code):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT code FROM RestoreCodes')
        all_codes = cursor.fetchall()
        
        matching_code = None
        for (code,) in all_codes:
            try:
                decrypted_code = decrypt_data(code)
                if decrypted_code == restore_code:
                    matching_code = code
                    break
            except:
                if code == restore_code:
                    matching_code = code
                    break
        
        if not matching_code:
            print(f"Restore code {restore_code} does not exist")
            close_connection(conn)
            return False
        
        cursor.execute('DELETE FROM RestoreCodes WHERE code = ?', (matching_code,))
        conn.commit()
        close_connection(conn)
        
        print(f"Restore code {restore_code} revoked successfully")
        return True
    except Exception as e:
        print(f"Error revoking restore code: {e}")
        return False

def list_restore_codes():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT code, system_admin_username, backup_filename, created_date, used
        FROM RestoreCodes
        ORDER BY created_date DESC
        ''')
        
        results = cursor.fetchall()
        close_connection(conn)
        
        if not results:
            print("No restore codes found")
            return
        
        print("\n=== RESTORE CODES ===")
        print(f"{'Code':<10} {'Admin':<15} {'Backup':<20} {'Created':<20} {'Used':<5}")
        print("-" * 80)
        
        for code, admin, backup, created, used in results:
            try:
                decrypted_code = decrypt_data(code)
                decrypted_admin = decrypt_data(admin)
                decrypted_backup = decrypt_data(backup)
                decrypted_created = decrypt_data(created)
                decrypted_used = decrypt_data(str(used))
                is_used = decrypted_used == "1" or decrypted_used == "True"
            except:
                decrypted_code = code
                decrypted_admin = admin
                decrypted_backup = backup
                decrypted_created = created
                is_used = used == 1 or used == "1"
            
            status = "Yes" if is_used else "No"
            print(f"{decrypted_code:<10} {decrypted_admin:<15} {decrypted_backup:<20} {decrypted_created:<20} {status:<5}")
        
    except Exception as e:
        print(f"Error listing restore codes: {e}")
