"""
Input validation module for Urban Mobility Backend System
Handles validation of all user inputs using regex patterns
"""

import re
from datetime import datetime

def validate_username(username):
    """Validate username according to requirements"""
    if not username or len(username) < 8 or len(username) > 10:
        return False, "Username must be 8-10 characters long"
    
    if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_\'\.]*$', username):
        return False, "Username must start with letter or underscore and contain only letters, numbers, underscores, apostrophes, and periods"
    
    return True, "Valid username"

def validate_password(password):
    """Validate password according to requirements"""
    if len(password) < 12 or len(password) > 30:
        return False, "Password must be 12-30 characters long"
    
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in "~!@#$%&_-+=`|\\(){}[]:;'<>,.?/" for c in password)
    
    if not (has_lower and has_upper and has_digit and has_special):
        return False, "Password must contain at least one lowercase letter, one uppercase letter, one digit, and one special character"
    
    return True, "Valid password"

def validate_email(email):
    """Validate email address"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False, "Invalid email format"
    return True, "Valid email"

def validate_phone(phone):
    """Validate mobile phone number (DDDDDDDD format)"""
    if not re.match(r'^\d{8}$', phone):
        return False, "Phone number must be 8 digits (DDDDDDDD)"
    return True, "Valid phone number"

def validate_zip_code(zip_code):
    """Validate Dutch zip code (DDDDXX format)"""
    if not re.match(r'^\d{4}[A-Z]{2}$', zip_code):
        return False, "Zip code must be in format DDDDXX (4 digits, 2 uppercase letters)"
    return True, "Valid zip code"

def validate_driving_license(license_num):
    """Validate driving license number (XXDDDDDDD or XDDDDDDDD format)"""
    if not re.match(r'^[A-Z]{1,2}\d{7,8}$', license_num):
        return False, "Driving license must be in format XXDDDDDDD or XDDDDDDDD"
    return True, "Valid driving license"

def validate_birthday(birthday):
    """Validate birthday format (YYYY-MM-DD)"""
    try:
        datetime.strptime(birthday, '%Y-%m-%d')
        return True, "Valid birthday"
    except ValueError:
        return False, "Birthday must be in format YYYY-MM-DD"

def validate_gender(gender):
    """Validate gender (male or female)"""
    if gender.lower() not in ['male', 'female']:
        return False, "Gender must be 'male' or 'female'"
    return True, "Valid gender"

def validate_city(city):
    """Validate city (must be from predefined list)"""
    predefined_cities = [
        'Rotterdam', 'Amsterdam', 'Utrecht', 'The Hague', 'Eindhoven',
        'Tilburg', 'Groningen', 'Almere', 'Breda', 'Nijmegen'
    ]
    if city not in predefined_cities:
        return False, f"City must be one of: {', '.join(predefined_cities)}"
    return True, "Valid city"

def validate_serial_number(serial_num):
    """Validate scooter serial number (10-17 alphanumeric characters)"""
    if not re.match(r'^[A-Za-z0-9]{10,17}$', serial_num):
        return False, "Serial number must be 10-17 alphanumeric characters"
    return True, "Valid serial number"

def validate_coordinates(latitude, longitude):
    """Validate GPS coordinates for Rotterdam region"""
    try:
        lat = float(latitude)
        lon = float(longitude)
        
        # Rotterdam region bounds (approximate)
        if not (51.8 <= lat <= 52.1) or not (4.2 <= lon <= 4.8):
            return False, "Coordinates must be within Rotterdam region"
        
        # Check decimal places (5 decimal places for 2-meter accuracy)
        if len(str(lat).split('.')[-1]) > 5 or len(str(lon).split('.')[-1]) > 5:
            return False, "Coordinates must have maximum 5 decimal places"
        
        return True, "Valid coordinates"
    except ValueError:
        return False, "Invalid coordinate format"

def validate_maintenance_date(date_str):
    """Validate maintenance date (ISO 8601 format: YYYY-MM-DD)"""
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True, "Valid maintenance date"
    except ValueError:
        return False, "Maintenance date must be in format YYYY-MM-DD"

def validate_numeric_input(value, min_val=None, max_val=None, field_name="value"):
    """Validate numeric input with optional min/max constraints"""
    try:
        num = float(value)
        if min_val is not None and num < min_val:
            return False, f"{field_name} must be at least {min_val}"
        if max_val is not None and num > max_val:
            return False, f"{field_name} must be at most {max_val}"
        return True, f"Valid {field_name}"
    except ValueError:
        return False, f"{field_name} must be a valid number"

def sanitize_input(input_str):
    """Sanitize input to prevent injection attacks"""
    if not input_str:
        return ""
    
    # Remove null bytes and other dangerous characters
    sanitized = input_str.replace('\x00', '').replace('\r', '').replace('\n', '')
    
    # Limit length to prevent buffer overflow
    if len(sanitized) > 1000:
        sanitized = sanitized[:1000]
    
    return sanitized.strip()
