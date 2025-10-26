

import logging
from datetime import datetime
from encryption import encrypt_log_entry, decrypt_log_entry
import os
import re
import json

encrypted_log_file = 'encrypted_logs.txt'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

def get_next_log_number():
    try:
        if not os.path.exists(encrypted_log_file):
            return 1
        
        with open(encrypted_log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if not lines:
                return 1
            
            last_line = lines[-1].strip()
            if last_line:
                decrypted = decrypt_log_entry(last_line)
                if decrypted and decrypted.startswith('No.'):
                    try:
                        last_number = int(decrypted.split()[0].split('.')[1])
                        return last_number + 1
                    except:
                        return len(lines) + 1
            return len(lines) + 1
    except:
        return 1

def log_action(username, action, additional_info="", suspicious=False):
    timestamp = datetime.now()
    date_str = timestamp.strftime("%d-%m-%Y")
    time_str = timestamp.strftime("%H:%M:%S")
    
    log_number = get_next_log_number()
    
    log_entry = f"No. {log_number} {date_str} {time_str} {username} {action}"
    if additional_info:
        log_entry += f" {additional_info}"
    log_entry += f" {'Yes' if suspicious else 'No'}"
    
    encrypted_entry = encrypt_log_entry(log_entry)
    
    with open(encrypted_log_file, 'a', encoding='utf-8') as f:
        f.write(encrypted_entry + '\n')

def log_login_attempt(username, success=True, password_attempts=1):
    if success:
        log_action(username, "Logged in", "No", False)
    else:
        suspicious = False
        additional_info = f"username: {username} is used for a login attempt with a wrong password"
        
        if password_attempts > 3:
            suspicious = True
            additional_info = f"Multiple usernames and passwords are tried in a row ({password_attempts} attempts)"
        
        log_action("...", "Unsuccessful login", additional_info, suspicious)

def log_suspicious_activity(username, activity, details=""):
    log_action(username, f"Suspicious activity: {activity}", details, True)

def detect_suspicious_patterns(username, action, additional_info=""):
    suspicious = False
    enhanced_info = additional_info
    
    if "Unsuccessful login" in action:
        recent_failures = count_recent_failed_logins(username)
        if recent_failures >= 3:
            suspicious = True
            enhanced_info = f"Multiple usernames and passwords are tried in a row ({recent_failures} attempts)"
    
    if is_rapid_successive_action(username, action):
        suspicious = True
        enhanced_info = f"Rapid successive actions detected: {action}"
    
    if "BLOCKED" in action and "wrong role" in additional_info:
        suspicious = True
        enhanced_info = f"Unauthorized access attempt: {additional_info}"
    
    return suspicious, enhanced_info

def count_recent_failed_logins(username, minutes=10):
    try:
        logs = get_logs()
        if isinstance(logs, str):
            return 0
        
        current_time = datetime.now()
        count = 0
        
        for log in logs:
            if "Unsuccessful login" in log and username in log:
                try:
                    parts = log.split()
                    if len(parts) >= 3:
                        date_str = parts[1]
                        time_str = parts[2]
                        log_time = datetime.strptime(f"{date_str} {time_str}", "%d-%m-%Y %H:%M:%S")
                        
                        if (current_time - log_time).total_seconds() < (minutes * 60):
                            count += 1
                except:
                    continue
        
        return count
    except:
        return 0

def is_rapid_successive_action(username, action, minutes=2):
    try:
        logs = get_logs()
        if isinstance(logs, str):
            return False
        
        current_time = datetime.now()
        recent_actions = 0
        
        for log in logs:
            if username in log and action in log:
                try:
                    parts = log.split()
                    if len(parts) >= 3:
                        date_str = parts[1]
                        time_str = parts[2]
                        log_time = datetime.strptime(f"{date_str} {time_str}", "%d-%m-%Y %H:%M:%S")
                        
                        if (current_time - log_time).total_seconds() < (minutes * 60):
                            recent_actions += 1
                except:
                    continue
        
        return recent_actions >= 5
    except:
        return False

def get_logs():
    try:
        if not os.path.exists(encrypted_log_file):
            return "No logs available"
        
        decrypted_logs = []
        with open(encrypted_log_file, 'r', encoding='utf-8') as f:
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
    
    suspicious_logs = [log for log in all_logs if "Yes" in log.split()[-1]]
    return suspicious_logs

def get_unread_suspicious_count():
    try:
        read_status_file = 'suspicious_read_status.json'
        read_logs = set()
        
        if os.path.exists(read_status_file):
            with open(read_status_file, 'r') as f:
                read_logs = set(json.load(f))
        
        suspicious_logs = get_suspicious_logs()
        if isinstance(suspicious_logs, str):
            return 0
        
        unread_count = 0
        for log in suspicious_logs:
            log_id = hash(log)
            if log_id not in read_logs:
                unread_count += 1
        
        return unread_count
    except:
        return 0

def mark_suspicious_as_read():
    try:
        read_status_file = 'suspicious_read_status.json'
        suspicious_logs = get_suspicious_logs()
        
        if isinstance(suspicious_logs, str):
            return
        
        read_logs = set()
        for log in suspicious_logs:
            log_id = hash(log)
            read_logs.add(log_id)
        
        with open(read_status_file, 'w') as f:
            json.dump(list(read_logs), f)
    except:
        pass

def check_suspicious_activities():
    suspicious_logs = get_suspicious_logs()
    if isinstance(suspicious_logs, str):
        return 0
    
    recent_count = 0
    current_time = datetime.now()
    
    for log in suspicious_logs:
        try:
            parts = log.split()
            if len(parts) >= 3:
                date_str = parts[1]
                time_str = parts[2]
                log_time = datetime.strptime(f"{date_str} {time_str}", "%d-%m-%Y %H:%M:%S")
                
                if (current_time - log_time).total_seconds() < 86400:  # 24 hours
                    recent_count += 1
        except:
            continue
    
    return recent_count

def display_alert_if_suspicious():
    unread_count = get_unread_suspicious_count()
    if unread_count > 0:
        print(f"\nALERT: {unread_count} unread suspicious activities detected!")
        print("Please review the security logs immediately.")
        return True
    return False

def display_logs_formatted():
    logs = get_logs()
    if isinstance(logs, str):
        print(logs)
        return
    
    if not logs:
        print("No logs available.")
        return
    
    print("\n" + "=" * 120)
    print("                                    SYSTEM ACTIVITY LOG")
    print("=" * 120)
    print(f"{'No.':<4} {'Date':<12} {'Time':<10} {'Username':<15} {'Description':<30} {'Additional Info':<25} {'Suspicious':<10}")
    print("-" * 120)
    
    for log in logs:
        try:
            parts = log.split()
            if len(parts) >= 6:
                no = parts[0] if parts[0].startswith('No.') else "N/A"
                date = parts[1] if len(parts) > 1 else "N/A"
                time = parts[2] if len(parts) > 2 else "N/A"
                username = parts[3] if len(parts) > 3 else "N/A"
                
                suspicious = parts[-1] if parts else "No"
                
                description_parts = parts[4:-1] if len(parts) > 4 else []
                description = " ".join(description_parts) if description_parts else "N/A"
                
                if len(description) > 30:
                    description = description[:27] + "..."
                
                print(f"{no:<4} {date:<12} {time:<10} {username:<15} {description:<30} {'':<25} {suspicious:<10}")
        except:
            print(f"Error parsing log: {log}")
    
    print("=" * 120)

def clear_logs():
    try:
        if os.path.exists(encrypted_log_file):
            os.remove(encrypted_log_file)
        if os.path.exists('system.log'):
            os.remove('system.log')
        return True
    except Exception as e:
        print(f"Error clearing logs: {e}")
        return False

def log_validation_failure(username, field_name, input_value, error_message, is_suspicious=False):
    truncated_input = input_value[:100] if len(input_value) > 100 else input_value
    
    suspicious_flag = detect_suspicious_input(input_value)
    
    log_entry = f"Validation failure - Field: {field_name}, Input: {truncated_input}, Error: {error_message}"
    log_action(username, "Input validation failed", log_entry, suspicious_flag or is_suspicious)

def detect_suspicious_input(input_value):
    suspicious_patterns = [
        r"('|\"|;|--|\*|\/\*|\*\/)",
        r"(<script|<iframe|<object|<embed|javascript:)",
        r"(UNION|SELECT|DROP|DELETE|INSERT|UPDATE|CREATE)",
        r"(onload|onerror|onclick|onfocus)",
        r"(\.\./|\.\.\\|%2e%2e)",
    ]
    
    for pattern in suspicious_patterns:
        if re.search(pattern, str(input_value), re.IGNORECASE):
            return True
    return False

def log_all_validation_attempts(username, field_name, input_value, is_valid, error_message=""):
    if not is_valid:
        log_validation_failure(username, field_name, input_value, error_message)
    else:
        pass
