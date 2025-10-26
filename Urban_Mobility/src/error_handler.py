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
        log_action(username, f"User interrupted operation in {context}", "Keyboard interrupt (Ctrl+C) - System shutdown", suspicious=False)
        print("\n\nSystem interrupted by user. Shutting down...")
        print("System shutdown initiated by user.")
        sys.exit(0)
    except Exception as e:
        handle_exception(username, context, e, show_details=True)
        print("Critical system error. Exiting for security reasons.")
        sys.exit(1)
