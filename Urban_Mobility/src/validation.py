import re
from datetime import datetime

def validate_username(username):
    # REQUIREMENT: Whitelist validation - only allow specific characters
    # REQUIREMENT: Length checking - enforce 8-10 character limit
    if not username or len(username) < 8 or len(username) > 10:
        return False, "Username must be 8-10 characters long"
    
    if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_\'\.]*$', username):
        return False, "Username must start with letter or underscore and contain only letters, numbers, underscores, apostrophes, and periods"
    
    return True, "Valid username"

def validate_password(password):
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
    # REQUIREMENT: Whitelist validation - only allow specific email format
    if not email:
        return False, "Email cannot be empty"
    if len(email) > 254:  # RFC 5321 maximum email length
        return False, "Email too long (maximum 254 characters)"
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False, "Invalid email format"
    return True, "Valid email"

def validate_phone(phone):
    # REQUIREMENT: Whitelist validation - only allow 8 digits
    if not phone:
        return False, "Phone number cannot be empty"
    if len(phone) != 8:
        return False, "Phone number must be exactly 8 digits"
    if not re.match(r'^\d{8}$', phone):
        return False, "Phone number must be 8 digits (DDDDDDDD)"
    return True, "Valid phone number"

def validate_zip_code(zip_code):
    # REQUIREMENT: Whitelist validation - only allow Dutch zip code format
    if not zip_code:
        return False, "Zip code cannot be empty"
    if len(zip_code) != 6:
        return False, "Zip code must be exactly 6 characters"
    if not re.match(r'^\d{4}[A-Z]{2}$', zip_code):
        return False, "Zip code must be in format DDDDXX (4 digits, 2 uppercase letters)"
    return True, "Valid zip code"

def validate_driving_license(license_num):
    # REQUIREMENT: Whitelist validation - only allow specific license format
    if not license_num:
        return False, "Driving license cannot be empty"
    if len(license_num) < 8 or len(license_num) > 10:
        return False, "Driving license must be 8-10 characters"
    if not re.match(r'^[A-Z]{1,2}\d{7,8}$', license_num):
        return False, "Driving license must be in format XXDDDDDDD or XDDDDDDDD"
    return True, "Valid driving license"

def validate_birthday(birthday):
    # REQUIREMENT: Whitelist validation - only allow YYYY-MM-DD format
    if not birthday:
        return False, "Birthday cannot be empty"
    if len(birthday) != 10:
        return False, "Birthday must be exactly 10 characters (YYYY-MM-DD)"
    try:
        datetime.strptime(birthday, '%Y-%m-%d')
        return True, "Valid birthday"
    except ValueError:
        return False, "Birthday must be in format YYYY-MM-DD"

def validate_gender(gender):
    # REQUIREMENT: Whitelist validation - only allow 'male' or 'female'
    if not gender:
        return False, "Gender cannot be empty"
    if len(gender) < 4 or len(gender) > 6:
        return False, "Gender must be 4-6 characters"
    if gender.lower() not in ['male', 'female']:
        return False, "Gender must be 'male' or 'female'"
    return True, "Valid gender"

def validate_city(city):
    # REQUIREMENT: Whitelist validation - only allow predefined cities
    if not city:
        return False, "City cannot be empty"
    if len(city) < 2 or len(city) > 50:
        return False, "City must be 2-50 characters"
    predefined_cities = [
        'Rotterdam', 'Amsterdam', 'Utrecht', 'The Hague', 'Eindhoven',
        'Tilburg', 'Groningen', 'Almere', 'Breda', 'Nijmegen'
    ]
    if city not in predefined_cities:
        return False, f"City must be one of: {', '.join(predefined_cities)}"
    return True, "Valid city"

def validate_serial_number(serial_num):
    # REQUIREMENT: Whitelist validation - only allow alphanumeric characters
    if not serial_num:
        return False, "Serial number cannot be empty"
    if len(serial_num) < 10 or len(serial_num) > 17:
        return False, "Serial number must be 10-17 characters"
    if not re.match(r'^[A-Za-z0-9]{10,17}$', serial_num):
        return False, "Serial number must be 10-17 alphanumeric characters"
    return True, "Valid serial number"

def validate_coordinates(latitude, longitude):
    # REQUIREMENT: Whitelist validation - only allow specific coordinate ranges
    if not latitude or not longitude:
        return False, "Coordinates cannot be empty"
    try:
        lat = float(latitude)
        lon = float(longitude)
        
        if not (51.8 <= lat <= 52.1) or not (4.2 <= lon <= 4.8):
            return False, "Coordinates must be within Rotterdam region"
        
        if len(str(lat).split('.')[-1]) > 5 or len(str(lon).split('.')[-1]) > 5:
            return False, "Coordinates must have maximum 5 decimal places"
        
        return True, "Valid coordinates"
    except ValueError:
        return False, "Invalid coordinate format"

def validate_maintenance_date(date_str):
    # REQUIREMENT: Whitelist validation - only allow YYYY-MM-DD format
    if not date_str:
        return False, "Maintenance date cannot be empty"
    if len(date_str) != 10:
        return False, "Maintenance date must be exactly 10 characters (YYYY-MM-DD)"
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True, "Valid maintenance date"
    except ValueError:
        return False, "Maintenance date must be in format YYYY-MM-DD"

def validate_numeric_input(value, min_val=None, max_val=None, field_name="value"):
    # REQUIREMENT: Whitelist validation - only allow valid numbers within ranges
    if not value:
        return False, f"{field_name} cannot be empty"
    try:
        num = float(value)
        if min_val is not None and num < min_val:
            return False, f"{field_name} must be at least {min_val}"
        if max_val is not None and num > max_val:
            return False, f"{field_name} must be at most {max_val}"
        return True, f"Valid {field_name}"
    except ValueError:
        return False, f"{field_name} must be a valid number"

def validate_first_name(first_name):
    # REQUIREMENT: Length checking - enforce 2-50 character limit
    if not first_name:
        return False, "First name cannot be empty"
    if len(first_name) < 2 or len(first_name) > 50:
        return False, "First name must be 2-50 characters"
    if not re.match(r'^[a-zA-Z\s\'-]+$', first_name):
        return False, "First name can only contain letters, spaces, apostrophes, and hyphens"
    return True, "Valid first name"

def validate_last_name(last_name):
    # REQUIREMENT: Length checking - enforce 2-50 character limit
    if not last_name:
        return False, "Last name cannot be empty"
    if len(last_name) < 2 or len(last_name) > 50:
        return False, "Last name must be 2-50 characters"
    if not re.match(r'^[a-zA-Z\s\'-]+$', last_name):
        return False, "Last name can only contain letters, spaces, apostrophes, and hyphens"
    return True, "Valid last name"

def validate_brand(brand):
    # REQUIREMENT: Length checking - enforce 2-50 character limit
    if not brand:
        return False, "Brand cannot be empty"
    if len(brand) < 2 or len(brand) > 50:
        return False, "Brand must be 2-50 characters"
    if not re.match(r'^[a-zA-Z0-9\s\-\.]+$', brand):
        return False, "Brand can only contain letters, numbers, spaces, hyphens, and dots"
    return True, "Valid brand"

def validate_model(model):
    # REQUIREMENT: Length checking - enforce 2-50 character limit
    if not model:
        return False, "Model cannot be empty"
    if len(model) < 2 or len(model) > 50:
        return False, "Model must be 2-50 characters"
    if not re.match(r'^[a-zA-Z0-9\s\-\.]+$', model):
        return False, "Model can only contain letters, numbers, spaces, hyphens, and dots"
    return True, "Valid model"

def validate_street_name(street_name):
    # REQUIREMENT: Length checking - enforce 2-100 character limit
    if not street_name:
        return False, "Street name cannot be empty"
    if len(street_name) < 2 or len(street_name) > 100:
        return False, "Street name must be 2-100 characters"
    if not re.match(r'^[a-zA-Z0-9\s\'-\.]+$', street_name):
        return False, "Street name can only contain letters, numbers, spaces, apostrophes, hyphens, and dots"
    return True, "Valid street name"

def validate_house_number(house_number):
    # REQUIREMENT: Length checking - enforce 1-10 character limit
    if not house_number:
        return False, "House number cannot be empty"
    if len(house_number) < 1 or len(house_number) > 10:
        return False, "House number must be 1-10 characters"
    if not re.match(r'^[a-zA-Z0-9\s\-]+$', house_number):
        return False, "House number can only contain letters, numbers, spaces, and hyphens"
    return True, "Valid house number"

def sanitize_input(input_str):
    if not input_str:
        return ""
    
    sanitized = input_str.replace('\x00', '').replace('\r', '').replace('\n', '')
    
    if len(sanitized) > 1000:
        sanitized = sanitized[:1000]
    
    return sanitized.strip()
