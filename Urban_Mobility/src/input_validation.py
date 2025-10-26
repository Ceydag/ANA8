import re
from datetime import datetime
from system_logging import log_validation_failure, log_all_validation_attempts

class InputValidator:
    def __init__(self):
        self.PATTERNS = {
            'username': r'^[a-zA-Z_][a-zA-Z0-9_\'\.]{7,9}$',
            'password': r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[~!@#$%&_\-+=`|\\(){}\[\]:;\'<>,.?/])[A-Za-z\d~!@#$%&_\-+=`|\\(){}\[\]:;\'<>,.?/]{12,30}$',
            'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
            'phone': r'^\d{8}$',
            'zip_code': r'^\d{4}[A-Z]{2}$',
            'driving_license': r'^[A-Z]{1,2}\d{7,8}$',
            'date_iso': r'^\d{4}-\d{2}-\d{2}$',
            'name': r'^[a-zA-Z\s\'-]{2,50}$',
            'serial_number': r'^[A-Za-z0-9]{10,17}$',
            'brand_model': r'^[a-zA-Z0-9\s\-\.]{2,50}$',
            'street': r'^[a-zA-Z0-9\s\'-\.]{2,100}$',
            'house_number': r'^[a-zA-Z0-9\s\-]{1,10}$',
        }
    
        self.CITIES = ['Rotterdam', 'Amsterdam', 'Utrecht', 'The Hague', 'Eindhoven', 'Tilburg', 'Groningen', 'Almere', 'Breda', 'Nijmegen']
        self.GENDERS = ['male', 'female']
        
        self.RANGES = {
            'top_speed': (1, 100),
            'battery_capacity': (1, 10000),
            'state_of_charge': (0, 100),
            'mileage': (0, 100000)
        }
        
        self.COORDINATE_BOUNDS = {
            'latitude': (51.8, 52.1),
            'longitude': (4.2, 4.8)
        }

    def validate_pattern(self, value, pattern_type, field_name):
        if not value:
            return False, f"{field_name} cannot be empty"
        
        if '\x00' in value:
            return False, "Invalid characters detected"
            
        if len(value) > 1000:
            return False, "Input too long"
        
        if pattern_type not in self.PATTERNS:
            return False, f"Unknown validation pattern: {pattern_type}"
        
        if not re.match(self.PATTERNS[pattern_type], value):
            return False, f"Invalid {field_name} format"
        
        return True, f"Valid {field_name}"

    def validate_choice(self, value, choices, field_name):
        if not value:
            return False, f"{field_name} cannot be empty"
        
        if value not in choices:
            return False, f"{field_name} must be one of: {', '.join(choices)}"
        
        return True, f"Valid {field_name}"

    def validate_numeric_range(self, value, range_type, field_name):
        if not value:
            return False, f"{field_name} cannot be empty"
        
        try:
            num_value = float(value)
            min_val, max_val = self.RANGES.get(range_type, (None, None))
            
            if min_val is not None and num_value < min_val:
                return False, f"{field_name} must be at least {min_val}"
            
            if max_val is not None and num_value > max_val:
                return False, f"{field_name} must be at most {max_val}"
            
            return True, f"Valid {field_name}"
        except ValueError:
            return False, f"{field_name} must be a valid number"

    def validate_date(self, value, field_name):
        if not value:
            return False, f"{field_name} cannot be empty"
        
        is_valid, message = self.validate_pattern(value, 'date_iso', field_name)
        if not is_valid:
            return False, message
        
        try:
            date_obj = datetime.strptime(value, '%Y-%m-%d')
            if date_obj > datetime.now():
                return False, f"{field_name} cannot be in the future"
            return True, f"Valid {field_name}"
        except ValueError:
            return False, f"Invalid {field_name}"

    def validate_coordinates(self, latitude, longitude):
        if not latitude or not longitude:
            return False, "Coordinates cannot be empty"
        
        try:
            lat = float(latitude)
            lon = float(longitude)
            
            lat_min, lat_max = self.COORDINATE_BOUNDS['latitude']
            lon_min, lon_max = self.COORDINATE_BOUNDS['longitude']
            
            if not (lat_min <= lat <= lat_max) or not (lon_min <= lon <= lon_max):
                return False, "Coordinates must be within Rotterdam region"
            
            if len(str(lat).split('.')[-1]) > 5 or len(str(lon).split('.')[-1]) > 5:
                return False, "Coordinates must have maximum 5 decimal places"
            
            return True, "Valid coordinates"
        except ValueError:
            return False, "Invalid coordinate format"



    def validate_target_range(self, min_range, max_range):
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


class InputCollector:
    def __init__(self):
        self.validator = InputValidator()

    def get_validated_input(self, prompt, validation_func, error_message, max_attempts=3, username="unknown", field_name="unknown"):
        attempts = 0
        while attempts < max_attempts:
            user_input = input(prompt).strip()
            
            if not user_input:
                log_validation_failure(username, field_name, user_input, "Empty input")
                print("Input cannot be empty. Please try again.")
                attempts += 1
                continue
            
            # Check for suspicious input attempts (SQL injection, XSS, path traversal, etc.)
            from system_logging import detect_suspicious_input
            if detect_suspicious_input(user_input):
                # Log as suspicious activity and terminate session
                from session_management import handle_suspicious_activity
                terminate_session, termination_message = handle_suspicious_activity(username, f"Suspicious input detected in {field_name}: {user_input}")
                log_validation_failure(username, field_name, user_input, f"SUSPICIOUS: Malicious input pattern detected")
                print("Bad input. Incident logged.")
                # Exit the program immediately
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
            lambda x: self.validator.validate_pattern(x, 'name', 'first name'),
            "First name must be 2-50 characters with letters, spaces, apostrophes, and hyphens only",
            username=username,
            field_name=field_name
        )

    def get_last_name(self, username="unknown", field_name="last_name"):
        return self.get_validated_input(
            "Enter last name: ",
            lambda x: self.validator.validate_pattern(x, 'name', 'last name'),
            "Last name must be 2-50 characters with letters, spaces, apostrophes, and hyphens only",
            username=username,
            field_name=field_name
        )

    def get_street_name(self, username="unknown", field_name="street_name"):
        return self.get_validated_input(
            "Enter street name: ",
            lambda x: self.validator.validate_pattern(x, 'street', 'street name'),
            "Street name must be 2-100 characters with letters, numbers, spaces, apostrophes, hyphens, and periods only",
            username=username,
            field_name=field_name
        )

    def get_house_number(self, username="unknown", field_name="house_number"):
        return self.get_validated_input(
            "Enter house number: ",
            lambda x: self.validator.validate_pattern(x, 'house_number', 'house number'),
            "House number must be 1-10 characters with letters, numbers, spaces, and hyphens only",
            username=username,
            field_name=field_name
        )

    def get_username(self):
        return self.get_validated_input(
            "Enter username (8-10 characters, start with letter/underscore): ",
            lambda x: self.validator.validate_pattern(x, 'username', 'username'),
            "Username must be 8-10 characters, start with letter or underscore, and contain only letters, numbers, underscores, apostrophes, and periods."
        )

    def get_password(self):
        return self.get_validated_input(
            "Enter password (12-30 characters, must contain lowercase, uppercase, digit, and special character): ",
            lambda x: self.validator.validate_pattern(x, 'password', 'password'),
            "Password must be 12-30 characters with at least one lowercase letter, one uppercase letter, one digit, and one special character."
        )

    def get_email(self):
        return self.get_validated_input(
            "Enter email address: ",
            lambda x: self.validator.validate_pattern(x, 'email', 'email'),
            "Please enter a valid email address (e.g., user@example.com)."
        )

    def get_phone(self):
        return self.get_validated_input(
            "Enter mobile phone (8 digits, e.g., 0612345678): ",
            lambda x: self.validator.validate_pattern(x, 'phone', 'phone number'),
            "Phone number must be exactly 8 digits (e.g., 0612345678)."
        )

    def get_zip_code(self):
        return self.get_validated_input(
            "Enter zip code (DDDDXX format, e.g., 3011AB): ",
            lambda x: self.validator.validate_pattern(x, 'zip_code', 'zip code'),
            "Zip code must be in format DDDDXX (4 digits, 2 uppercase letters, e.g., 3011AB)."
        )

    def get_driving_license(self):
        return self.get_validated_input(
            "Enter driving license (XXDDDDDDD or XDDDDDDDD format): ",
            lambda x: self.validator.validate_pattern(x, 'driving_license', 'driving license'),
            "Driving license must be in format XXDDDDDDD or XDDDDDDDD (2-3 letters followed by 7-8 digits)."
        )

    def get_birthday(self):
        return self.get_validated_input(
            "Enter birthday (YYYY-MM-DD format, e.g., 1990-05-15): ",
            lambda x: self.validator.validate_date(x, 'birthday'),
            "Birthday must be in format YYYY-MM-DD (e.g., 1990-05-15)."
        )

    def get_gender(self):
        return self.get_validated_input(
            "Enter gender (male or female): ",
            lambda x: self.validator.validate_choice(x, self.validator.GENDERS, 'gender'),
            "Gender must be either 'male' or 'female'."
        )

    def get_city(self):
        print(f"Available cities: {', '.join(self.validator.CITIES)}")
        return self.get_validated_input(
            "Enter city: ",
            lambda x: self.validator.validate_choice(x, self.validator.CITIES, 'city'),
            f"City must be one of: {', '.join(self.validator.CITIES)}."
        )

    def get_serial_number(self):
        return self.get_validated_input(
            "Enter serial number (10-17 alphanumeric characters): ",
            lambda x: self.validator.validate_pattern(x, 'serial_number', 'serial number'),
            "Serial number must be 10-17 alphanumeric characters."
        )

    def get_maintenance_date(self):
        return self.get_validated_input(
            "Enter last maintenance date (YYYY-MM-DD format): ",
            lambda x: self.validator.validate_date(x, 'maintenance date'),
            "Maintenance date must be in format YYYY-MM-DD (e.g., 2024-01-15)."
        )

    def get_brand(self):
        return self.get_validated_input(
            "Enter brand (e.g., Segway, NIU): ",
            lambda x: self.validator.validate_pattern(x, 'brand_model', 'brand'),
            "Brand must be 2-50 characters with letters, numbers, spaces, hyphens, and dots only."
        )

    def get_model(self):
        return self.get_validated_input(
            "Enter model (e.g., Ninebot E25, N1S Pro): ",
            lambda x: self.validator.validate_pattern(x, 'brand_model', 'model'),
            "Model must be 2-50 characters with letters, numbers, spaces, hyphens, and dots only."
        )

    def get_top_speed(self):
        return self.get_validated_input(
            "Enter top speed (1-100 km/h): ",
            lambda x: self.validator.validate_numeric_range(x, 'top_speed', 'top speed'),
            "Top speed must be between 1-100 km/h."
        )

    def get_battery_capacity(self):
        return self.get_validated_input(
            "Enter battery capacity (1-10000 Wh): ",
            lambda x: self.validator.validate_numeric_range(x, 'battery_capacity', 'battery capacity'),
            "Battery capacity must be between 1-10000 Wh."
        )

    def get_state_of_charge(self):
        return self.get_validated_input(
            "Enter state of charge (0-100%): ",
            lambda x: self.validator.validate_numeric_range(x, 'state_of_charge', 'state of charge'),
            "State of charge must be between 0-100%."
        )

    def get_mileage(self):
        return self.get_validated_input(
            "Enter mileage (0-100000 km): ",
            lambda x: self.validator.validate_numeric_range(x, 'mileage', 'mileage'),
            "Mileage must be between 0-100000 km."
        )

    def get_coordinates(self, username="unknown", field_name="coordinates"):
        """✅ C4 L3: Specialized input with custom validation"""
        print("Enter GPS coordinates for Rotterdam region:")
        
        while True:
            try:
                lat_input = input("Enter latitude (e.g., 51.9225): ").strip()
                lon_input = input("Enter longitude (e.g., 4.47917): ").strip()
                
                if not lat_input or not lon_input:
                    print("Coordinates cannot be empty. Please try again.")
                    continue
                
                # Check for suspicious input
                from system_logging import detect_suspicious_input
                if detect_suspicious_input(lat_input) or detect_suspicious_input(lon_input):
                    from session_management import handle_suspicious_activity
                    handle_suspicious_activity(username, f"Suspicious input detected in {field_name}: {lat_input}, {lon_input}")
                    print("Bad input. Incident logged.")
                    import sys
                    sys.exit(0)
                
                is_valid, message = self.validator.validate_coordinates(lat_input, lon_input)
                
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
                min_range = input("Enter minimum target range (0-100%): ").strip()
                max_range = input("Enter maximum target range (0-100%): ").strip()
                
                if not min_range or not max_range:
                    print("Both values are required. Please try again.")
                    continue
                
                # Check for suspicious input
                from system_logging import detect_suspicious_input
                if detect_suspicious_input(min_range) or detect_suspicious_input(max_range):
                    from session_management import handle_suspicious_activity
                    handle_suspicious_activity(username, f"Suspicious input detected in {field_name}: {min_range}, {max_range}")
                    print("Bad input. Incident logged.")
                    import sys
                    sys.exit(0)
                
                is_valid, message = self.validator.validate_target_range(min_range, max_range)
                
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
                print(f"\nInput cancelled for {field_name}.")
                return None

    def get_boolean_input(self, prompt, username="unknown", field_name="boolean_input"):
        while True:
            response = input(f"{prompt} (y/n): ").strip().lower()
            
            # Check for suspicious input
            from system_logging import detect_suspicious_input
            if detect_suspicious_input(response):
                from session_management import handle_suspicious_activity
                terminate_session, termination_message = handle_suspicious_activity(username, f"Suspicious input detected in {field_name}: {response}")
                print("Bad input. Incident logged.")
                import sys
                sys.exit(0)
            
            if response in ['y', 'yes']:
                return True
            elif response in ['n', 'no']:
                return False
            else:
                print("Please enter 'y' for yes or 'n' for no.")

    def get_menu_choice(self, prompt, max_choice, username="unknown", field_name="menu_choice"):
        while True:
            try:
                choice = input(prompt).strip()
                if not choice:
                    print("Please enter a choice.")
                    continue
                
                # Check for suspicious input
                from system_logging import detect_suspicious_input
                if detect_suspicious_input(choice):
                    from session_management import handle_suspicious_activity
                    terminate_session, termination_message = handle_suspicious_activity(username, f"Suspicious input detected in {field_name}: {choice}")
                    print("Bad input. Incident logged.")
                    import sys
                    sys.exit(0)
                
                choice_num = int(choice)
                if 1 <= choice_num <= max_choice:
                    return choice_num
                else:
                    print(f"Please enter a number between 1 and {max_choice}.")
            except ValueError:
                print("Please enter a valid number.")



validator = InputValidator()
collector = InputCollector()