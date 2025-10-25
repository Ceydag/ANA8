import re
from validation import *

def get_validated_input(prompt, validation_func, error_message, max_attempts=3):
    attempts = 0
    while attempts < max_attempts:
        user_input = input(prompt).strip()
        
        if not user_input:
            print("Input cannot be empty. Please try again.")
            attempts += 1
            continue
        
        is_valid, message = validation_func(user_input)
        
        if is_valid:
            return user_input
        else:
            print(f"{message}")
            if attempts < max_attempts - 1:
                print(f"{error_message}")
            attempts += 1
    
    print(f"Maximum attempts ({max_attempts}) exceeded. Skipping this field.")
    return None

def validate_username_input(username):
    return validate_username(username)

def validate_password_input(password):
    return validate_password(password)

def validate_email_input(email):
    return validate_email(email)

def validate_phone_input(phone):
    return validate_phone(phone)

def validate_zip_code_input(zip_code):
    return validate_zip_code(zip_code)

def validate_driving_license_input(license_num):
    return validate_driving_license(license_num)

def validate_birthday_input(birthday):
    return validate_birthday(birthday)

def validate_gender_input(gender):
    return validate_gender(gender)

def validate_city_input(city):
    return validate_city(city)

def validate_serial_number_input(serial_num):
    return validate_serial_number(serial_num)

def validate_coordinates_input(latitude, longitude):
    return validate_coordinates(latitude, longitude)

def validate_maintenance_date_input(date_str):
    return validate_maintenance_date(date_str)

def get_first_name():
    return get_validated_input(
        "Enter first name: ",
        lambda x: (True, "") if x.strip() else (False, "First name cannot be empty"),
        "First name is required"
    )

def get_last_name():
    return get_validated_input(
        "Enter last name: ",
        lambda x: (True, "") if x.strip() else (False, "Last name cannot be empty"),
        "Last name is required"
    )

def get_username():
    return get_validated_input(
        "Enter username (8-10 characters, start with letter/underscore): ",
        validate_username_input,
        "Username must be 8-10 characters, start with letter or underscore, and contain only letters, numbers, underscores, apostrophes, and periods."
    )

def get_password():
    return get_validated_input(
        "Enter password (12-30 characters, must contain lowercase, uppercase, digit, and special character): ",
        validate_password_input,
        "Password must be 12-30 characters with at least one lowercase letter, one uppercase letter, one digit, and one special character."
    )

def get_email():
    return get_validated_input(
        "Enter email address: ",
        validate_email_input,
        "Please enter a valid email address (e.g., user@example.com)."
    )

def get_phone():
    return get_validated_input(
        "Enter mobile phone (8 digits, e.g., 0612345678): ",
        validate_phone_input,
        "Phone number must be exactly 8 digits (e.g., 0612345678)."
    )

def get_zip_code():
    return get_validated_input(
        "Enter zip code (DDDDXX format, e.g., 3011AB): ",
        validate_zip_code_input,
        "Zip code must be in format DDDDXX (4 digits, 2 uppercase letters, e.g., 3011AB)."
    )

def get_driving_license():
    return get_validated_input(
        "Enter driving license (XXDDDDDDD or XDDDDDDDD format): ",
        validate_driving_license_input,
        "Driving license must be in format XXDDDDDDD or XDDDDDDDD (2-3 letters followed by 7-8 digits)."
    )

def get_birthday():
    return get_validated_input(
        "Enter birthday (YYYY-MM-DD format, e.g., 1990-05-15): ",
        validate_birthday_input,
        "Birthday must be in format YYYY-MM-DD (e.g., 1990-05-15)."
    )

def get_gender():
    return get_validated_input(
        "Enter gender (male or female): ",
        validate_gender_input,
        "Gender must be either 'male' or 'female'."
    )

def get_city():
    cities = ['Rotterdam', 'Amsterdam', 'Utrecht', 'The Hague', 'Eindhoven',
              'Tilburg', 'Groningen', 'Almere', 'Breda', 'Nijmegen']
    print(f"Available cities: {', '.join(cities)}")
    return get_validated_input(
        "Enter city: ",
        validate_city_input,
        f"City must be one of: {', '.join(cities)}."
    )

def get_serial_number():
    return get_validated_input(
        "Enter serial number (10-17 alphanumeric characters): ",
        validate_serial_number_input,
        "Serial number must be 10-17 alphanumeric characters."
    )

def get_coordinates():
    print("Enter GPS coordinates for Rotterdam region:")
    
    while True:
        try:
            lat_input = input("Enter latitude (e.g., 51.9225): ").strip()
            lon_input = input("Enter longitude (e.g., 4.47917): ").strip()
            
            if not lat_input or not lon_input:
                print("Coordinates cannot be empty. Please try again.")
                continue
            
            is_valid, message = validate_coordinates_input(lat_input, lon_input)
            
            if is_valid:
                return float(lat_input), float(lon_input)
            else:
                print(f"{message}")
                print("Coordinates must be within Rotterdam region with maximum 5 decimal places.")
        except ValueError:
            print("Invalid number format. Please enter valid decimal numbers.")
        except KeyboardInterrupt:
            print("\nInput cancelled.")
            return None, None

def get_maintenance_date():
    return get_validated_input(
        "Enter last maintenance date (YYYY-MM-DD format): ",
        validate_maintenance_date_input,
        "Maintenance date must be in format YYYY-MM-DD (e.g., 2024-01-15)."
    )

def get_numeric_input(prompt, min_val=None, max_val=None, field_name="value"):
    while True:
        try:
            value = input(prompt).strip()
            if not value:
                print("Input cannot be empty. Please try again.")
                continue
            
            num_value = float(value)
            
            if min_val is not None and num_value < min_val:
                print(f"{field_name} must be at least {min_val}")
                continue
            
            if max_val is not None and num_value > max_val:
                print(f"{field_name} must be at most {max_val}")
                continue
            
            return num_value
            
        except ValueError:
            print(f"Invalid number format. Please enter a valid number for {field_name}.")
        except KeyboardInterrupt:
            print(f"\n Input cancelled for {field_name}.")
            return None


def validate_serial_number_input(serial_number):
    if not serial_number:
        return False, "Serial number cannot be empty"
    
    if len(serial_number) < 10 or len(serial_number) > 17:
        return False, "Serial number must be 10-17 characters long"
    
    if not re.match(r'^[A-Za-z0-9]+$', serial_number):
        return False, "Serial number must contain only letters and numbers"
    
    return True, "Valid serial number"

def get_serial_number():
    return get_validated_input(
        "Enter serial number (10-17 alphanumeric characters): ",
        validate_serial_number_input,
        "Serial number must be 10-17 alphanumeric characters (e.g., SG1234567890)."
    )

def validate_brand_input(brand):
    if not brand:
        return False, "Brand cannot be empty"
    
    if len(brand) < 2 or len(brand) > 50:
        return False, "Brand must be 2-50 characters long"
    
    if not re.match(r'^[A-Za-z0-9\s\-\.]+$', brand):
        return False, "Brand contains invalid characters"
    
    return True, "Valid brand"

def get_brand():
    return get_validated_input(
        "Enter brand (e.g., Segway, NIU): ",
        validate_brand_input,
        "Brand must be 2-50 characters with letters, numbers, spaces, hyphens, and dots only."
    )

def validate_model_input(model):
    if not model:
        return False, "Model cannot be empty"
    
    if len(model) < 2 or len(model) > 50:
        return False, "Model must be 2-50 characters long"
    
    if not re.match(r'^[A-Za-z0-9\s\-\.]+$', model):
        return False, "Model contains invalid characters"
    
    return True, "Valid model"

def get_model():
    return get_validated_input(
        "Enter model (e.g., Ninebot E25, N1S Pro): ",
        validate_model_input,
        "Model must be 2-50 characters with letters, numbers, spaces, hyphens, and dots only."
    )

def validate_top_speed_input(speed):
    try:
        speed_val = float(speed)
        if speed_val < 1 or speed_val > 100:
            return False, "Top speed must be between 1-100 km/h"
        return True, "Valid top speed"
    except ValueError:
        return False, "Top speed must be a valid number"

def get_top_speed():
    return get_validated_input(
        "Enter top speed (1-100 km/h): ",
        validate_top_speed_input,
        "Top speed must be between 1-100 km/h."
    )

def validate_battery_capacity_input(capacity):
    try:
        cap_val = float(capacity)
        if cap_val < 1 or cap_val > 10000:
            return False, "Battery capacity must be between 1-10000 Wh"
        return True, "Valid battery capacity"
    except ValueError:
        return False, "Battery capacity must be a valid number"

def get_battery_capacity():
    return get_validated_input(
        "Enter battery capacity (1-10000 Wh): ",
        validate_battery_capacity_input,
        "Battery capacity must be between 1-10000 Wh."
    )

def validate_state_of_charge_input(soc):
    try:
        soc_val = float(soc)
        if soc_val < 0 or soc_val > 100:
            return False, "State of charge must be between 0-100%"
        return True, "Valid state of charge"
    except ValueError:
        return False, "State of charge must be a valid number"

def get_state_of_charge():
    return get_validated_input(
        "Enter state of charge (0-100%): ",
        validate_state_of_charge_input,
        "State of charge must be between 0-100%."
    )

def validate_target_range_input(min_range, max_range):
    try:
        min_val = float(min_range)
        max_val = float(max_range)
        
        if min_val < 0 or min_val > 100:
            return False, "Minimum range must be between 0-100%"
        
        if max_val < 0 or max_val > 100:
            return False, "Maximum range must be between 0-100%"
        
        if min_val >= max_val:
            return False, "Minimum range must be less than maximum range"
        
        return True, "Valid target range"
    except ValueError:
        return False, "Target range must be valid numbers"

def get_target_range():
    while True:
        try:
            min_range = input("Enter minimum target range (0-100%): ").strip()
            max_range = input("Enter maximum target range (0-100%): ").strip()
            
            if not min_range or not max_range:
                print("Both values are required. Please try again.")
                continue
            
            is_valid, message = validate_target_range_input(min_range, max_range)
            
            if is_valid:
                return float(min_range), float(max_range)
            else:
                print(f"{message}")
                print("Minimum must be less than maximum, both between 0-100%.")
        except KeyboardInterrupt:
            print("\n Input cancelled.")
            return None, None

def validate_mileage_input(mileage):
    try:
        mileage_val = float(mileage)
        if mileage_val < 0 or mileage_val > 100000:
            return False, "Mileage must be between 0-100000 km"
        return True, "Valid mileage"
    except ValueError:
        return False, "Mileage must be a valid number"

def get_mileage():
    return get_validated_input(
        "Enter mileage (0-100000 km): ",
        validate_mileage_input,
        "Mileage must be between 0-100000 km."
    )

def get_boolean_input(prompt):
    while True:
        response = input(f"{prompt} (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        else:
            print("Please enter 'y' for yes or 'n' for no.")

def get_menu_choice(prompt, max_choice):
    while True:
        try:
            choice = input(prompt).strip()
            if not choice:
                print("Please enter a choice.")
                continue
            
            choice_num = int(choice)
            if 1 <= choice_num <= max_choice:
                return choice_num
            else:
                print(f"Please enter a number between 1 and {max_choice}.")
        except ValueError:
            print("Please enter a valid number.")
        except KeyboardInterrupt:
            print("\n Input cancelled.")
            return None
