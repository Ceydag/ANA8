from cryptography.fernet import Fernet
import base64
import os

def get_or_create_key():
    key_file = 'encryption.key'
    
    if os.path.exists(key_file):
        with open(key_file, 'rb') as f:
            return f.read()
    else:
        key = Fernet.generate_key()
        with open(key_file, 'wb') as f:
            f.write(key)
        return key

key = get_or_create_key()
cipher_suite = Fernet(key)

def encrypt_data(data):
    if not data:
        return ""
    
    try:
        data_str = str(data)
        encrypted_data = cipher_suite.encrypt(data_str.encode('utf-8'))
        return base64.b64encode(encrypted_data).decode('utf-8')
    except Exception as e:
        print(f"Encryption error: {e}")
        return ""

def decrypt_data(encrypted_data):
    if not encrypted_data:
        return ""
    
    try:
        if not encrypted_data.startswith('Z0FBQUFB'):
            return encrypted_data

        encrypted_bytes = base64.b64decode(encrypted_data.encode('utf-8'))
        decrypted_data = cipher_suite.decrypt(encrypted_bytes)
        return decrypted_data.decode('utf-8')
    except Exception as e:
        print(f"Decryption error: {e}")
        return ""

def encrypt_log_entry(log_entry):
    return encrypt_data(log_entry)

def decrypt_log_entry(encrypted_log):
    return decrypt_data(encrypted_log)
