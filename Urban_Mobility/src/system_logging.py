

import logging
from datetime import datetime
from encryption import encrypt_log_entry, decrypt_log_entry
import os

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
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    log_entry = f"{timestamp} | User: {username} | Action: {action}"
    if additional_info:
        log_entry += f" | Info: {additional_info}"
    if suspicious:
        log_entry += " | SUSPICIOUS: Yes"
    else:
        log_entry += " | SUSPICIOUS: No"
    
  
    encrypted_entry = encrypt_log_entry(log_entry)
 
    with open('encrypted_logs.txt', 'a', encoding='utf-8') as f:
        f.write(encrypted_entry + '\n')

    logging.info(log_entry)

def log_login_attempt(username, success=True):
    if success:
        log_action(username, "Logged in successfully")
    else:
        log_action(username, "Unsuccessful login attempt", suspicious=True)

def log_suspicious_activity(username, activity, details=""):
    log_action(username, f"Suspicious activity: {activity}", details, suspicious=True)

def get_logs():
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
    all_logs = get_logs()
    if isinstance(all_logs, str):
        return all_logs
    
    suspicious_logs = [log for log in all_logs if "SUSPICIOUS: Yes" in log]
    return suspicious_logs

def check_suspicious_activities():
    suspicious_logs = get_suspicious_logs()
    if isinstance(suspicious_logs, str):
        return 0
    
    recent_count = 0
    current_time = datetime.now()
    
    for log in suspicious_logs:
        try:
            timestamp_str = log.split(' | ')[0]
            log_time = datetime.strptime(timestamp_str, "%d-%m-%Y %H:%M:%S")

            if (current_time - log_time).total_seconds() < 86400:  # 24 hours
                recent_count += 1
        except:
            continue
    
    return recent_count

def clear_logs():
    try:
        if os.path.exists('encrypted_logs.txt'):
            os.remove('encrypted_logs.txt')
        if os.path.exists(log_file):
            os.remove(log_file)
        return True
    except Exception as e:
        print(f"Error clearing logs: {e}")
        return False
