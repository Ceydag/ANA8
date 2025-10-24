"""
Backup and restore module for Urban Mobility Backend System
Handles database backup and restore functionality with role-based access
"""

import zipfile
import os
import sqlite3
from datetime import datetime
import uuid
from database import get_connection, close_connection
from encryption import encrypt_data, decrypt_data

def create_backup():
    """Create backup of the database"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"backup_{timestamp}.zip"
        
        with zipfile.ZipFile(backup_filename, 'w', zipfile.ZIP_DEFLATED) as backup_zip:
            # Add database file
            if os.path.exists('urban_mobility.db'):
                backup_zip.write('urban_mobility.db')
            
            # Add encrypted logs if they exist
            if os.path.exists('encrypted_logs.txt'):
                backup_zip.write('encrypted_logs.txt')
            
            # Add encryption key
            if os.path.exists('encryption.key'):
                backup_zip.write('encryption.key')
        
        print(f"Backup created successfully: {backup_filename}")
        return backup_filename
    except Exception as e:
        print(f"Error creating backup: {e}")
        return None

def generate_restore_code(system_admin_username, backup_filename):
    """Generate one-time restore code for System Admin"""
    try:
        # Generate unique restore code
        restore_code = str(uuid.uuid4())[:8].upper()
        
        conn = get_connection()
        cursor = conn.cursor()
        
        # Check if user exists and is a System Admin
        cursor.execute('SELECT role FROM Users WHERE username = ?', (system_admin_username,))
        user_result = cursor.fetchone()
        
        if not user_result:
            print(f"User {system_admin_username} not found")
            close_connection(conn)
            return None
        
        if user_result[0] != 'System Admin':
            print(f"User {system_admin_username} is not a System Admin")
            close_connection(conn)
            return None
        
        # Store restore code in database
        cursor.execute('''
        INSERT INTO RestoreCodes (code, system_admin_username, backup_filename, created_date)
        VALUES (?, ?, ?, datetime('now'))
        ''', (restore_code, system_admin_username, backup_filename))
        
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
    """Restore database from backup using restore code"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Check if restore code exists and is unused
        cursor.execute('''
        SELECT backup_filename, system_admin_username, used 
        FROM RestoreCodes 
        WHERE code = ? AND system_admin_username = ?
        ''', (restore_code, username))
        
        result = cursor.fetchone()
        
        if not result:
            print("Invalid restore code or unauthorized user")
            return False
        
        backup_filename, admin_username, used = result
        
        if used:
            print("Restore code has already been used")
            return False
        
        # Check if backup file exists
        if not os.path.exists(backup_filename):
            print(f"Backup file not found: {backup_filename}")
            return False
        
        # Extract backup
        with zipfile.ZipFile(backup_filename, 'r') as backup_zip:
            backup_zip.extractall('.')
        
        # Mark restore code as used
        cursor.execute('''
        UPDATE RestoreCodes 
        SET used = 1 
        WHERE code = ?
        ''', (restore_code,))
        
        conn.commit()
        close_connection(conn)
        
        print(f"Database restored successfully from {backup_filename}")
        return True
        
    except Exception as e:
        print(f"Error restoring backup: {e}")
        return False

def list_backups():
    """List available backup files"""
    backup_files = []
    for file in os.listdir('.'):
        if file.startswith('backup_') and file.endswith('.zip'):
            backup_files.append(file)
    
    return sorted(backup_files, reverse=True)  # Most recent first

def revoke_restore_code(restore_code):
    """Revoke a restore code (Super Admin only)"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM RestoreCodes WHERE code = ?', (restore_code,))
        conn.commit()
        close_connection(conn)
        
        print(f"Restore code {restore_code} revoked successfully")
        return True
    except Exception as e:
        print(f"Error revoking restore code: {e}")
        return False

def list_restore_codes():
    """List all restore codes (Super Admin only)"""
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
            status = "Yes" if used else "No"
            print(f"{code:<10} {admin:<15} {backup:<20} {created:<20} {status:<5}")
        
    except Exception as e:
        print(f"Error listing restore codes: {e}")
