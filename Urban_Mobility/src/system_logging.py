"""
Logging module for Urban Mobility Backend System
Handles centralized logging with encryption and suspicious activity detection
"""

import logging
from datetime import datetime
from encryption import encrypt_log_entry, decrypt_log_entry
import os

# Setup logging
log_file = 'system.log'
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, mode='a'),
        logging.StreamHandler()
    ]
)

def log_action(username, action, additional_info="", suspicious=False):
    """Log user action with encryption"""
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    
    # Create log entry
    log_entry = f"{timestamp} | User: {username} | Action: {action}"
    if additional_info:
        log_entry += f" | Info: {additional_info}"
    if suspicious:
        log_entry += " | SUSPICIOUS: Yes"
    else:
        log_entry += " | SUSPICIOUS: No"
    
    # Encrypt and store log entry
    encrypted_entry = encrypt_log_entry(log_entry)
    
    # Write to encrypted log file
    with open('encrypted_logs.txt', 'a', encoding='utf-8') as f:
        f.write(encrypted_entry + '\n')
    
    # Also log to regular log for debugging (in production, remove this)
    logging.info(log_entry)

def log_login_attempt(username, success=True):
    """Log login attempts"""
    if success:
        log_action(username, "Logged in successfully")
    else:
        log_action(username, "Unsuccessful login attempt", suspicious=True)

def log_suspicious_activity(username, activity, details=""):
    """Log suspicious activities"""
    log_action(username, f"Suspicious activity: {activity}", details, suspicious=True)

def get_logs():
    """Retrieve and decrypt logs for authorized users"""
    try:
        if not os.path.exists('encrypted_logs.txt'):
            return "No logs available"
        
        decrypted_logs = []
        with open('encrypted_logs.txt', 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    decrypted_log = decrypt_log_entry(line.strip())
                    if decrypted_log:
                        decrypted_logs.append(decrypted_log)
        
        return decrypted_logs
    except Exception as e:
        return f"Error retrieving logs: {e}"

def get_suspicious_logs():
    """Get only suspicious activities from logs"""
    all_logs = get_logs()
    if isinstance(all_logs, str):
        return all_logs
    
    suspicious_logs = [log for log in all_logs if "SUSPICIOUS: Yes" in log]
    return suspicious_logs

def check_suspicious_activities():
    """Check for unread suspicious activities"""
    suspicious_logs = get_suspicious_logs()
    if isinstance(suspicious_logs, str):
        return 0
    
    # Count recent suspicious activities (last 24 hours)
    recent_count = 0
    current_time = datetime.now()
    
    for log in suspicious_logs:
        try:
            # Extract timestamp from log
            timestamp_str = log.split(' | ')[0]
            log_time = datetime.strptime(timestamp_str, "%d-%m-%Y %H:%M:%S")
            
            # Check if within last 24 hours
            if (current_time - log_time).total_seconds() < 86400:  # 24 hours
                recent_count += 1
        except:
            continue
    
    return recent_count

def clear_logs():
    """Clear all logs (admin function)"""
    try:
        if os.path.exists('encrypted_logs.txt'):
            os.remove('encrypted_logs.txt')
        if os.path.exists(log_file):
            os.remove(log_file)
        return True
    except Exception as e:
        print(f"Error clearing logs: {e}")
        return False
