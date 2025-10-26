import sqlite3
import sys
from system_logging import log_action
from datetime import datetime

def handle_exception(username, context, exception, show_details=False):
    error_type = type(exception).__name__
    error_message = str(exception)

    log_action(
        username, 
        f"System error in {context}", 
        f"Type: {error_type}, Message: {error_message}", 
        suspicious=False
    )
    
    print("\n" + "="*60)
    print("An error occurred")
    print("="*60)
    if show_details:
        print(f"Context: {context}")
        print(f"Error: {error_message}")
    else:
        print("The system encountered an error and has been logged.")
        print("Returning to main menu...")
    print("="*60)
    
    return False

def safe_execute(func, username, context, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except KeyboardInterrupt:
        handle_keyboard_interrupt(username, context)
        print("System shutdown initiated by user.")
        sys.exit(0)
    except Exception as e:
        handle_exception(username, context, e, show_details=True)
        print("Critical system error. Exiting for security reasons.")
        sys.exit(1)

def handle_database_error(username, context, exception):
    if isinstance(exception, sqlite3.OperationalError):
        log_action(username, f"Database operational error in {context}", str(exception), suspicious=True)
        print("Database operation failed. Please try again.")
    elif isinstance(exception, sqlite3.IntegrityError):
        log_action(username, f"Database integrity error in {context}", str(exception), suspicious=True)
        print("Data integrity violation. Please check your input.")
    elif isinstance(exception, sqlite3.DatabaseError):
        log_action(username, f"Database error in {context}", str(exception), suspicious=True)
        print("Database error occurred. Please contact administrator.")
    else:
        handle_exception(username, context, exception)
    return False

def handle_validation_error(username, context, exception):
    log_action(username, f"Validation error in {context}", str(exception), suspicious=False)
    print("Input validation failed. Please check your input format.")
    return False

def handle_authentication_error(username, context, exception):
    log_action(username, f"Authentication error in {context}", str(exception), suspicious=True)
    print("Authentication failed. Please check your credentials.")
    return False

def handle_encryption_error(username, context, exception):
    log_action(username, f"Encryption error in {context}", str(exception), suspicious=True)
    print("Data encryption/decryption failed. Please contact administrator.")
    return False

def handle_file_error(username, context, exception):
    log_action(username, f"File operation error in {context}", str(exception), suspicious=False)
    print("File operation failed. Please check file permissions and try again.")
    return False

def handle_network_error(username, context, exception):
    log_action(username, f"Network error in {context}", str(exception), suspicious=False)
    print("Network operation failed. Please check your connection.")
    return False

def handle_timeout_error(username, context, exception):
    log_action(username, f"Timeout error in {context}", str(exception), suspicious=False)
    print("Operation timed out. Please try again.")
    return False

def handle_permission_error(username, context, exception):
    log_action(username, f"Permission error in {context}", str(exception), suspicious=True)
    print("Insufficient permissions for this operation.")
    return False

def handle_memory_error(username, context, exception):
    log_action(username, f"Memory error in {context}", str(exception), suspicious=True)
    print("System memory error. Please contact administrator.")
    return False

def handle_keyboard_interrupt(username, context):
    log_action(username, f"User interrupted operation in {context}", "Keyboard interrupt (Ctrl+C) - System shutdown", suspicious=False)
    print("\n\nSystem interrupted by user. Shutting down...")

def handle_system_exit(username, context):
    log_action(username, f"System exit requested in {context}", "User requested system exit", suspicious=False)
    print("System shutting down...")
    return False
