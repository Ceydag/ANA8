import time
import secrets
import hashlib
from datetime import datetime, timedelta
from system_logging import log_action

SESSION_TIMEOUT = 1800
MAX_SESSION_DURATION = 7200
MAX_INVALID_ATTEMPTS = 5

sessions = {}

class Session:
    
    def __init__(self, username, role):
        self.username = username
        self.role = role
        self.session_id = self._generate_session_id()
        self.login_time = datetime.now()
        self.last_activity = datetime.now()
        self.is_active = True
        self.invalid_attempts = 0
        self.suspicious_activity = 0
    
    def _generate_session_id(self):
        return secrets.token_urlsafe(32)
    
    def update_activity(self):
        self.last_activity = datetime.now()
    
    def is_expired(self):
        if (datetime.now() - self.last_activity).seconds > SESSION_TIMEOUT:
            return True, "Session expired due to inactivity"
        if (datetime.now() - self.login_time).seconds > MAX_SESSION_DURATION:
            return True, "Session expired due to maximum duration"
        return False, "Session valid"
    
    def add_invalid_attempt(self):
        self.invalid_attempts += 1
        if self.invalid_attempts >= MAX_INVALID_ATTEMPTS:
            return True, f"Session terminated due to {self.invalid_attempts} invalid attempts"
        return False, f"Invalid attempt {self.invalid_attempts}/{MAX_INVALID_ATTEMPTS}"
    
    def add_suspicious_activity(self):
        self.suspicious_activity += 1
        if self.suspicious_activity >= 3:
            return True, f"Session terminated due to {self.suspicious_activity} suspicious activities"
        return False, f"Suspicious activity {self.suspicious_activity}/3"
    
    def get_session_info(self):
        time_remaining = SESSION_TIMEOUT - (datetime.now() - self.last_activity).seconds
        max_time_remaining = MAX_SESSION_DURATION - (datetime.now() - self.login_time).seconds
        
        return {
            'username': self.username,
            'role': self.role,
            'session_id': self.session_id[:8] + "...",
            'login_time': self.login_time,
            'last_activity': self.last_activity,
            'time_remaining': max(0, time_remaining),
            'max_time_remaining': max(0, max_time_remaining),
            'invalid_attempts': self.invalid_attempts,
            'suspicious_activity': self.suspicious_activity
        }

def create_session(username, role):
    if username in sessions:
        terminate_session(username, "New session created")
    
    session = Session(username, role)
    sessions[session.session_id] = session
    sessions[username] = session
    
    log_action(username, "Session created", f"Session ID: {session.session_id[:16]}..., Login time: {session.login_time}, Role: {role}")
    return session

def get_session_by_username(username):
    return sessions.get(username)

def get_session_by_id(session_id):
    return sessions.get(session_id)

def check_session(username):
    session = get_session_by_username(username)
    if not session:
        return False, "No active session"
    
    is_expired, reason = session.is_expired()
    if is_expired:
        terminate_session(username, reason)
        return False, reason
    
    session.update_activity()
    return True, "Session valid"

def terminate_session(username, reason="User logout"):
    if username in sessions:
        session = sessions[username]
        if session.session_id in sessions:
            del sessions[session.session_id]
        del sessions[username]
        
        duration = (datetime.now() - session.login_time).seconds
        log_action(username, "Session terminated", f"Reason: {reason}, Duration: {duration}s, Invalid attempts: {session.invalid_attempts}, Suspicious activities: {session.suspicious_activity}")
        return True
    return False

def terminate_session_by_id(session_id, reason="Session terminated"):
    session = get_session_by_id(session_id)
    if session:
        username = session.username
        if session.session_id in sessions:
            del sessions[session.session_id]
        if username in sessions:
            del sessions[username]
        
        duration = (datetime.now() - session.login_time).seconds
        log_action(username, "Session terminated", f"Reason: {reason}, Duration: {duration}s")
        return True
    return False

def get_session_info(username):
    session = get_session_by_username(username)
    if session:
        return session.get_session_info()
    return None

def display_session_info(username):
    session = get_session_by_username(username)
    if not session:
        return
    
    info = session.get_session_info()
    max_time_remaining_min = info['max_time_remaining'] // 60
    
    print(f"\nSESSION INFO")
    print(f"User: {info['username']} ({info['role']})")
    print(f"Session ID: {info['session_id']}")
    print(f"Max session time remaining: {max_time_remaining_min} minutes")
    if info['invalid_attempts'] > 0:
        print(f"Invalid attempts: {info['invalid_attempts']}/{MAX_INVALID_ATTEMPTS}")
    if info['suspicious_activity'] > 0:
        print(f"Suspicious activities: {info['suspicious_activity']}/3")

def handle_invalid_input(username, input_value, field_name):
    session = get_session_by_username(username)
    if not session:
        return False, "No active session"
    
    log_action(username, "Invalid input detected", f"Field: {field_name}, Input: {input_value[:50]}...")
    
    should_terminate, message = session.add_invalid_attempt()
    if should_terminate:
        terminate_session(username, message)
        return True, message
    
    return False, message

def handle_suspicious_activity(username, activity_description):
    session = get_session_by_username(username)
    if not session:
        return False, "No active session"
    
    log_action(username, "Suspicious activity detected", activity_description, suspicious=True)
    
    should_terminate, message = session.add_suspicious_activity()
    if should_terminate:
        terminate_session(username, message)
        return True, message
    
    return False, message

def cleanup_expired_sessions():
    expired_users = []
    for username, session in sessions.items():
        is_expired, _ = session.is_expired()
        if is_expired:
            expired_users.append(username)
    
    for username in expired_users:
        terminate_session(username, "Session expired during cleanup")
    
    return len(expired_users)

def get_active_sessions():
    active_sessions = []
    for username, session in sessions.items():
        if session.is_active:
            active_sessions.append(session.get_session_info())
    return active_sessions

def force_logout_user(username, reason="Forced logout by administrator"):
    if username in sessions:
        terminate_session(username, reason)
        return True
    return False

def force_logout_all(reason="System maintenance"):
    count = 0
    for username in list(sessions.keys()):
        if terminate_session(username, reason):
            count += 1
    return count
