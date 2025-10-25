import os
import sys
from database import initialize_db
from authentication import login, change_password, logout_user
from session_management import check_session, display_session_info, handle_invalid_input, handle_suspicious_activity
from error_handler import handle_exception, handle_keyboard_interrupt, handle_database_error
from system_logging import log_action, check_suspicious_activities, get_logs, get_suspicious_logs
from backup import create_backup, generate_restore_code, restore_backup, list_backups, revoke_restore_code, list_restore_codes
from crud_operations import *
from input_validation import *

def exit_system(username):
    print("\nExiting Urban Mobility Backend System...")
    log_action(username, "System exit")
    print("Thank you for using Urban Mobility Backend System!")
    sys.exit(0)

def main():
    print("=" * 60)
    print("    URBAN MOBILITY BACKEND SYSTEM")
    print("    Secure Scooter Network Management")
    print("=" * 60)
   
    initialize_db()
    
    username, role = login()
    if not username:
        print("Login failed. Exiting system.")
        return
    
    suspicious_count = check_suspicious_activities()
    if suspicious_count > 0:
        print(f"\n ALERT: {suspicious_count} suspicious activities detected in the last 24 hours!")
        print("Please review the logs for details.")
    
    log_action(username, "Logged in successfully")
    
    while True:
        try:
            if role == "Super Admin":
                result = super_admin_menu(username)
                if result == "logout":
                    print("Logging out...")
                    break
            elif role == "System Admin":
                result = system_admin_menu(username)
                if result == "logout":
                    print("Logging out...")
                    break
            elif role == "Service Engineer":
                result = service_engineer_menu(username)
                if result == "logout":
                    print("Logging out...")
                    break
            else:
                print("Invalid role. Exiting system.")
                break
        except KeyboardInterrupt:
            exit_system(username)
        except Exception as e:
            print(f"An error occurred: {e}")
            log_action(username, f"System error: {e}", suspicious=True)

def super_admin_menu(username):
    # REQUIREMENT: Session management - check session validity
    is_valid, message = check_session(username)
    if not is_valid:
        print(f"Session error: {message}")
        return "logout"
    
    # Check for suspicious activities and display alert
    from system_logging import display_alert_if_suspicious
    display_alert_if_suspicious()
    
    # REQUIREMENT: Session management - display session info
    display_session_info(username)
    
    while True:
        print("\n" + "=" * 50)
        print("    SUPER ADMIN MENU")
        print("=" * 50)
        print("1.  Manage System Administrators")
        print("2.  Manage Service Engineers")
        print("3.  Manage Travellers")
        print("4.  Manage Scooters")
        print("5.  View System Logs")
        print("6.  Create Backup")
        print("7.  Generate Restore Code")
        print("8.  Revoke Restore Code")
        print("9.  List Restore Codes")
        print("10. View All Users")
        print("11. Logout")
        print("12. Exit System")
        print("-" * 50)
        
        choice = input("Enter your choice (1-12): ").strip()
        
        if choice == "1":
            manage_system_admins(username)
        elif choice == "2":
            manage_service_engineers(username)
        elif choice == "3":
            manage_travellers(username)
        elif choice == "4":
            manage_scooters(username)
        elif choice == "5":
            view_logs(username)
        elif choice == "6":
            create_backup()
        elif choice == "7":
            generate_restore_code_menu(username)
        elif choice == "8":
            revoke_restore_code_menu(username)
        elif choice == "9":
            list_restore_codes()
        elif choice == "10":
            list_users(username)
        elif choice == "11":
            # REQUIREMENT: Session management - logout user
            if logout_user(username):
                print("Successfully logged out.")
                return "logout"
            else:
                print("Logout failed.")
        elif choice == "12":
            exit_system(username)
        else:
            print("Invalid choice. Please try again.")

def system_admin_menu(username):
    # REQUIREMENT: Session management - check session validity
    is_valid, message = check_session(username)
    if not is_valid:
        print(f"Session error: {message}")
        return "logout"
    
    # Check for suspicious activities and display alert
    from system_logging import display_alert_if_suspicious
    display_alert_if_suspicious()
    
    # REQUIREMENT: Session management - display session info
    display_session_info(username)
    
    while True:
        print("\n" + "=" * 50)
        print("    SYSTEM ADMIN MENU")
        print("=" * 50)
        print("1.  Change Password")
        print("2.  Manage Service Engineers")
        print("3.  Manage Travellers")
        print("4.  Manage Scooters")
        print("5.  View System Logs")
        print("6.  Create Backup")
        print("7.  Restore Backup")
        print("8.  View Users")
        print("9.  Exit System")
        print("-" * 50)
        
        choice = input("Enter your choice (1-9): ").strip()
        
        if choice == "1":
            change_password(username)
        elif choice == "2":
            manage_service_engineers(username)
        elif choice == "3":
            manage_travellers(username)
        elif choice == "4":
            manage_scooters(username)
        elif choice == "5":
            view_logs(username)
        elif choice == "6":
            create_backup()
        elif choice == "7":
            restore_backup_menu(username)
        elif choice == "8":
            # System Admin can only view Service Engineers
            from crud_operations import list_service_engineers
            list_service_engineers()
        elif choice == "9":
            exit_system(username)
        else:
            print("Invalid choice. Please try again.")

def service_engineer_menu(username):
    # REQUIREMENT: Session management - check session validity
    is_valid, message = check_session(username)
    if not is_valid:
        print(f"Session error: {message}")
        return "logout"
    
    # Check for suspicious activities and display alert
    from system_logging import display_alert_if_suspicious
    display_alert_if_suspicious()
    
    # REQUIREMENT: Session management - display session info
    display_session_info(username)
    
    while True:
        print("\n" + "=" * 50)
        print("    SERVICE ENGINEER MENU")
        print("=" * 50)
        print("1.  Change Password")
        print("2.  Search Scooters")
        print("3.  Update Scooter Information")
        print("4.  Logout")
        print("5.  Exit System")
        print("-" * 50)
        
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == "1":
            change_password(username)
        elif choice == "2":
            search_scooters_menu()
        elif choice == "3":
            update_scooter_menu_service_engineer()
        elif choice == "4":
            # REQUIREMENT: Session management - logout user
            if logout_user(username):
                print("Successfully logged out.")
                return "logout"
            else:
                print("Logout failed.")
        elif choice == "5":
            exit_system(username)
        else:
            print("Invalid choice. Please try again.")

def manage_system_admins(username):
    while True:
        print("\n=== MANAGE SYSTEM ADMINISTRATORS ===")
        print("1. Add System Administrator")
        print("2. Update System Administrator")
        print("3. Delete System Administrator")
        print("4. Reset Password")
        print("5. Back to Main Menu")
        
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == "1":
            add_system_admin(username)
        elif choice == "2":
            update_system_admin_menu(username)
        elif choice == "3":
            delete_system_admin()
        elif choice == "4":
            reset_password_menu()
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")

def update_system_admin_menu(current_user):
    from input_validation import get_username, get_first_name, get_last_name
    from crud_operations import list_system_admins, update_user_by_id
    from database import get_connection, close_connection

    print("\n" + "=" * 60)
    print("    UPDATE SYSTEM ADMINISTRATOR")
    print("=" * 60)
    print("⚠️  WARNING: This will update user information!")
    print("⚠️  NOTE: Super Admin account (ID 1) is protected and cannot be updated!")
    print()
    
    # Check if there are any System Admins first
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM Users WHERE role = ?', ("System Admin",))
    count = cursor.fetchone()[0]
    close_connection(conn)
    
    if count == 0:
        print("📋 No System Administrators found in the system.")
        print("   Cannot update System Administrators when none exist.")
        return
    
    # Show list of System Administrators
    list_system_admins(current_user)
    
    print("\nEnter the ID of the System Administrator to update:")
    user_id = input("User ID: ").strip()
    
    if not user_id:
        print("User ID is required.")
        return
    
    try:
        user_id = int(user_id)
    except ValueError:
        print("Invalid user ID. Please enter a number.")
        return
    
    # IMMEDIATE VALIDATION - Check if user exists with correct role
    from crud_operations import validate_user_exists_with_role
    is_valid, username, role = validate_user_exists_with_role(user_id, "System Admin")
    if not is_valid:
        return  # Exit if validation fails
    
    print("\n" + "=" * 50)
    print("    UPDATE SYSTEM ADMINISTRATOR")
    print("=" * 50)
    print("Available fields to update:")
    print("1. First Name")
    print("2. Last Name")
    print("3. Username")
    print("4. Cancel Update")

    choice = input("Enter your choice (1-4): ").strip()

    if choice == "1":
        print("\n Update First Name:")
        new_first = get_first_name()
        if new_first:
            update_data = {"first_name": new_first}
            if update_user_by_id(user_id, update_data, current_user, "System Admin"):
                print("First name updated successfully!")
            else:
                print("Failed to update first name.")
        else:
            print("First name cannot be empty. Update cancelled.")
            
    elif choice == "2":
        print("\n Update Last Name:")
        new_last = get_last_name()
        if new_last:
            update_data = {"last_name": new_last}
            if update_user_by_id(user_id, update_data, current_user, "System Admin"):
                print("Last name updated successfully!")
            else:
                print("Failed to update last name.")
        else:
            print("Last name cannot be empty. Update cancelled.")
    
    elif choice == "3":
        print("\n Update Username:")
        new_user = get_username()
        if new_user:
            update_data = {"username": new_user}
            if update_user_by_id(user_id, update_data, current_user, "System Admin"):
                print("Username updated successfully!")
            else:
                print("Failed to update username.")
        else:
            print("Update cancelled.")
    
    elif choice == "4":
        print("Update cancelled.")
        return
    
    else:
        print("Invalid field selection. Please choose 1-4.")

def manage_service_engineers(username):
    while True:
        print("\n=== MANAGE SERVICE ENGINEERS ===")
        print("1. Add Service Engineer")
        print("2. Update Service Engineer")
        print("3. Delete Service Engineer")
        print("4. Reset Password")
        print("5. Back to Main Menu")
        
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == "1":
            add_service_engineer(username)
        elif choice == "2":
            update_service_engineer_menu(username)
        elif choice == "3":
            delete_service_engineer()
        elif choice == "4":
            reset_password_menu()
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")


def update_service_engineer_menu(current_user):
    from input_validation import get_username, get_first_name, get_last_name
    from crud_operations import list_service_engineers, update_user_by_id
    from database import get_connection, close_connection

    print("\n" + "=" * 60)
    print("    UPDATE SERVICE ENGINEER")
    print("=" * 60)
    print("⚠️  WARNING: This will update user information!")
    print()
    
    # Check if there are any Service Engineers first
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM Users WHERE role = ?', ("Service Engineer",))
    count = cursor.fetchone()[0]
    close_connection(conn)
    
    if count == 0:
        print("📋 No Service Engineers found in the system.")
        print("   Cannot update Service Engineers when none exist.")
        return
    
    # Show list of Service Engineers
    list_service_engineers(current_user)
    
    print("\nEnter the ID of the Service Engineer to update:")
    user_id = input("User ID: ").strip()
    
    if not user_id:
        print("User ID is required.")
        return
    
    try:
        user_id = int(user_id)
    except ValueError:
        print("Invalid user ID. Please enter a number.")
        return
    
    # IMMEDIATE VALIDATION - Check if user exists with correct role
    from crud_operations import validate_user_exists_with_role
    is_valid, username, role = validate_user_exists_with_role(user_id, "Service Engineer")
    if not is_valid:
        return  # Exit if validation fails
    
    print("\n" + "=" * 50)
    print("    UPDATE SERVICE ENGINEER")
    print("=" * 50)
    print("Available fields to update:")
    print("1. First Name")
    print("2. Last Name")
    print("3. Username")
    print("4. Cancel Update")

    choice = input("Enter your choice (1-4): ").strip()

    if choice == "1":
        print("\n Update First Name:")
        new_first = get_first_name()
        if new_first:
            update_data = {"first_name": new_first}
            if update_user_by_id(user_id, update_data, current_user, "System Admin"):
                print("First name updated successfully!")
            else:
                print("Failed to update first name.")
        else:
            print("First name cannot be empty. Update cancelled.")
            
    elif choice == "2":
        print("\n Update Last Name:")
        new_last = get_last_name()
        if new_last:
            update_data = {"last_name": new_last}
            if update_user_by_id(user_id, update_data, current_user, "System Admin"):
                print("Last name updated successfully!")
            else:
                print("Failed to update last name.")
        else:
            print("Last name cannot be empty. Update cancelled.")
    
    elif choice == "3":
        print("\n Update Username:")
        new_user = get_username()
        if new_user:
            update_data = {"username": new_user}
            if update_user_by_id(user_id, update_data, current_user, "System Admin"):
                print("Username updated successfully!")
            else:
                print("Failed to update username.")
        else:
            print("Update cancelled.")
    
    elif choice == "4":
        print("Update cancelled.")
        return
    
    else:
        print("Invalid field selection. Please choose 1-4.")



def manage_travellers(username):
    while True:
        print("\n=== MANAGE TRAVELLERS ===")
        print("1. Add Traveller")
        print("2. Search Travellers")
        print("3. Update Traveller")
        print("4. Delete Traveller")
        print("5. Back to Main Menu")
        
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == "1":
            add_traveller_menu()
        elif choice == "2":
            search_travellers_menu()
        elif choice == "3":
            update_traveller_menu(username)
        elif choice == "4":
            delete_traveller_menu()
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")

def manage_scooters(username):
    while True:
        print("\n=== MANAGE SCOOTERS ===")
        print("1. Add Scooter")
        print("2. Search Scooters")
        print("3. Update Scooter")
        print("4. Delete Scooter")
        print("5. Back to Main Menu")
        
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == "1":
            add_scooter_menu()
        elif choice == "2":
            search_scooters_menu()
        elif choice == "3":
            update_scooter_menu()
        elif choice == "4":
            delete_scooter_menu()
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")

def add_traveller_menu():
    print("\n" + "=" * 50)
    print("    ADD NEW TRAVELLER")
    print("=" * 50)
    print("Please provide the following information:")
    
    from input_validation import get_birthday, get_gender, get_zip_code, get_city, get_email, get_phone, get_driving_license
    
    traveller_data = {}
    
    print("\n Personal Information:")
    traveller_data['first_name'] = input("First Name: ").strip()
    if not traveller_data['first_name']:
        print("First name is required. Operation cancelled.")
        return
    
    traveller_data['last_name'] = input("Last Name: ").strip()
    if not traveller_data['last_name']:
        print("Last name is required. Operation cancelled.")
        return
    
    traveller_data['birthday'] = get_birthday()
    if not traveller_data['birthday']:
        print("Birthday is required. Operation cancelled.")
        return
    
    traveller_data['gender'] = get_gender()
    if not traveller_data['gender']:
        print("Gender is required. Operation cancelled.")
        return
    
    print("\n Address Information:")
    traveller_data['street_name'] = input("Street Name: ").strip()
    if not traveller_data['street_name']:
        print("Street name is required. Operation cancelled.")
        return
    
    traveller_data['house_number'] = input("House Number: ").strip()
    if not traveller_data['house_number']:
        print("House number is required. Operation cancelled.")
        return
    
    traveller_data['zip_code'] = get_zip_code()
    if not traveller_data['zip_code']:
        print("Zip code is required. Operation cancelled.")
        return
    
    traveller_data['city'] = get_city()
    if not traveller_data['city']:
        print("City is required. Operation cancelled.")
        return
    
    print("\n Contact Information:")
    traveller_data['email'] = get_email()
    if not traveller_data['email']:
        print("Email is required. Operation cancelled.")
        return
    
    traveller_data['mobile_phone'] = get_phone()
    if not traveller_data['mobile_phone']:
        print("Mobile phone is required. Operation cancelled.")
        return
    
    print("\n License Information:")
    traveller_data['driving_license'] = get_driving_license()
    if not traveller_data['driving_license']:
        print("Driving license is required. Operation cancelled.")
        return
    
    print("\n🔄 Creating traveller...")
    if create_traveller(traveller_data):
        print("Traveller added successfully!")
    else:
        print("Failed to add traveller. Please check your input.")

def update_traveller_menu(current_user):
    from input_validation import (get_first_name, get_last_name, get_gender, get_zip_code, 
                                get_city, get_email, get_phone, get_driving_license)
    from crud_operations import list_travellers
    from database import get_connection, close_connection

    print("\n" + "=" * 60)
    print("    UPDATE TRAVELLER")
    print("=" * 60)
    print("⚠️  WARNING: This will update traveller information!")
    print()
    
    # Check if there are any travellers first
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM Travellers')
    count = cursor.fetchone()[0]
    close_connection(conn)
    
    if count == 0:
        print("📋 No travellers found in the system.")
        print("   Cannot update travellers when none exist.")
        return
    
    # Show list of all travellers
    list_travellers()
    
    print("\nEnter the ID of the Traveller to update:")
    traveller_id = input("Traveller ID: ").strip()
    if not traveller_id:
        print("Traveller ID is required. Operation cancelled")
        return

    traveller = search_traveller_by_id(traveller_id)
    if not traveller:
        print(f"❌ ERROR: Traveller with ID '{traveller_id}' not found.")
        print(f"   Please select a valid traveller ID from the list above.")
        return
    
    print("\n" + "=" * 50)
    print("    UPDATE TRAVELLER")
    print("=" * 50)
    print("Available fields to update:")
    print("1. First Name")
    print("2. Last Name")
    print("3. Gender")
    print("4. Street Name")
    print("5. House Number")
    print("6. Zip Code")
    print("7. City")
    print("8. Email")
    print("9. Phone Number")
    print("10. Driving License")
    print("11. Cancel Update")

    choice = input("Enter your choice (1-11): ").strip()

    if choice == "1":
        print("\n Update First Name:")
        new_first = get_first_name()
        if new_first:
            update_data = {"first_name": new_first}
            if update_traveller(traveller_id, update_data):
                print("First name updated successfully!")
            else:
                print("Failed to update first name.")
        else:
            print("First name cannot be empty. Update cancelled.")
            
    elif choice == "2":
        print("\n Update Last Name:")
        new_last = get_last_name()
        if new_last:
            update_data = {"last_name": new_last}
            if update_traveller(traveller_id, update_data):
                print("Last name updated successfully!")
            else:
                print("Failed to update last name.")
        else:
            print("Last name cannot be empty. Update cancelled.")
    
    elif choice == "3":
        print("\n Update Gender:")
        new_gender = get_gender()
        if new_gender:
            update_data = {"gender": new_gender}
            if update_traveller(traveller_id, update_data):
                print("Gender updated successfully!")
            else:
                print("Failed to update gender.")
        else:
            print("Gender cannot be empty. Update cancelled.")
    
    elif choice == "4":
        print("\n Update Street Name:")
        new_street = input("Enter new street name: ").strip()
        if new_street:
            update_data = {"street_name": new_street}
            if update_traveller(traveller_id, update_data):
                print("Street name updated successfully!")
            else:
                print("Failed to update street name.")
        else:
            print("Street name cannot be empty. Update cancelled.")
    
    elif choice == "5":
        print("\n Update House Number:")
        new_house = input("Enter new house number: ").strip()
        if new_house:
            update_data = {"house_number": new_house}
            if update_traveller(traveller_id, update_data):
                print("House number updated successfully!")
            else:
                print("Failed to update house number.")
        else:
            print("House number cannot be empty. Update cancelled.")
    
    elif choice == "6":
        print("\n Update Zip Code:")
        new_zip = get_zip_code()
        if new_zip:
            update_data = {"zip_code": new_zip}
            if update_traveller(traveller_id, update_data):
                print("Zip code updated successfully!")
            else:
                print("Failed to update zip code.")
        else:
            print("Zip code cannot be empty. Update cancelled.")
    
    elif choice == "7":
        print("\n Update City:")
        new_city = get_city()
        if new_city:
            update_data = {"city": new_city}
            if update_traveller(traveller_id, update_data):
                print("City updated successfully!")
            else:
                print("Failed to update city.")
        else:
            print("City cannot be empty. Update cancelled.")
    
    elif choice == "8":
        print("\n Update Email:")
        new_email = get_email()
        if new_email:
            update_data = {"email": new_email}
            if update_traveller(traveller_id, update_data):
                print("Email updated successfully!")
            else:
                print("Failed to update email.")
        else:
            print("Email cannot be empty. Update cancelled.")
    
    elif choice == "9":
        print("\n Update Phone Number:")
        new_phone = get_phone()
        if new_phone:
            update_data = {"mobile_phone": new_phone}
            if update_traveller(traveller_id, update_data):
                print("Phone number updated successfully!")
            else:
                print("Failed to update phone number.")
        else:
            print("Phone number cannot be empty. Update cancelled.")
    
    elif choice == "10":
        print("\n Update Driving License:")
        new_license = get_driving_license()
        if new_license:
            update_data = {"driving_license": new_license}
            if update_traveller(traveller_id, update_data):
                print("Driving license updated successfully!")
            else:
                print("Failed to update driving license.")
        else:
            print("Driving license cannot be empty. Update cancelled.")
    
    elif choice == "11":
        print("Update cancelled.")
        return
    
    else:
        print("Invalid field selection. Please choose 1-11.")

def add_scooter_menu():
    print("\n" + "=" * 50)
    print("    ADD NEW SCOOTER")
    print("=" * 50)
    print("Please provide the following information:")
    
    from input_validation import (get_brand, get_model, get_serial_number, get_top_speed, 
                                get_battery_capacity, get_state_of_charge, get_target_range,
                                get_coordinates, get_boolean_input, get_mileage, get_maintenance_date)
    
    scooter_data = {}
    
    print("\n Basic Information:")
    scooter_data['brand'] = get_brand()
    if not scooter_data['brand']:
        print("Brand is required. Operation cancelled.")
        return
    
    scooter_data['model'] = get_model()
    if not scooter_data['model']:
        print("Model is required. Operation cancelled.")
        return
    
    scooter_data['serial_number'] = get_serial_number()
    if not scooter_data['serial_number']:
        print("Serial number is required. Operation cancelled.")
        return
    
    print("\nPerformance Information:")
    scooter_data['top_speed'] = get_top_speed()
    if not scooter_data['top_speed']:
        print("Top speed is required. Operation cancelled.")
        return
    
    scooter_data['battery_capacity'] = get_battery_capacity()
    if not scooter_data['battery_capacity']:
        print("Battery capacity is required. Operation cancelled.")
        return
    
    scooter_data['state_of_charge'] = get_state_of_charge()
    if not scooter_data['state_of_charge']:
        print("State of charge is required. Operation cancelled.")
        return
    
    print("\n Target Range Information:")
    target_min, target_max = get_target_range()
    if target_min is None or target_max is None:
        print("Target range is required. Operation cancelled.")
        return
    scooter_data['target_range_min'] = target_min
    scooter_data['target_range_max'] = target_max
    
    print("\n Location Information:")
    lat, lon = get_coordinates()
    if lat is None or lon is None:
        print("Coordinates are required. Operation cancelled.")
        return
    scooter_data['latitude'] = lat
    scooter_data['longitude'] = lon
    
    print("\n Status Information:")
    scooter_data['out_of_service'] = get_boolean_input("Is the scooter out of service?")
    
    scooter_data['mileage'] = get_mileage()
    if not scooter_data['mileage']:
        print("Mileage is required. Operation cancelled.")
        return
    
    scooter_data['last_maintenance_date'] = get_maintenance_date()
    if not scooter_data['last_maintenance_date']:
        print("Last maintenance date is required. Operation cancelled.")
        return
    
    print("\n Creating scooter...")
    if create_scooter(scooter_data):
        print("Scooter added successfully!")
    else:
        print("Failed to add scooter. Please check your input.")

def search_travellers_menu():
    search_term = input("Enter search term (name, email, phone, or traveller ID): ").strip()
    if search_term:
        search_travellers(search_term)

def search_scooters_menu():
    search_term = input("Enter search term (brand, model, or serial number): ").strip()
    if search_term:
        search_scooters(search_term)

def update_scooter_menu_service_engineer():
    from input_validation import (get_state_of_charge, get_coordinates, get_boolean_input, 
                                get_mileage, get_maintenance_date)
    
    scooter_id = input("Enter Scooter ID to update: ").strip()
    if not scooter_id.isdigit():
        print("Invalid scooter ID. Must be a number.")
        return
    
    print("\n" + "=" * 50)
    print("    UPDATE SCOOTER (SERVICE ENGINEER)")
    print("=" * 50)
    print("Available fields to update:")
    print("1. State of Charge (0-100%)")
    print("2. Location (Latitude & Longitude)")
    print("3. Out of Service Status")
    print("4. Mileage (0-100000 km)")
    print("5. Last Maintenance Date")
    print("6. Cancel Update")
    
    field_choice = input("\nSelect field (1-6): ").strip()
    
    if field_choice == "1":
        print("\n🔋 Update State of Charge:")
        new_value = get_state_of_charge()
        if new_value is not None:
            update_data = {"state_of_charge": new_value}
            if update_scooter(int(scooter_id), update_data):
                print("State of charge updated successfully!")
            else:
                print("Failed to update state of charge.")
        else:
            print("Update cancelled.")
    
    elif field_choice == "2":
        print("\n Update Location:")
        lat, lon = get_coordinates()
        if lat is not None and lon is not None:
            update_data = {"latitude": lat, "longitude": lon}
            if update_scooter(int(scooter_id), update_data):
                print("Location updated successfully!")
            else:
                print("Failed to update location.")
        else:
            print("Update cancelled.")
    
    elif field_choice == "3":
        print("\n Update Out of Service Status:")
        new_value = get_boolean_input("Is the scooter out of service?")
        update_data = {"out_of_service": new_value}
        if update_scooter(int(scooter_id), update_data):
            status = "out of service" if new_value else "in service"
            print(f"Scooter status updated to {status}!")
        else:
            print("Failed to update service status.")
    
    elif field_choice == "4":
        print("\n📏 Update Mileage:")
        new_value = get_mileage()
        if new_value is not None:
            update_data = {"mileage": new_value}
            if update_scooter(int(scooter_id), update_data):
                print("Mileage updated successfully!")
            else:
                print("Failed to update mileage.")
        else:
            print("Update cancelled.")
    
    elif field_choice == "5":
        print("\n Update Last Maintenance Date:")
        new_value = get_maintenance_date()
        if new_value:
            update_data = {"last_maintenance_date": new_value}
            if update_scooter(int(scooter_id), update_data):
                print("Last maintenance date updated successfully!")
            else:
                print("Failed to update maintenance date.")
        else:
            print("Update cancelled.")
    
    elif field_choice == "6":
        print("Update cancelled.")
        return
    
    else:
        print("Invalid field selection. Please choose 1-6.")

def update_scooter_menu():
    from input_validation import (get_brand, get_model, get_serial_number, get_top_speed,
                                get_battery_capacity, get_state_of_charge, get_target_range,
                                get_coordinates, get_boolean_input, get_mileage, get_maintenance_date)
    from crud_operations import list_scooters
    from database import get_connection, close_connection
    
    print("\n" + "=" * 60)
    print("    UPDATE SCOOTER")
    print("=" * 60)
    print("⚠️  WARNING: This will update scooter information!")
    print()
    
    # Check if there are any scooters first
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM Scooters')
    count = cursor.fetchone()[0]
    close_connection(conn)
    
    if count == 0:
        print("📋 No scooters found in the system.")
        print("   Cannot update scooters when none exist.")
        return
    
    # Show list of all scooters
    list_scooters()
    
    print("\nEnter the ID of the Scooter to update:")
    scooter_id = input("Scooter ID: ").strip()
    if not scooter_id:
        print("Scooter ID is required. Operation cancelled")
        return
    
    if not scooter_id.isdigit():
        print("Invalid scooter ID. Must be a number.")
        return
    
    # IMMEDIATE VALIDATION - Check if scooter exists
    from crud_operations import update_scooter
    # Test if scooter exists by trying to get it
    import sqlite3
    from database import get_connection, close_connection
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM Scooters WHERE id = ?', (int(scooter_id),))
    scooter_exists = cursor.fetchone()
    close_connection(conn)
    
    if not scooter_exists:
        print(f"❌ ERROR: No scooter found with ID {scooter_id}")
        print(f"   Please select a valid scooter ID from the list above.")
        return
    
    print("\n" + "=" * 50)
    print("    UPDATE SCOOTER (SYSTEM ADMIN)")
    print("=" * 50)
    print("Available fields to update:")
    print("1. Brand")
    print("2. Model")
    print("3. Serial Number")
    print("4. Top Speed")
    print("5. Battery Capacity")
    print("6. State of Charge")
    print("7. Target Range")
    print("8. Location (Latitude & Longitude)")
    print("9. Out of Service Status")
    print("10. Mileage")
    print("11. Last Maintenance Date")
    print("12. Cancel Update")
    
    field_choice = input("\nSelect field (1-12): ").strip()
    
    if field_choice == "1":
        print("\n Update Brand:")
        new_value = get_brand()
        if new_value:
            update_data = {"brand": new_value}
            if update_scooter(int(scooter_id), update_data):
                print("Brand updated successfully!")
            else:
                print("Failed to update brand.")
        else:
            print("Update cancelled.")
    
    elif field_choice == "2":
        print("\n Update Model:")
        new_value = get_model()
        if new_value:
            update_data = {"model": new_value}
            if update_scooter(int(scooter_id), update_data):
                print("Model updated successfully!")
            else:
                print("Failed to update model.")
        else:
            print("Update cancelled.")
    
    elif field_choice == "3":
        print("\n Update Serial Number:")
        new_value = get_serial_number()
        if new_value:
            update_data = {"serial_number": new_value}
            if update_scooter(int(scooter_id), update_data):
                print("Serial number updated successfully!")
            else:
                print("Failed to update serial number.")
        else:
            print("Update cancelled.")
    
    elif field_choice == "4":
        print("\n Update Top Speed:")
        new_value = get_top_speed()
        if new_value is not None:
            update_data = {"top_speed": new_value}
            if update_scooter(int(scooter_id), update_data):
                print("Top speed updated successfully!")
            else:
                print("Failed to update top speed.")
        else:
            print("Update cancelled.")
    
    elif field_choice == "5":
        print("\n Update Battery Capacity:")
        new_value = get_battery_capacity()
        if new_value is not None:
            update_data = {"battery_capacity": new_value}
            if update_scooter(int(scooter_id), update_data):
                print("Battery capacity updated successfully!")
            else:
                print("Failed to update battery capacity.")
        else:
            print("Update cancelled.")
    
    elif field_choice == "6":
        print("\n Update State of Charge:")
        new_value = get_state_of_charge()
        if new_value is not None:
            update_data = {"state_of_charge": new_value}
            if update_scooter(int(scooter_id), update_data):
                print("State of charge updated successfully!")
            else:
                print("Failed to update state of charge.")
        else:
            print("Update cancelled.")
    
    elif field_choice == "7":
        print("\n Update Target Range:")
        min_range, max_range = get_target_range()
        if min_range is not None and max_range is not None:
            update_data = {"target_range_min": min_range, "target_range_max": max_range}
            if update_scooter(int(scooter_id), update_data):
                print("Target range updated successfully!")
            else:
                print("Failed to update target range.")
        else:
            print("Update cancelled.")
    
    elif field_choice == "8":
        print("\n Update Location:")
        lat, lon = get_coordinates()
        if lat is not None and lon is not None:
            update_data = {"latitude": lat, "longitude": lon}
            if update_scooter(int(scooter_id), update_data):
                print("Location updated successfully!")
            else:
                print("Failed to update location.")
        else:
            print("Update cancelled.")
    
    elif field_choice == "9":
        print("\n Update Out of Service Status:")
        new_value = get_boolean_input("Is the scooter out of service?")
        update_data = {"out_of_service": new_value}
        if update_scooter(int(scooter_id), update_data):
            status = "out of service" if new_value else "in service"
            print(f"Scooter status updated to {status}!")
        else:
            print("Failed to update service status.")
    
    elif field_choice == "10":
        print("\n Update Mileage:")
        new_value = get_mileage()
        if new_value is not None:
            update_data = {"mileage": new_value}
            if update_scooter(int(scooter_id), update_data):
                print("Mileage updated successfully!")
            else:
                print("Failed to update mileage.")
        else:
            print("Update cancelled.")
    
    elif field_choice == "11":
        print("\n Update Last Maintenance Date:")
        new_value = get_maintenance_date()
        if new_value:
            update_data = {"last_maintenance_date": new_value}
            if update_scooter(int(scooter_id), update_data):
                print("Last maintenance date updated successfully!")
            else:
                print("Failed to update maintenance date.")
        else:
            print("Update cancelled.")
    
    elif field_choice == "12":
        print("Update cancelled.")
        return
    
    else:
        print("Invalid field selection. Please choose 1-12.")

def delete_traveller_menu():
    from crud_operations import list_travellers
    from database import get_connection, close_connection
    
    print("\n" + "=" * 60)
    print("    DELETE TRAVELLER")
    print("=" * 60)
    print("⚠️  WARNING: This action cannot be undone!")
    print()
    
    # Check if there are any travellers first
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM Travellers')
    count = cursor.fetchone()[0]
    close_connection(conn)
    
    if count == 0:
        print("📋 No travellers found in the system.")
        print("   Cannot delete travellers when none exist.")
        return
    
    # Show list of all travellers
    list_travellers()
    
    print("\nEnter the ID of the Traveller to delete:")
    traveller_id = input("Traveller ID: ").strip()
    if not traveller_id:
        print("Traveller ID is required. Operation cancelled")
        return
    
    # Validate traveller exists
    from crud_operations import search_traveller_by_id
    traveller = search_traveller_by_id(traveller_id)
    if not traveller:
        print(f"❌ ERROR: Traveller with ID '{traveller_id}' not found.")
        print(f"   Please select a valid traveller ID from the list above.")
        return
    
    confirm = input(f"Are you sure you want to delete traveller {traveller_id}? (y/n): ").strip().lower()
    if confirm == 'y':
        delete_traveller(traveller_id)
    else:
        print("Deletion cancelled.")

def delete_scooter_menu():
    from crud_operations import list_scooters
    from database import get_connection, close_connection
    
    print("\n" + "=" * 60)
    print("    DELETE SCOOTER")
    print("=" * 60)
    print("⚠️  WARNING: This action cannot be undone!")
    print()
    
    # Check if there are any scooters first
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM Scooters')
    count = cursor.fetchone()[0]
    close_connection(conn)
    
    if count == 0:
        print("📋 No scooters found in the system.")
        print("   Cannot delete scooters when none exist.")
        return
    
    # Show list of all scooters
    list_scooters()
    
    print("\nEnter the ID of the Scooter to delete:")
    scooter_id = input("Scooter ID: ").strip()
    if not scooter_id:
        print("Scooter ID is required. Operation cancelled")
        return
    
    if not scooter_id.isdigit():
        print("Invalid scooter ID. Must be a number.")
        return
    
    # Validate scooter exists
    from database import get_connection, close_connection
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM Scooters WHERE id = ?', (int(scooter_id),))
    scooter_exists = cursor.fetchone()
    close_connection(conn)
    
    if not scooter_exists:
        print(f"❌ ERROR: Scooter with ID '{scooter_id}' not found.")
        print(f"   Please select a valid scooter ID from the list above.")
        return
    
    confirm = input(f"Are you sure you want to delete scooter {scooter_id}? (y/n): ").strip().lower()
    if confirm == 'y':
        delete_scooter(int(scooter_id))
    else:
        print("Deletion cancelled.")

def add_system_admin(current_user):
    print("\n" + "=" * 50)
    print("    ADD SYSTEM ADMINISTRATOR")
    print("=" * 50)
    print("Please provide the following information:")
    
    from input_validation import get_username, get_password, get_first_name, get_last_name
    
    print("\n User Information:")
    username = get_username()
    if not username:
        print("Username is required. Operation cancelled.")
        return
    
    password = get_password()
    if not password:
        print("Password is required. Operation cancelled.")
        return
    
    first_name = input("First Name: ").strip()
    if not first_name:
        print("First name is required. Operation cancelled.")
        return
    
    last_name = input("Last Name: ").strip()
    if not last_name:
        print("Last name is required. Operation cancelled.")
        return
    
    print("\n Creating System Administrator...")
    from authentication import hash_password
    hashed_password = hash_password(password)
    
    user_data = {
        'username': username,
        'password_hash': hashed_password,
        'first_name': first_name,
        'last_name': last_name,
        'role': 'System Admin'
    }
    if create_user(user_data, current_user):
        print("System Administrator created successfully!")
    else:
        print("Failed to create System Administrator.")

def add_service_engineer(current_user):
    print("\n" + "=" * 50)
    print("    ADD SERVICE ENGINEER")
    print("=" * 50)
    print("Please provide the following information:")
    
    from input_validation import get_username, get_password, get_first_name, get_last_name
    
    print("\n User Information:")
    username = get_username()
    if not username:
        print("Username is required. Operation cancelled.")
        return
    
    password = get_password()
    if not password:
        print("Password is required. Operation cancelled.")
        return
    
    first_name = input("First Name: ").strip()
    if not first_name:
        print("First name is required. Operation cancelled.")
        return
    
    last_name = input("Last Name: ").strip()
    if not last_name:
        print("Last name is required. Operation cancelled.")
        return
    
    print("\n Creating Service Engineer...")
    from authentication import hash_password
    hashed_password = hash_password(password)
    
    user_data = {
        'username': username,
        'password_hash': hashed_password,
        'first_name': first_name,
        'last_name': last_name,
        'role': 'Service Engineer'
    }
    if create_user(user_data, current_user):
        print("Service Engineer created successfully!")
    else:
        print("Failed to create Service Engineer.")

def list_system_admins():
    print("\n=== SYSTEM ADMINISTRATORS ===")
    list_users("super_admin")

def list_service_engineers():
    """List Service Engineers"""
    print("\n=== SERVICE ENGINEERS ===")
    list_users("super_admin")

def delete_system_admin():
    from database import get_connection, close_connection
    
    print("\n" + "=" * 60)
    print("    DELETE SYSTEM ADMINISTRATOR")
    print("=" * 60)
    print("⚠️  WARNING: This action cannot be undone!")
    print("⚠️  Super Admin account cannot be deleted.")
    print()
    
    # Check if there are any System Admins first
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM Users WHERE role = ?', ("System Admin",))
    count = cursor.fetchone()[0]
    close_connection(conn)
    
    if count == 0:
        print("📋 No System Administrators found in the system.")
        print("   Cannot delete System Administrators when none exist.")
        return
    
    # Show list of System Administrators
    from crud_operations import list_system_admins
    list_system_admins("super_admin")
    
    print("\nEnter the ID of the System Administrator to delete:")
    user_id = input("User ID: ").strip()
    
    if not user_id:
        print("User ID is required.")
        return
    
    try:
        user_id = int(user_id)
        delete_user_by_id(user_id, "super_admin", "System Admin")
    except ValueError:
        print("Invalid user ID. Please enter a number.")
        return

def delete_service_engineer():
    from database import get_connection, close_connection
    
    print("\n" + "=" * 60)
    print("    DELETE SERVICE ENGINEER")
    print("=" * 60)
    print("⚠️  WARNING: This action cannot be undone!")
    print()
    
    # Check if there are any Service Engineers first
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM Users WHERE role = ?', ("Service Engineer",))
    count = cursor.fetchone()[0]
    close_connection(conn)
    
    if count == 0:
        print("📋 No Service Engineers found in the system.")
        print("   Cannot delete Service Engineers when none exist.")
        return
    
    # Show list of Service Engineers
    from crud_operations import list_service_engineers
    list_service_engineers("super_admin")
    
    print("\nEnter the ID of the Service Engineer to delete:")
    user_id = input("User ID: ").strip()
    
    if not user_id:
        print("User ID is required.")
        return
    
    try:
        user_id = int(user_id)
        delete_user_by_id(user_id, "super_admin", "Service Engineer")
    except ValueError:
        print("Invalid user ID. Please enter a number.")
        return

def reset_password_menu():
    print("\n" + "=" * 60)
    print("    RESET USER PASSWORD")
    print("=" * 60)
    
    # Show list of all users
    from crud_operations import list_users
    list_users("super_admin")
    
    print("\nEnter the username to reset password:")
    username = input("Username: ").strip()
    new_password = input("Enter new temporary password: ").strip()
    
    if not username or not new_password:
        print("Username and password are required.")
        return
    
    from authentication import hash_password
    hashed_password = hash_password(new_password)
    
    # Fix: Use the correct function name
    from crud_operations import update_user_password
    if update_user_password(username, hashed_password, "super_admin"):
        print("Password reset successfully!")
    else:
        print("Failed to reset password.")

def view_logs(username):
    print("\n=== SYSTEM LOGS ===")
    print("1. View All Logs")
    print("2. View Suspicious Activities")
    print("3. Back")
    
    choice = input("Enter your choice (1-3): ").strip()
    
    if choice == "1":
        from system_logging import display_logs_formatted
        display_logs_formatted()
    elif choice == "2":
        from system_logging import get_suspicious_logs
        suspicious_logs = get_suspicious_logs()
        if isinstance(suspicious_logs, list):
            print("\n" + "=" * 100)
            print("                                    SUSPICIOUS ACTIVITIES")
            print("=" * 100)
            for log in suspicious_logs:
                print(log)
            print("=" * 100)
        else:
            print(suspicious_logs)

def generate_restore_code_menu(username):
    system_admin = input("Enter System Admin username: ").strip()
    if not system_admin:
        print("Username cannot be empty")
        return
    
    backup_files = list_backups()
    if not backup_files:
        print("No backup files found. Create a backup first.")
        return
    
    print("Available backups:")
    for i, backup in enumerate(backup_files, 1):
        print(f"{i}. {backup}")
    
    choice = input("Select backup (number): ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(backup_files):
        backup_file = backup_files[int(choice) - 1]
        generate_restore_code(system_admin, backup_file)
    else:
        print("Invalid selection")

def revoke_restore_code_menu(username):
    code = input("Enter restore code to revoke: ").strip()
    if not code:
        print("Restore code cannot be empty")
        return
    revoke_restore_code(code)

def restore_backup_menu(username):
    code = input("Enter restore code: ").strip()
    if not code:
        print("Restore code cannot be empty")
        return
    restore_backup(code, username)

if __name__ == "__main__":
    main()
