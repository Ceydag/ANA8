"""
Session Management Module
Handles user sessions, timeouts, and session termination
"""

import time
from datetime import datetime, timedelta
from system_logging import log_action

# Session configuration
SESSION_TIMEOUT = 1800  # 30 minutes inactivity
MAX_SESSION_DURATION = 7200  # 2 hours maximum
MAX_INVALID_ATTEMPTS = 5  # Maximum invalid input attempts before session termination

# Global session storage
sessions = {}

class Session:
    """Session class to track user session information"""
    
    def __init__(self, username, role):
        # REQUIREMENT: Session management - track login time and activity
        self.username = username
        self.role = role
        self.login_time = datetime.now()
        self.last_activity = datetime.now()
        self.is_active = True
        self.invalid_attempts = 0  # Track invalid input attempts
        self.suspicious_activity = 0  # Track suspicious activity count
    
    def update_activity(self):
        """Update last activity timestamp"""
        self.last_activity = datetime.now()
    
    def is_expired(self):
        """Check if session has expired due to inactivity or maximum duration"""
        # Check inactivity timeout
        if (datetime.now() - self.last_activity).seconds > SESSION_TIMEOUT:
            return True, "Session expired due to inactivity"
        # Check maximum session duration
        if (datetime.now() - self.login_time).seconds > MAX_SESSION_DURATION:
            return True, "Session expired due to maximum duration"
        return False, "Session valid"
    
    def add_invalid_attempt(self):
        """Add an invalid attempt and check if session should be terminated"""
        self.invalid_attempts += 1
        if self.invalid_attempts >= MAX_INVALID_ATTEMPTS:
            return True, f"Session terminated due to {self.invalid_attempts} invalid attempts"
        return False, f"Invalid attempt {self.invalid_attempts}/{MAX_INVALID_ATTEMPTS}"
    
    def add_suspicious_activity(self):
        """Add suspicious activity and check if session should be terminated"""
        self.suspicious_activity += 1
        if self.suspicious_activity >= 3:  # Terminate after 3 suspicious activities
            return True, f"Session terminated due to {self.suspicious_activity} suspicious activities"
        return False, f"Suspicious activity {self.suspicious_activity}/3"
    
    def get_session_info(self):
        """Get session information for display"""
        time_remaining = SESSION_TIMEOUT - (datetime.now() - self.last_activity).seconds
        max_time_remaining = MAX_SESSION_DURATION - (datetime.now() - self.login_time).seconds
        
        return {
            'username': self.username,
            'role': self.role,
            'login_time': self.login_time,
            'last_activity': self.last_activity,
            'time_remaining': max(0, time_remaining),
            'max_time_remaining': max(0, max_time_remaining),
            'invalid_attempts': self.invalid_attempts,
            'suspicious_activity': self.suspicious_activity
        }

def create_session(username, role):
    """Create a new session for a user"""
    # REQUIREMENT: Session management - create session on login
    session = Session(username, role)
    sessions[username] = session
    log_action(username, "Session created", f"Login time: {session.login_time}, Role: {role}")
    return session

def get_session(username):
    """Get session for a user"""
    return sessions.get(username)

def check_session(username):
    """Check if session is valid and update activity"""
    # REQUIREMENT: Session management - check session validity
    session = get_session(username)
    if not session:
        return False, "No active session"
    
    # Check if session is expired
    is_expired, reason = session.is_expired()
    if is_expired:
        terminate_session(username, reason)
        return False, reason
    
    # Update activity
    session.update_activity()
    return True, "Session valid"

def terminate_session(username, reason="User logout"):
    """Terminate a user session"""
    # REQUIREMENT: Session management - terminate session with logging
    if username in sessions:
        session = sessions[username]
        duration = (datetime.now() - session.login_time).seconds
        log_action(username, "Session terminated", f"Reason: {reason}, Duration: {duration}s, Invalid attempts: {session.invalid_attempts}, Suspicious activities: {session.suspicious_activity}")
        del sessions[username]
        return True
    return False

def get_session_info(username):
    """Get session information for display"""
    session = get_session(username)
    if session:
        return session.get_session_info()
    return None

def display_session_info(username):
    """Display session information to user"""
    session = get_session(username)
    if not session:
        return
    
    info = session.get_session_info()
    time_remaining_min = info['time_remaining'] // 60
    max_time_remaining_min = info['max_time_remaining'] // 60
    
    print(f"\n📊 SESSION INFO")
    print(f"   User: {info['username']} ({info['role']})")
    print(f"   Time remaining: {time_remaining_min} minutes")
    print(f"   Max session time: {max_time_remaining_min} minutes")
    if info['invalid_attempts'] > 0:
        print(f"   ⚠️  Invalid attempts: {info['invalid_attempts']}/{MAX_INVALID_ATTEMPTS}")
    if info['suspicious_activity'] > 0:
        print(f"   🚨 Suspicious activities: {info['suspicious_activity']}/3")

def handle_invalid_input(username, input_value, field_name):
    """Handle invalid input and check for session termination"""
    session = get_session(username)
    if not session:
        return False, "No active session"
    
    # Log the invalid input
    log_action(username, "Invalid input detected", f"Field: {field_name}, Input: {input_value[:50]}...")
    
    # Add invalid attempt
    should_terminate, message = session.add_invalid_attempt()
    if should_terminate:
        terminate_session(username, message)
        return True, message
    
    return False, message

def handle_suspicious_activity(username, activity_description):
    """Handle suspicious activity and check for session termination"""
    session = get_session(username)
    if not session:
        return False, "No active session"
    
    # Log the suspicious activity
    log_action(username, "Suspicious activity detected", activity_description, suspicious=True)
    
    # Add suspicious activity
    should_terminate, message = session.add_suspicious_activity()
    if should_terminate:
        terminate_session(username, message)
        return True, message
    
    return False, message

def cleanup_expired_sessions():
    """Clean up expired sessions"""
    expired_users = []
    for username, session in sessions.items():
        is_expired, _ = session.is_expired()
        if is_expired:
            expired_users.append(username)
    
    for username in expired_users:
        terminate_session(username, "Session expired during cleanup")
    
    return len(expired_users)

def get_active_sessions():
    """Get list of active sessions (for admin purposes)"""
    active_sessions = []
    for username, session in sessions.items():
        if session.is_active:
            active_sessions.append(session.get_session_info())
    return active_sessions

def force_logout_user(username, reason="Forced logout by administrator"):
    """Force logout a specific user (for admin purposes)"""
    if username in sessions:
        terminate_session(username, reason)
        return True
    return False

def force_logout_all(reason="System maintenance"):
    """Force logout all users (for system maintenance)"""
    count = 0
    for username in list(sessions.keys()):
        if terminate_session(username, reason):
            count += 1
    return count
