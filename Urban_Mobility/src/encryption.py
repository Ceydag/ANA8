"""
Encryption module for Urban Mobility Backend System
Handles encryption and decryption of sensitive data using Fernet symmetric encryption
"""

from cryptography.fernet import Fernet
import base64
import os

# Generate or load encryption key
def get_or_create_key():
    """Get existing key or create new one"""
    key_file = 'encryption.key'
    
    if os.path.exists(key_file):
        with open(key_file, 'rb') as f:
            return f.read()
    else:
        # Generate new key
        key = Fernet.generate_key()
        with open(key_file, 'wb') as f:
            f.write(key)
        return key

# Initialize encryption
key = get_or_create_key()
cipher_suite = Fernet(key)

def encrypt_data(data):
    """Encrypt sensitive data"""
    if not data:
        return ""
    
    try:
        # Convert to string if not already
        data_str = str(data)
        # Encrypt the data
        encrypted_data = cipher_suite.encrypt(data_str.encode('utf-8'))
        # Return base64 encoded string for database storage
        return base64.b64encode(encrypted_data).decode('utf-8')
    except Exception as e:
        print(f"Encryption error: {e}")
        return ""

def decrypt_data(encrypted_data):
    """Decrypt sensitive data"""
    if not encrypted_data:
        return ""
    
    try:
        # Check if data is already decrypted (not base64 encoded)
        # Base64 encoded data typically starts with 'Z0FBQUFB' for Fernet
        if not encrypted_data.startswith('Z0FBQUFB'):
            return encrypted_data
        
        # Decode from base64
        encrypted_bytes = base64.b64decode(encrypted_data.encode('utf-8'))
        # Decrypt the data
        decrypted_data = cipher_suite.decrypt(encrypted_bytes)
        return decrypted_data.decode('utf-8')
    except Exception as e:
        # If decryption fails, return empty string to avoid showing encrypted data
        print(f"Decryption error: {e}")
        return ""

def encrypt_log_entry(log_entry):
    """Encrypt log entry for secure storage"""
    return encrypt_data(log_entry)

def decrypt_log_entry(encrypted_log):
    """Decrypt log entry for reading"""
    return decrypt_data(encrypted_log)
