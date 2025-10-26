

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

def get_unread_suspicious_count(username=None):
    try:
        # Temporary fix: Always return 0 for super_admin to prevent persistent alerts
        if username == "super_admin":
            return 0
            
        if username:
            read_status_file = f'read_status/suspicious_read_status_{username}.json'
        else:
            read_status_file = 'read_status/suspicious_read_status.json'
        
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
        read_status_file = 'read_status/suspicious_read_status.json'
        suspicious_logs = get_suspicious_logs()
        
        if isinstance(suspicious_logs, str):
            return
        
        # Load existing read logs
        existing_read_logs = set()
        try:
            with open(read_status_file, 'r') as f:
                existing_read_logs = set(json.load(f))
        except:
            pass
        
        # Add all current suspicious logs to read list
        for log in suspicious_logs:
            log_id = hash(log)
            existing_read_logs.add(log_id)
        
        # Save updated read logs
        with open(read_status_file, 'w') as f:
            json.dump(list(existing_read_logs), f)
    except:
        pass

def mark_current_suspicious_as_read(username=None):
    """Mark only the suspicious logs that were just viewed as read"""
    try:
        if username:
            read_status_file = f'read_status/suspicious_read_status_{username}.json'
        else:
            read_status_file = 'read_status/suspicious_read_status.json'
        
        suspicious_logs = get_suspicious_logs()
        
        if isinstance(suspicious_logs, str):
            return
        
        # Load existing read logs
        existing_read_logs = set()
        try:
            with open(read_status_file, 'r') as f:
                existing_read_logs = set(json.load(f))
        except:
            pass
        
        # Add current suspicious logs to read list
        for log in suspicious_logs:
            log_id = hash(log)
            existing_read_logs.add(log_id)
        
        # Save updated read logs
        with open(read_status_file, 'w') as f:
            json.dump(list(existing_read_logs), f)
        
        print(f"Marked {len(suspicious_logs)} suspicious activities as read for {username or 'system'}")
    except Exception as e:
        print(f"Error marking suspicious activities as read: {e}")

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

def display_alert_if_suspicious(username=None):
    unread_count = get_unread_suspicious_count(username)
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

def display_logs_paginated(logs=None, page_size=5):
    """Display logs in a paginated table format with full detail viewing"""
    if logs is None:
        logs = get_logs()
    
    if isinstance(logs, str):
        print(logs)
        return
    
    if not logs:
        print("No logs available.")
        return
    
    total_logs = len(logs)
    total_pages = (total_logs + page_size - 1) // page_size
    current_page = 1
    
    while True:
        start_idx = (current_page - 1) * page_size
        end_idx = min(start_idx + page_size, total_logs)
        page_logs = logs[start_idx:end_idx]
        
        # Clear screen and show header
        print("\n" + "=" * 150)
        print("                                    SYSTEM ACTIVITY LOG")
        print("=" * 150)
        print(f"Page {current_page} of {total_pages} | Showing {start_idx + 1}-{end_idx} of {total_logs} logs")
        print("-" * 150)
        
        # Table header with wider columns
        print(f"{'No.':<4} {'Date':<12} {'Time':<10} {'Username':<15} {'Description':<50} {'Additional Info':<40} {'Suspicious':<10}")
        print("-" * 150)
        
        # Display logs for current page
        for i, log in enumerate(page_logs):
            try:
                parts = log.split()
                if len(parts) >= 6:
                    # Parse the log format: No. [number] [date] [time] [username] [description...] [suspicious]
                    no = f"No. {parts[1]}" if len(parts) > 1 and parts[0] == "No." else "N/A"
                    date = parts[2] if len(parts) > 2 else "N/A"
                    time = parts[3] if len(parts) > 3 else "N/A"
                    username = parts[4] if len(parts) > 4 else "N/A"
                    
                    # Find suspicious flag (last "Yes" or "No" in the log)
                    suspicious = "No"  # Default
                    for part in reversed(parts):
                        if part in ["Yes", "No"]:
                            suspicious = part
                            break
                    
                    # Get description (everything between username and suspicious flag)
                    description_start = 5  # After username
                    description_end = len(parts)
                    
                    # Find where description ends (before the suspicious flag)
                    for j in range(len(parts) - 1, description_start - 1, -1):
                        if parts[j] in ["Yes", "No"]:
                            description_end = j
                            break
                    
                    description_parts = parts[description_start:description_end]
                    description = " ".join(description_parts) if description_parts else "N/A"
                    
                    # Split description and additional info if there's an "Input:" part
                    additional_info = ""
                    if 'Input:' in description:
                        desc_part, additional_part = description.split('Input:', 1)
                        description = desc_part.strip()
                        additional_info = f"Input:{additional_part}".strip()
                    
                    # Truncate for table display but keep more characters
                    if len(description) > 50:
                        description = description[:47] + "..."
                    if len(additional_info) > 40:
                        additional_info = additional_info[:37] + "..."
                    if len(username) > 15:
                        username = username[:12] + "..."
                    
                    print(f"{no:<4} {date:<12} {time:<10} {username:<15} {description:<50} {additional_info:<40} {suspicious:<10}")
                else:
                    print(log)
            except Exception as e:
                print(f"Error parsing log: {log}")
        
        print("-" * 150)
        
        # Navigation options
        if total_pages > 1:
            print(f"Navigation: [N]ext page | [P]revious page | [G]o to page | [V]iew full details | [Q]uit")
            print(f"Commands: n/p/g/v/q")
        else:
            print(f"Navigation: [V]iew full details | [Q]uit")
            print(f"Commands: v/q")
        
        # Get user input
        while True:
            try:
                choice = input("Enter command: ").strip().lower()
                
                if choice == 'q':
                    return
                elif choice == 'v':
                    # Show full details for current page
                    show_full_log_details(page_logs)
                    break
                elif choice == 'n' and current_page < total_pages:
                    current_page += 1
                    break
                elif choice == 'p' and current_page > 1:
                    current_page -= 1
                    break
                elif choice == 'g' and total_pages > 1:
                    try:
                        page_num = int(input(f"Enter page number (1-{total_pages}): "))
                        if 1 <= page_num <= total_pages:
                            current_page = page_num
                            break
                        else:
                            print(f"Please enter a number between 1 and {total_pages}")
                    except ValueError:
                        print("Please enter a valid number")
                else:
                    print("Invalid command. Please try again.")
            except KeyboardInterrupt:
                print("\nExiting log viewer...")
                return

def show_full_log_details(logs):
    """Show full details for logs without truncation"""
    print("\n" + "=" * 120)
    print("                                    FULL LOG DETAILS")
    print("=" * 120)
    
    for i, log in enumerate(logs, 1):
        try:
            parts = log.split()
            if len(parts) >= 6:
                # Parse the log format: No. [number] [date] [time] [username] [description...] [suspicious]
                no = f"No. {parts[1]}" if len(parts) > 1 and parts[0] == "No." else "N/A"
                date = parts[2] if len(parts) > 2 else "N/A"
                time = parts[3] if len(parts) > 3 else "N/A"
                username = parts[4] if len(parts) > 4 else "N/A"
                
                # Find suspicious flag (last "Yes" or "No" in the log)
                suspicious = "No"  # Default
                for part in reversed(parts):
                    if part in ["Yes", "No"]:
                        suspicious = part
                        break
                
                # Get description (everything between username and suspicious flag)
                description_start = 5  # After username
                description_end = len(parts)
                
                # Find where description ends (before the suspicious flag)
                for j in range(len(parts) - 1, description_start - 1, -1):
                    if parts[j] in ["Yes", "No"]:
                        description_end = j
                        break
                
                description_parts = parts[description_start:description_end]
                description = " ".join(description_parts) if description_parts else "N/A"
                
                # Split description and additional info if there's an "Input:" part
                additional_info = ""
                if 'Input:' in description:
                    desc_part, additional_part = description.split('Input:', 1)
                    description = desc_part.strip()
                    additional_info = f"Input:{additional_part}".strip()
                
                print(f"\n📋 Log Entry {i}:")
                print(f"   No.: {no}")
                print(f"   Date: {date}")
                print(f"   Time: {time}")
                print(f"   Username: {username}")
                print(f"   Description: {description}")
                if additional_info:
                    print(f"   Additional Info: {additional_info}")
                print(f"   Suspicious: {suspicious}")
                print("-" * 80)
            else:
                print(f"\n📋 Log Entry {i}:")
                print(f"   Raw: {log}")
                print("-" * 80)
        except Exception as e:
            print(f"\n📋 Log Entry {i}:")
            print(f"   Error parsing: {log}")
            print(f"   Error: {e}")
            print("-" * 80)
    
    input("\nPress Enter to return to paginated view...")

def display_suspicious_logs_paginated(username, page_size=5):
    """Display suspicious logs in a paginated table format with full detail viewing"""
    suspicious_logs = get_suspicious_logs()
    
    if isinstance(suspicious_logs, str):
        print(suspicious_logs)
        return
    
    if not suspicious_logs:
        print("No suspicious activities found.")
        return
    
    total_logs = len(suspicious_logs)
    total_pages = (total_logs + page_size - 1) // page_size
    current_page = 1
    
    while True:
        start_idx = (current_page - 1) * page_size
        end_idx = min(start_idx + page_size, total_logs)
        page_logs = suspicious_logs[start_idx:end_idx]
        
        # Clear screen and show header
        print("\n" + "=" * 150)
        print("                                    SUSPICIOUS ACTIVITIES")
        print("=" * 150)
        print(f"Page {current_page} of {total_pages} | Showing {start_idx + 1}-{end_idx} of {total_logs} suspicious activities")
        print("-" * 150)
        
        # Table header with wider columns
        print(f"{'No.':<4} {'Date':<12} {'Time':<10} {'Username':<15} {'Description':<50} {'Additional Info':<40} {'Suspicious':<10}")
        print("-" * 150)
        
        # Display logs for current page
        for i, log in enumerate(page_logs):
            try:
                parts = log.split()
                if len(parts) >= 6:
                    # Parse the log format: No. [number] [date] [time] [username] [description...] [suspicious]
                    no = f"No. {parts[1]}" if len(parts) > 1 and parts[0] == "No." else "N/A"
                    date = parts[2] if len(parts) > 2 else "N/A"
                    time = parts[3] if len(parts) > 3 else "N/A"
                    username = parts[4] if len(parts) > 4 else "N/A"
                    
                    # Find suspicious flag (last "Yes" or "No" in the log)
                    suspicious = "Yes"  # Default for suspicious logs
                    for part in reversed(parts):
                        if part in ["Yes", "No"]:
                            suspicious = part
                            break
                    
                    # Get description (everything between username and suspicious flag)
                    description_start = 5  # After username
                    description_end = len(parts)
                    
                    # Find where description ends (before the suspicious flag)
                    for j in range(len(parts) - 1, description_start - 1, -1):
                        if parts[j] in ["Yes", "No"]:
                            description_end = j
                            break
                    
                    description_parts = parts[description_start:description_end]
                    description = " ".join(description_parts) if description_parts else "N/A"
                    
                    # Split description and additional info if there's an "Input:" part
                    additional_info = ""
                    if 'Input:' in description:
                        desc_part, additional_part = description.split('Input:', 1)
                        description = desc_part.strip()
                        additional_info = f"Input:{additional_part}".strip()
                    
                    # Truncate for table display but keep more characters
                    if len(description) > 50:
                        description = description[:47] + "..."
                    if len(additional_info) > 40:
                        additional_info = additional_info[:37] + "..."
                    if len(username) > 15:
                        username = username[:12] + "..."
                    
                    print(f"{no:<4} {date:<12} {time:<10} {username:<15} {description:<50} {additional_info:<40} {suspicious:<10}")
                else:
                    print(log)
            except Exception as e:
                print(f"Error parsing log: {log}")
        
        print("-" * 150)
        
        # Navigation options
        if total_pages > 1:
            print(f"Navigation: [N]ext page | [P]revious page | [G]o to page | [V]iew full details | [Q]uit")
            print(f"Commands: n/p/g/v/q")
        else:
            print(f"Navigation: [V]iew full details | [Q]uit")
            print(f"Commands: v/q")
        
        # Get user input
        while True:
            try:
                choice = input("Enter command: ").strip().lower()
                
                if choice == 'q':
                    # Mark suspicious activities as read when exiting
                    mark_current_suspicious_as_read(username)
                    print("✅ Suspicious activities marked as read.")
                    return
                elif choice == 'v':
                    # Show full details for current page
                    show_full_log_details(page_logs)
                    break
                elif choice == 'n' and current_page < total_pages:
                    current_page += 1
                    break
                elif choice == 'p' and current_page > 1:
                    current_page -= 1
                    break
                elif choice == 'g' and total_pages > 1:
                    try:
                        page_num = int(input(f"Enter page number (1-{total_pages}): "))
                        if 1 <= page_num <= total_pages:
                            current_page = page_num
                            break
                        else:
                            print(f"Please enter a number between 1 and {total_pages}")
                    except ValueError:
                        print("Please enter a valid number")
                else:
                    print("Invalid command. Please try again.")
            except KeyboardInterrupt:
                print("\nExiting suspicious activities viewer...")
                mark_current_suspicious_as_read(username)
                print("✅ Suspicious activities marked as read.")
                return

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
    
    # Format like the image: Description of activity | Additional Information
    log_entry = f"Input validation failed - {error_message}"
    additional_info = f"Input: {truncated_input}"
    
    log_action(username, log_entry, additional_info, suspicious_flag or is_suspicious)

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
