import re
from datetime import datetime
from system_logging import log_validation_failure, log_all_validation_attempts

def is_valid(value, pattern):
    return re.match(pattern, value) and "\x00" not in value

def check_basic_validation(value, field_name="value"):
    if not value:
        return False, f"{field_name} cannot be empty"
    if "\x00" in value:
        return False, "Invalid characters detected"
    return None

def validate_username(username):
    error = check_basic_validation(username, "Username")
    if error:
        return error
    pattern = r"^(?!.*[_.]{2})[a-zA-Z_](?:[\w.\'-]{7,9})$"
    if is_valid(username, pattern):
        return True, "Valid username"
    return False, "Invalid username format"

def validate_password(password):
    error = check_basic_validation(password, "Password")
    if error:
        return error
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[~!@#$%&_\-+=`|\\(){}[\]:;\'<>,.?/])[A-Za-z\d~!@#$%&_\-+=`|\\(){}[\]:;\'<>,.?/]{12,30}$"
    if is_valid(password, pattern):
        return True, "Valid password"
    return False, "Invalid password format"

def validate_name(name):
    error = check_basic_validation(name, "Name")
    if error:
        return error
    pattern = r"^[a-zA-Z]{2,20}$"
    if is_valid(name, pattern):
        return True, "Valid name"
    return False, "Invalid name format"

def validate_email(email):
    error = check_basic_validation(email, "Email")
    if error:
        return error
    pattern = r"^[a-zA-Z0-9_.+-]{1,64}@[a-zA-Z0-9-]{1,255}\.[a-zA-Z]{2,24}$"
    if is_valid(email, pattern):
        return True, "Valid email"
    return False, "Invalid email format"

def validate_phone_number(phone_number):
    error = check_basic_validation(phone_number, "Phone number")
    if error:
        return error
    pattern = r"^\d{8}$"
    if is_valid(phone_number, pattern):
        return True, "Valid phone number"
    return False, "Invalid phone number format"

def validate_street_name(street_name):
    error = check_basic_validation(street_name, "Street name")
    if error:
        return error
    pattern = r"^[a-zA-Z0-9\s]{2,30}$"
    if is_valid(street_name, pattern):
        return True, "Valid street name"
    return False, "Invalid street name format"

def validate_house_number(house_number):
    error = check_basic_validation(house_number, "House number")
    if error:
        return error
    pattern = r"^[1-9][0-9]{0,3}[a-zA-Z]{0,1}$"
    if is_valid(house_number, pattern):
        return True, "Valid house number"
    return False, "Invalid house number format"

def validate_zip_code(zip_code):
    error = check_basic_validation(zip_code, "Zip code")
    if error:
        return error
    pattern = r"^[1-9][0-9]{3}\s?[a-zA-Z]{2}$"
    if is_valid(zip_code, pattern):
        return True, "Valid zip code"
    return False, "Invalid zip code format"

def validate_driving_license(driving_license):
    error = check_basic_validation(driving_license, "Driving license")
    if error:
        return error
    pattern = r"^[A-Z]{1,2}\d{7,8}$"
    if is_valid(driving_license, pattern):
        return True, "Valid driving license"
    return False, "Invalid driving license format"

def validate_serial_number(serial_number):
    error = check_basic_validation(serial_number, "Serial number")
    if error:
        return error
    pattern = r"^[A-Za-z0-9]{10,17}$"
    if is_valid(serial_number, pattern):
        return True, "Valid serial number"
    return False, "Invalid serial number format"

def validate_brand_model(brand_model):
    error = check_basic_validation(brand_model, "Brand/model")
    if error:
        return error
    pattern = r"^[a-zA-Z0-9\s\-\.]{2,50}$"
    if is_valid(brand_model, pattern):
        return True, "Valid brand/model"
    return False, "Invalid brand/model format"

def validate_top_speed(top_speed):
    error = check_basic_validation(top_speed, "Top speed")
    if error:
        return error
    pattern = r"^(?:[1-9][0-9]?|100)$"
    if is_valid(top_speed, pattern):
        return True, "Valid top speed"
    return False, "Invalid top speed format"

def validate_battery_capacity(battery_capacity):
    error = check_basic_validation(battery_capacity, "Battery capacity")
    if error:
        return error
    pattern = r"^(?:[1-9][0-9]{0,3}|10000)$"
    if is_valid(battery_capacity, pattern):
        return True, "Valid battery capacity"
    return False, "Invalid battery capacity format"

def validate_state_of_charge(state_of_charge):
    error = check_basic_validation(state_of_charge, "State of charge")
    if error:
        return error
    pattern = r"^(?:[0-9]|[1-9][0-9]|100)$"
    if is_valid(state_of_charge, pattern):
        return True, "Valid state of charge"
    return False, "Invalid state of charge format"

def validate_mileage(mileage):
    error = check_basic_validation(mileage, "Mileage")
    if error:
        return error
    pattern = r"^(?:[0-9]|[1-9][0-9]{1,4}|100000)$"
    if is_valid(mileage, pattern):
        return True, "Valid mileage"
    return False, "Invalid mileage format"

from datetime import datetime

def validate_date(value):
    error = check_basic_validation(value, "Date")
    if error:
        return error
    
    pattern = r"^\d{4}-\d{2}-\d{2}$"
    if not is_valid(value, pattern):
        return False, "Invalid date format. Must be YYYY-MM-DD"
    
    try:
        date_obj = datetime.strptime(value, '%Y-%m-%d').date()
        current_date = datetime.now().date()
        if date_obj.year < 1930:
            return False, "Date must be 1930 or later"
        if date_obj > current_date:
            return False, "Date cannot be in the future"
        return True, "Valid date"
    except ValueError:
        return False, "Invalid date"

def validate_coordinates(latitude, longitude):
    if not latitude or not longitude:
        return False, "Coordinates cannot be empty"
    error = check_basic_validation(latitude)
    if error:
        return error
    error = check_basic_validation(longitude)
    if error:
        return error
    lat_pattern = r'^(?:51\.(?:[89]\d{0,4})|52\.(?:[01]\d{0,4}))$'
    lon_pattern = r'^4\.(?:[2-8]\d{0,4})$'
    if not is_valid(latitude, lat_pattern) or not is_valid(longitude, lon_pattern):
        return False, "Coordinates must be within Rotterdam region and have valid format"
    return True, "Valid coordinates"

def validate_target_range(min_range, max_range):
    if not min_range or not max_range:
        return False, "Range values cannot be empty"
    error = check_basic_validation(min_range)
    if error:
        return error
    error = check_basic_validation(max_range)
    if error:
        return error
    percent_pattern = r'^(?:[0-9]|[1-9][0-9]|100)$'
    if not is_valid(min_range, percent_pattern) or not is_valid(max_range, percent_pattern):
        return False, "Range values must be valid numbers between 0-100"
    if int(min_range) >= int(max_range):
        return False, "Minimum range must be less than maximum range"
    return True, "Valid target range"

def validate_choice(value, choices):
    error = check_basic_validation(value, "Choice")
    if error:
        return error
    if value in choices:
        return True, "Valid choice"
    return False, f"Choice must be one of: {', '.join(choices)}"

def create_range_pattern(min_val, max_val):
    if min_val is None and max_val is None:
        return None
    
    if min_val is not None and max_val is not None:
        min_str = str(min_val)
        max_str = str(max_val)
        
        if min_val == 0 and max_val < 10:
            return f'^[0-{max_val}]$'
        elif min_val > 0 and max_val < 10:
            return f'^[{min_val}-{max_val}]$'
        elif min_val == 0 and max_val < 100:
            return f'^(?:[0-9]|[1-9][0-9]|{max_val})$'
        elif min_val > 0 and max_val < 100:
            if min_val < 10:
                return f'^(?:[{min_val}-9]|[1-9][0-9]|{max_val})$'
            else:
                return f'^(?:{min_str}|[1-9][0-9]|{max_str})$'
        else:
            return f'^(?:{min_str}|[1-9]\\d+|{max_str})$'
    
    return None

CITIES = ['Rotterdam', 'Amsterdam', 'Utrecht', 'The Hague', 'Eindhoven', 'Tilburg', 'Groningen', 'Almere', 'Breda', 'Nijmegen']
GENDERS = ['male', 'female']

class InputCollector:

    def get_validated_input(self, prompt, validation_func, error_message, max_attempts=3, username="unknown", field_name="unknown"):
        attempts = 0
        while attempts < max_attempts:
            user_input = input(prompt)
            
            if not user_input:
                log_validation_failure(username, field_name, user_input, "Empty input")
                print("Input cannot be empty. Please try again.")
                attempts += 1
                continue
            
            from system_logging import detect_suspicious_input
            if detect_suspicious_input(user_input, field_name):
                from session_management import handle_suspicious_activity
                terminate_session, termination_message = handle_suspicious_activity(username, f"Suspicious input detected in {field_name}: {user_input}")
                log_validation_failure(username, field_name, user_input, f"SUSPICIOUS: Malicious input pattern detected")
                print("Bad input. Incident logged.")
                import sys
                sys.exit(0)
            
            is_valid, message = validation_func(user_input)
            
            if is_valid:
                log_all_validation_attempts(username, field_name, user_input, True, "Validation successful")
                return user_input
            else:
                log_validation_failure(username, field_name, user_input, message)
                print(f"{message}")
                if attempts < max_attempts - 1:
                    print(f"{error_message}")
                attempts += 1
        
        log_all_validation_attempts(username, field_name, user_input, False, f"Max attempts ({max_attempts}) exceeded")
        print(f"Maximum attempts ({max_attempts}) exceeded. Skipping this field.")
        return None

    def get_first_name(self, username="unknown", field_name="first_name"):
        return self.get_validated_input(
            "Enter first name: ",
            validate_name,
            "First name must be 2-20 characters with letters only",
            username=username,
            field_name=field_name
        )

    def get_last_name(self, username="unknown", field_name="last_name"):
        return self.get_validated_input(
            "Enter last name: ",
            validate_name,
            "Last name must be 2-20 characters with letters only",
            username=username,
            field_name=field_name
        )

    def get_street_name(self, username="unknown", field_name="street_name"):
        return self.get_validated_input(
            "Enter street name: ",
            validate_street_name,
            "Street name must be 2-30 characters with letters, numbers, and spaces only",
            username=username,
            field_name=field_name
        )

    def get_house_number(self, username="unknown", field_name="house_number"):
        return self.get_validated_input(
            "Enter house number: ",
            validate_house_number,
            "House number must be 1-4 digits optionally followed by one letter",
            username=username,
            field_name=field_name
        )

    def get_username(self):
        return self.get_validated_input(
            "Enter username (8-10 characters, start with letter/underscore): ",
            validate_username,
            "Username must be 8-10 characters, start with letter or underscore, and contain only letters, numbers, underscores, apostrophes, and periods."
        )

    def get_password(self):
        return self.get_validated_input(
            "Enter password (12-30 characters, must contain lowercase, uppercase, digit, and special character): ",
            validate_password,
            "Password must be 12-30 characters with at least one lowercase letter, one uppercase letter, one digit, and one special character."
        )

    def get_email(self):
        return self.get_validated_input(
            "Enter email address: ",
            validate_email,
            "Please enter a valid email address (e.g., user@example.com)."
        )

    def get_phone(self):
        return self.get_validated_input(
            "Enter mobile phone (8 digits, e.g., 12345678): ",
            validate_phone_number,
            "Phone number must be exactly 8 digits (e.g., 12345678)."
        )

    def get_zip_code(self):
        return self.get_validated_input(
            "Enter zip code (DDDDXX format, e.g., 3011AB): ",
            validate_zip_code,
            "Zip code must be in format DDDDXX (4 digits, 2 uppercase letters, e.g., 3011AB)."
        )

    def get_driving_license(self):
        return self.get_validated_input(
            "Enter driving license (DDXXXXXXX or DXXXXXXXX format): ",
            validate_driving_license,
            "Driving license must be in format DDXXXXXXX or DXXXXXXXX (2-3 letters followed by 7-8 digits)."
        )

    def get_birthday(self):
        return self.get_validated_input(
            "Enter birthday (YYYY-MM-DD format, e.g., 1990-05-15): ",
            validate_date,
            "Birthday must be in format YYYY-MM-DD (e.g., 1990-05-15)."
        )

    def get_gender(self):
        return self.get_validated_input(
            "Enter gender (male or female): ",
            lambda x: validate_choice(x, GENDERS),
            "Gender must be either 'male' or 'female'."
        )

    def get_city(self):
        print(f"Available cities: {', '.join(CITIES)}")
        return self.get_validated_input(
            "Enter city: ",
            lambda x: validate_choice(x, CITIES),
            f"City must be one of: {', '.join(CITIES)}."
        )

    def get_serial_number(self):
        return self.get_validated_input(
            "Enter serial number (10-17 alphanumeric characters): ",
            validate_serial_number,
            "Serial number must be 10-17 alphanumeric characters."
        )

    def get_maintenance_date(self):
        return self.get_validated_input(
            "Enter last maintenance date (YYYY-MM-DD format): ",
            validate_date,
            "Maintenance date must be in format YYYY-MM-DD (e.g., 2024-01-15)."
        )

    def get_brand(self):
        return self.get_validated_input(
            "Enter brand (e.g., Segway, NIU): ",
            validate_brand_model,
            "Brand must be 2-50 characters with letters, numbers, spaces, hyphens, and dots only."
        )

    def get_model(self):
        return self.get_validated_input(
            "Enter model (e.g., Ninebot E25, N1S Pro): ",
            validate_brand_model,
            "Model must be 2-50 characters with letters, numbers, spaces, hyphens, and dots only."
        )

    def get_top_speed(self):
        return self.get_validated_input(
            "Enter top speed (1-100 km/h): ",
            validate_top_speed,
            "Top speed must be between 1-100 km/h."
        )

    def get_battery_capacity(self):
        return self.get_validated_input(
            "Enter battery capacity (1-10000 Wh): ",
            validate_battery_capacity,
            "Battery capacity must be between 1-10000 Wh."
        )

    def get_state_of_charge(self):
        return self.get_validated_input(
            "Enter state of charge (0-100%): ",
            validate_state_of_charge,
            "State of charge must be between 0-100%."
        )

    def get_mileage(self):
        return self.get_validated_input(
            "Enter mileage (0-100000 km): ",
            validate_mileage,
            "Mileage must be between 0-100000 km."
        )

    def get_coordinates(self, username="unknown", field_name="coordinates"):
        print("Enter GPS coordinates for Rotterdam region:")
        
        while True:
            try:
                lat_input = input("Enter latitude (e.g., 51.9225): ")
                lon_input = input("Enter longitude (e.g., 4.47917): ")
                
                if not lat_input or not lon_input:
                    print("Coordinates cannot be empty. Please try again.")
                    continue
                
                from system_logging import detect_suspicious_input
                if detect_suspicious_input(lat_input, field_name) or detect_suspicious_input(lon_input, field_name):
                    from session_management import handle_suspicious_activity
                    handle_suspicious_activity(username, f"Suspicious input detected in {field_name}: {lat_input}, {lon_input}")
                    print("Bad input. Incident logged.")
                    import sys
                    sys.exit(0)
                
                is_valid, message = validate_coordinates(lat_input, lon_input)
                
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

    def get_target_range(self, username="unknown", field_name="target_range"):
        while True:
            try:
                min_range = input("Enter minimum target range (0-100%): ")
                max_range = input("Enter maximum target range (0-100%): ")
                
                if not min_range or not max_range:
                    print("Both values are required. Please try again.")
                    continue
                
                from system_logging import detect_suspicious_input
                if detect_suspicious_input(min_range, field_name) or detect_suspicious_input(max_range, field_name):
                    from session_management import handle_suspicious_activity
                    handle_suspicious_activity(username, f"Suspicious input detected in {field_name}: {min_range}, {max_range}")
                    print("Bad input. Incident logged.")
                    import sys
                    sys.exit(0)
                
                is_valid, message = validate_target_range(min_range, max_range)
                
                if is_valid:
                    return float(min_range), float(max_range)
                else:
                    print(f"{message}")
                    print("Minimum must be less than maximum, both between 0-100%.")
            except KeyboardInterrupt:
                print("\nInput cancelled.")
                return None, None

    def get_numeric_input(self, prompt, min_val=None, max_val=None, field_name="value"):
        while True:
            try:
                value = input(prompt)
                
                error = check_basic_validation(value, field_name)
                if error:
                    print(f"{error[1]}. Please try again.")
                    continue
                
                numeric_pattern = r'^-?(?:\d+\.?\d*|\.\d+)$'
                if not is_valid(value, numeric_pattern):
                    print(f"Invalid number format. Please enter a valid number for {field_name}.")
                    continue
                
                if min_val is not None or max_val is not None:
                    range_pattern = create_range_pattern(min_val, max_val)
                    if range_pattern and not is_valid(value, range_pattern):
                        if min_val is not None and max_val is not None:
                            print(f"{field_name} must be between {min_val} and {max_val}")
                        elif min_val is not None:
                            print(f"{field_name} must be at least {min_val}")
                        else:
                            print(f"{field_name} must be at most {max_val}")
                        continue
                
                return value
                
            except KeyboardInterrupt:
                print(f"\nInput cancelled for {field_name}.")
                return None

    def get_boolean_input(self, prompt, username="unknown", field_name="boolean_input"):
        while True:
            response = input(f"{prompt} (y/n): ")
            
            from system_logging import detect_suspicious_input
            if detect_suspicious_input(response, field_name):
                from session_management import handle_suspicious_activity
                terminate_session, termination_message = handle_suspicious_activity(username, f"Suspicious input detected in {field_name}: {response}")
                print("Bad input. Incident logged.")
                import sys
                sys.exit(0)
            
            if response in ['y', 'yes', 'Y', 'YES', 'Yes']:
                return True
            elif response in ['n', 'no', 'N', 'NO', 'No']:
                return False
            else:
                print("Please enter 'y' for yes or 'n' for no.")

    def get_menu_choice(self, prompt, max_choice, username="unknown", field_name="menu_choice"):
        while True:
            try:
                choice = input(prompt)
                if not choice:
                    print("Please enter a choice.")
                    continue
                
                from system_logging import detect_suspicious_input
                if detect_suspicious_input(choice, field_name):
                    from session_management import handle_suspicious_activity
                    terminate_session, termination_message = handle_suspicious_activity(username, f"Suspicious input detected in {field_name}: {choice}")
                    print("Bad input. Incident logged.")
                    import sys
                    sys.exit(0)
                
                choice_pattern = create_range_pattern(1, max_choice)
                if choice_pattern:
                    if not is_valid(choice, choice_pattern):
                        print(f"Please enter a number between 1 and {max_choice}.")
                        continue
                else:
                    numeric_pattern = r'^\d+$'
                    if not is_valid(choice, numeric_pattern):
                        print("Please enter a valid number.")
                        continue
                    if not (1 <= int(choice) <= max_choice):
                        print(f"Please enter a number between 1 and {max_choice}.")
                        continue
                
                return int(choice)
            except ValueError:
                print("Please enter a valid number.")


collector = InputCollector()
def validate_pattern(value, pattern_type, field_name):
    validators = {
        'username': validate_username,
        'password': validate_password,
        'email': validate_email,
        'phone': validate_phone_number,
        'zip_code': validate_zip_code,
        'driving_license': validate_driving_license,
        'date_iso': lambda x: validate_date(x),
        'name': validate_name,
        'serial_number': validate_serial_number,
        'brand_model': validate_brand_model,
        'street': validate_street_name,
        'house_number': validate_house_number,
    }
    
    if pattern_type not in validators:
        return False, f"Unknown validation pattern: {pattern_type}"
    
    return validators[pattern_type](value)

def validate_numeric_range(value, range_type, field_name):
    validators = {
        'top_speed': validate_top_speed,
        'battery_capacity': validate_battery_capacity,
        'state_of_charge': validate_state_of_charge,
        'mileage': validate_mileage,
    }
    
    if range_type not in validators:
        return False, f"Unknown range type: {range_type}"
    
    return validators[range_type](value)

class ValidatorCompat:
    def validate_pattern(self, value, pattern_type, field_name):
        return validate_pattern(value, pattern_type, field_name)
    
    def validate_choice(self, value, choices, field_name):
        return validate_choice(value, choices)
    
    def validate_numeric_range(self, value, range_type, field_name):
        return validate_numeric_range(value, range_type, field_name)
    
    def validate_date(self, value, field_name):
        return validate_date(value)
    
    def validate_coordinates(self, latitude, longitude):
        return validate_coordinates(latitude, longitude)
    
    def validate_target_range(self, min_range, max_range):
        return validate_target_range(min_range, max_range)
    
    GENDERS = GENDERS
    CITIES = CITIES

validator = ValidatorCompat()
