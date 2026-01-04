import sys
from database import initialize_db
from authentication import login, change_password, logout_user
from session_management import check_session, display_session_info
from error_handler import safe_execute
from system_logging import log_action, get_unread_suspicious_count
from backup import create_backup, generate_restore_code, restore_backup, list_backups, revoke_restore_code, list_restore_codes
from crud_operations import *
from input_validation import collector, validator

def get_validated_id(prompt, entity_name):
    return collector.get_validated_input(
        prompt,
        lambda x: (x.isdigit(), "Must be a number") if x.isdigit() else (False, "Must be a number"),
        f"Invalid {entity_name.lower()} ID. Must be a number.",
        username="unknown",
        field_name=f"{entity_name.lower()}_id"
    )


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
        
    if username is None and role is None:
        return
    
    if role in ["System Admin", "Super Admin"]:
        suspicious_count = get_unread_suspicious_count(username)
        if suspicious_count > 0:
            print(f"\n ALERT: {suspicious_count} suspicious activities detected in the last 24 hours!")
            print("Please review the logs for details.")
    
    log_action(username, "Logged in successfully")
    
    safe_execute(_main_loop, username, "Main System Loop", username, role)

def _main_loop(username, role):
    while True:
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

def super_admin_menu(username):
    while True:
        is_valid, message = check_session(username)
        if not is_valid:
            print(f"Session error: {message}")
            return "logout"
        
        display_session_info(username)
    
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
        print("-" * 50)
        
        choice = collector.get_menu_choice("Enter your choice (1-11): ", 11, username=username)
        
        if choice == 1:
            manage_system_admins(username)
        elif choice == 2:
            manage_service_engineers(username)
        elif choice == 3:
            manage_travellers(username)
        elif choice == 4:
            manage_scooters(username)
        elif choice == 5:
            view_logs(username)
        elif choice == 6:
            create_backup()
        elif choice == 7:
            generate_restore_code_menu(username)
        elif choice == 8:
            revoke_restore_code_menu(username)
        elif choice == 9:
            list_restore_codes()
        elif choice == 10:
            list_users(username)
        elif choice == 11:
            if logout_user(username):
                print("Successfully logged out.")
                return "logout"
            else:
                print("Logout failed.")
        else:
            print("Invalid choice. Please try again.")

def system_admin_menu(username):
    is_valid, message = check_session(username)
    if not is_valid:
        print(f"Session error: {message}")
        return "logout"
    
    display_session_info(username)
    
    while True:
        print("\n" + "=" * 50)
        print("    SYSTEM ADMIN MENU")
        print("=" * 50)
        print("1.  Change Password")
        print("2.  Update My Account")
        print("3.  Delete My Account")
        print("4.  Manage Service Engineers")
        print("5.  Manage Travellers")
        print("6.  Manage Scooters")
        print("7.  View System Logs")
        print("8.  Create Backup")
        print("9.  Restore Backup")
        print("10. View Users")
        print("11. Logout")
        print("-" * 50)
        
        choice = collector.get_menu_choice("Enter your choice (1-11): ", 11, username=username)
        
        if choice == 1:
            change_password(username)
        elif choice == 2:
            username = update_my_account_menu(username)
        elif choice == 3:
            delete_my_account_menu(username)
        elif choice == 4:
            manage_service_engineers(username)
        elif choice == 5:
            manage_travellers(username)
        elif choice == 6:
            manage_scooters(username)
        elif choice == 7:
            view_logs(username)
        elif choice == 8:
            create_backup()
        elif choice == 9:
            restore_backup_menu(username)
        elif choice == 10:
            list_users(username)
        elif choice == 11:
            if logout_user(username):
                print("Successfully logged out.")
                return "logout"
            else:
                print("Logout failed.")
        else:
            print("Invalid choice. Please try again.")
        

def service_engineer_menu(username):
    is_valid, message = check_session(username)
    if not is_valid:
        print(f"Session error: {message}")
        return "logout"
    
    display_session_info(username)
    
    while True:
        print("\n" + "=" * 50)
        print("    SERVICE ENGINEER MENU")
        print("=" * 50)
        print("1.  Change Password")
        print("2.  Search Scooters")
        print("3.  Update Scooter Information")
        print("4.  Logout")
        print("-" * 50)
        
        choice = collector.get_menu_choice("Enter your choice (1-4): ", 4, username=username)
        
        if choice == 1:
            change_password(username)
        elif choice == 2:
            search_scooters_menu()
        elif choice == 3:
            update_scooter_menu_service_engineer(username)
        elif choice == 4:
            if logout_user(username):
                print("Successfully logged out.")
                return "logout"
            else:
                print("Logout failed.")
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
        
        choice = collector.get_menu_choice("Enter your choice (1-5): ", 5, username=username)
        
        if choice == 1:
            add_system_admin(username)
        elif choice == 2:
            update_system_admin_menu(username)
        elif choice == 3:
            delete_system_admin()
        elif choice == 4:
            reset_system_admin_password_menu()
        elif choice == 5:
            break
        else:
            print("Invalid choice. Please try again.")

def update_system_admin_menu(current_user):
    from crud_operations import list_system_admins, update_user_by_id
    from database import get_connection, close_connection

    print("\n" + "=" * 60)
    print("    UPDATE SYSTEM ADMINISTRATOR")
    print("=" * 60)
    print("WARNING: This will update user information!")
    print("NOTE: Super Admin account (ID 1) is protected and cannot be updated!")
    print()
    
    from crud_operations import count_users_by_role
    count = count_users_by_role("System Admin")
    
    if count == 0:
        print("No System Administrators found in the system.")
        print("Cannot update System Administrators when none exist.")
        return
    
    list_system_admins(current_user)
    
    print("\nEnter the ID of the System Administrator to update:")
    user_id = get_validated_id("User ID: ", "User")
    if not user_id:
        print("User ID is required.")
        return
    
    from crud_operations import validate_user_exists_with_role
    is_valid, username, role = validate_user_exists_with_role(user_id, "System Admin")
    if not is_valid:
        return
    
    print("\n" + "=" * 50)
    print("    UPDATE SYSTEM ADMINISTRATOR")
    print("=" * 50)
    print("Available fields to update:")
    print("1. First Name")
    print("2. Last Name")
    print("3. Username")
    print("4. Cancel Update")

    choice = collector.get_menu_choice("Enter your choice (1-4): ", 4)

    if choice == 1:
        print("\n Update First Name:")
        new_first = collector.get_first_name(username=current_user, field_name="first_name")
        if new_first:
            update_data = {"first_name": new_first}
            if update_user_by_id(user_id, update_data, current_user, "System Admin"):
                print("First name updated successfully!")
            else:
                print("Failed to update first name.")
        else:
            print("First name cannot be empty. Update cancelled.")
            
    elif choice == 2:
        print("\n Update Last Name:")
        new_last = collector.get_last_name(username=current_user, field_name="last_name")
        if new_last:
            update_data = {"last_name": new_last}
            if update_user_by_id(user_id, update_data, current_user, "System Admin"):
                print("Last name updated successfully!")
            else:
                print("Failed to update last name.")
        else:
            print("Last name cannot be empty. Update cancelled.")
    
    elif choice == 3:
        print("\n Update Username:")
        new_user = collector.get_username()
        if new_user:
            update_data = {"username": new_user}
            if update_user_by_id(user_id, update_data, current_user, "System Admin"):
                print("Username updated successfully!")
            else:
                print("Failed to update username.")
        else:
            print("Update cancelled.")
    
    elif choice == 4:
        print("Update cancelled.")
        return
    
    else:
        print("Invalid field selection. Please choose 1-4.")

def update_my_account_menu(current_user):
    from crud_operations import update_user_by_id
    from database import get_connection, close_connection
    from session_management import get_current_user_id
    
    print("\n" + "=" * 60)
    print("    UPDATE MY ACCOUNT")
    print("=" * 60)
    print("WARNING: This will update your account information!")
    print()
    
    user_id = get_current_user_id(current_user)
    
    if not user_id:
        print("ERROR: Could not find your user account in session.")
        return current_user
    
    from encryption import decrypt_data
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT role FROM Users WHERE id = ?', (user_id,))
    user_data = cursor.fetchone()
    close_connection(conn)
    
    if not user_data:
        print("ERROR: Could not find your user account in database.")
        return current_user
    
    try:
        user_role = decrypt_data(user_data[0])
    except:
        user_role = user_data[0]
    
    print("\n" + "=" * 50)
    print("    UPDATE MY ACCOUNT")
    print("=" * 50)
    print("Available fields to update:")
    print("1. First Name")
    print("2. Last Name")
    print("3. Username")
    print("4. Cancel Update")

    choice = collector.get_menu_choice("Enter your choice (1-4): ", 4)

    if choice == 1:
        print("\n Update First Name:")
        new_first = collector.get_first_name(username=current_user, field_name="first_name")
        if new_first:
            update_data = {"first_name": new_first}
            success, _ = update_user_by_id(user_id, update_data, current_user, user_role)
            if success:
                print("First name updated successfully!")
            else:
                print("Failed to update first name.")
        else:
            print("First name cannot be empty. Update cancelled.")
            
    elif choice == 2:
        print("\n Update Last Name:")
        new_last = collector.get_last_name(username=current_user, field_name="last_name")
        if new_last:
            update_data = {"last_name": new_last}
            success, _ = update_user_by_id(user_id, update_data, current_user, user_role)
            if success:
                print("Last name updated successfully!")
            else:
                print("Failed to update last name.")
        else:
            print("Last name cannot be empty. Update cancelled.")
    
    elif choice == 3:
        print("\n Update Username:")
        new_user = collector.get_username()
        if new_user:
            update_data = {"username": new_user}
            success, new_username = update_user_by_id(user_id, update_data, current_user, user_role)
            if success:
                print("Username updated successfully!")
                print("NOTE: You will need to use your new username for future logins.")
                return new_username
            else:
                print("Failed to update username.")
        else:
            print("Update cancelled.")
    
    elif choice == 4:
        print("Update cancelled.")
        return current_user
    
    else:
        print("Invalid field selection. Please choose 1-4.")
    
    return current_user

def manage_service_engineers(username):
    while True:
        print("\n=== MANAGE SERVICE ENGINEERS ===")
        print("1. Add Service Engineer")
        print("2. Update Service Engineer")
        print("3. Delete Service Engineer")
        print("4. Reset Password")
        print("5. Back to Main Menu")
        
        choice = collector.get_menu_choice("Enter your choice (1-5): ", 5, username=username)
        
        if choice == 1:
            add_service_engineer(username)
        elif choice == 2:
            update_service_engineer_menu(username)
        elif choice == 3:
            delete_service_engineer()
        elif choice == 4:
            reset_service_engineer_password_menu()
        elif choice == 5:
            break
        else:
            print("Invalid choice. Please try again.")


def update_service_engineer_menu(current_user):
    from crud_operations import list_service_engineers, update_user_by_id
    from database import get_connection, close_connection

    print("\n" + "=" * 60)
    print("    UPDATE SERVICE ENGINEER")
    print("=" * 60)
    print("WARNING: This will update user information!")
    print()
    
    from crud_operations import count_users_by_role
    count = count_users_by_role("Service Engineer")
    
    if count == 0:
        print("No Service Engineers found in the system.")
        print("Cannot update Service Engineers when none exist.")
        return
    
    list_service_engineers(current_user)
    
    print("\nEnter the ID of the Service Engineer to update:")
    user_id = get_validated_id("User ID: ", "User")
    if not user_id:
        print("User ID is required.")
        return
    
    from crud_operations import validate_user_exists_with_role
    is_valid, username, role = validate_user_exists_with_role(user_id, "Service Engineer")
    if not is_valid:
        return 
    
    print("\n" + "=" * 50)
    print("    UPDATE SERVICE ENGINEER")
    print("=" * 50)
    print("Available fields to update:")
    print("1. First Name")
    print("2. Last Name")
    print("3. Username")
    print("4. Cancel Update")

    choice = collector.get_menu_choice("Enter your choice (1-4): ", 4)

    if choice == 1:
        print("\n Update First Name:")
        new_first = collector.get_first_name(username=current_user, field_name="first_name")
        if new_first:
            update_data = {"first_name": new_first}
            if update_user_by_id(user_id, update_data, current_user, "Service Engineer"):
                print("First name updated successfully!")
            else:
                print("Failed to update first name.")
        else:
            print("First name cannot be empty. Update cancelled.")
            
    elif choice == 2:
        print("\n Update Last Name:")
        new_last = collector.get_last_name(username=current_user, field_name="last_name")
        if new_last:
            update_data = {"last_name": new_last}
            if update_user_by_id(user_id, update_data, current_user, "Service Engineer"):
                print("Last name updated successfully!")
            else:
                print("Failed to update last name.")
        else:
            print("Last name cannot be empty. Update cancelled.")
    
    elif choice == 3:
        print("\n Update Username:")
        new_user = collector.get_username()
        if new_user:
            update_data = {"username": new_user}
            if update_user_by_id(user_id, update_data, current_user, "Service Engineer"):
                print("Username updated successfully!")
            else:
                print("Failed to update username.")
        else:
            print("Update cancelled.")
    
    elif choice == 4:
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
        
        choice = collector.get_menu_choice("Enter your choice (1-5): ", 5, username=username)
        
        if choice == 1:
            add_traveller_menu(username)
        elif choice == 2:
            search_travellers_menu()
        elif choice == 3:
            update_traveller_menu(username)
        elif choice == 4:
            delete_traveller_menu()
        elif choice == 5:
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
        
        choice = collector.get_menu_choice("Enter your choice (1-5): ", 5, username=username)
        
        if choice == 1:
            add_scooter_menu(username)
        elif choice == 2:
            search_scooters_menu()
        elif choice == 3:
            update_scooter_menu(username)
        elif choice == 4:
            delete_scooter_menu()
        elif choice == 5:
            break
        else:
            print("Invalid choice. Please try again.")

def add_traveller_menu(current_user):
    print("\n" + "=" * 50)
    print("    ADD NEW TRAVELLER")
    print("=" * 50)
    print("Please provide the following information:")
    
    traveller_data = {}
    
    print("\n Personal Information:")
    traveller_data['first_name'] = collector.get_validated_input(
        "First Name: ", 
        lambda x: validator.validate_pattern(x, 'name', 'first name'),
        "Invalid first name format",
        username=current_user,
        field_name="first_name"
    )
    if not traveller_data['first_name']:
        print("First name is required. Operation cancelled.")
        return
    
    traveller_data['last_name'] = collector.get_validated_input(
        "Last Name: ", 
        lambda x: validator.validate_pattern(x, 'name', 'last name'),
        "Invalid last name format",
        username=current_user,
        field_name="last_name"
    )
    if not traveller_data['last_name']:
        print("Last name is required. Operation cancelled.")
        return
    
    traveller_data['birthday'] = collector.get_birthday()
    if not traveller_data['birthday']:
        print("Birthday is required. Operation cancelled.")
        return
    
    traveller_data['gender'] = collector.get_gender()
    if not traveller_data['gender']:
        print("Gender is required. Operation cancelled.")
        return
    
    print("\n Address Information:")
    traveller_data['street_name'] = collector.get_validated_input(
        "Street Name: ", 
        lambda x: validator.validate_pattern(x, 'street', 'street name'),
        "Invalid street name format",
        username=current_user,
        field_name="street_name"
    )
    if not traveller_data['street_name']:
        print("Street name is required. Operation cancelled.")
        return
    
    traveller_data['house_number'] = collector.get_validated_input(
        "House Number: ", 
        lambda x: validator.validate_pattern(x, 'house_number', 'house number'),
        "Invalid house number format",
        username=current_user,
        field_name="house_number"
    )
    if not traveller_data['house_number']:
        print("House number is required. Operation cancelled.")
        return
    
    traveller_data['zip_code'] = collector.get_zip_code()
    if not traveller_data['zip_code']:
        print("Zip code is required. Operation cancelled.")
        return
    
    traveller_data['city'] = collector.get_city()
    if not traveller_data['city']:
        print("City is required. Operation cancelled.")
        return
    
    print("\n Contact Information:")
    traveller_data['email'] = collector.get_email()
    if not traveller_data['email']:
        print("Email is required. Operation cancelled.")
        return
    
    traveller_data['mobile_phone'] = collector.get_phone()
    if not traveller_data['mobile_phone']:
        print("Mobile phone is required. Operation cancelled.")
        return
    
    print("\n License Information:")
    traveller_data['driving_license'] = collector.get_driving_license()
    if not traveller_data['driving_license']:
        print("Driving license is required. Operation cancelled.")
        return
    
    print("\nCreating traveller...")
    if create_traveller(traveller_data):
        print("Traveller added successfully!")
    else:
        print("Failed to add traveller. Please check your input.")

def update_traveller_menu(current_user):
    from crud_operations import list_travellers
    from database import get_connection, close_connection

    print("\n" + "=" * 60)
    print("UPDATE TRAVELLER")
    print("=" * 60)
    print("WARNING: This will update traveller information!")
    print()
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM Travellers')
    count = cursor.fetchone()[0]
    close_connection(conn)
    
    if count == 0:
        print("No travellers found in the system.")
        print("   Cannot update travellers when none exist.")
        return
    list_travellers()
    
    print("\nEnter the ID of the Traveller to update:")
    traveller_id = get_validated_id("Traveller ID: ", "Traveller")
    if not traveller_id:
        print("Traveller ID is required. Operation cancelled")
        return

    traveller = search_traveller_by_id(traveller_id)
    if not traveller:
        print(f"No traveller found with ID {traveller_id}")
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

    choice = collector.get_menu_choice("Enter your choice (1-11): ", 11, username=current_user)

    if choice == 1:
        print("\n Update First Name:")
        new_first = collector.get_first_name(username=current_user, field_name="first_name")
        if new_first:
            update_data = {"first_name": new_first}
            if update_traveller(traveller_id, update_data):
                print("First name updated successfully!")
            else:
                print("Failed to update first name.")
        else:
            print("First name cannot be empty. Update cancelled.")
            
    elif choice == 2:
        print("\n Update Last Name:")
        new_last = collector.get_last_name(username=current_user, field_name="last_name")
        if new_last:
            update_data = {"last_name": new_last}
            if update_traveller(traveller_id, update_data):
                print("Last name updated successfully!")
            else:
                print("Failed to update last name.")
        else:
            print("Last name cannot be empty. Update cancelled.")
    
    elif choice == 3:
        print("\n Update Gender:")
        new_gender = collector.get_gender()
        if new_gender:
            update_data = {"gender": new_gender}
            if update_traveller(traveller_id, update_data):
                print("Gender updated successfully!")
            else:
                print("Failed to update gender.")
        else:
            print("Gender cannot be empty. Update cancelled.")
    
    elif choice == 4:
        print("\n Update Street Name:")
        new_street = collector.get_validated_input(
            "Enter new street name: ", 
            lambda x: validator.validate_pattern(x, 'street', 'street name'),
            "Invalid street name format",
            username=current_user,
            field_name="street_name"
        )
        if new_street:
            update_data = {"street_name": new_street}
            if update_traveller(traveller_id, update_data):
                print("Street name updated successfully!")
            else:
                print("Failed to update street name.")
        else:
            print("Street name cannot be empty. Update cancelled.")
    
    elif choice == 5:
        print("\n Update House Number:")
        new_house = collector.get_validated_input(
            "Enter new house number: ", 
            lambda x: validator.validate_pattern(x, 'house_number', 'house number'),
            "Invalid house number format",
            username=current_user,
            field_name="house_number"
        )
        if new_house:
            update_data = {"house_number": new_house}
            if update_traveller(traveller_id, update_data):
                print("House number updated successfully!")
            else:
                print("Failed to update house number.")
        else:
            print("House number cannot be empty. Update cancelled.")
    
    elif choice == 6:
        print("\n Update Zip Code:")
        new_zip = collector.get_zip_code()
        if new_zip:
            update_data = {"zip_code": new_zip}
            if update_traveller(traveller_id, update_data):
                print("Zip code updated successfully!")
            else:
                print("Failed to update zip code.")
        else:
            print("Zip code cannot be empty. Update cancelled.")
    
    elif choice == 7:
        print("\n Update City:")
        new_city = collector.get_city()
        if new_city:
            update_data = {"city": new_city}
            if update_traveller(traveller_id, update_data):
                print("City updated successfully!")
            else:
                print("Failed to update city.")
        else:
            print("City cannot be empty. Update cancelled.")
    
    elif choice == 8:
        print("\n Update Email:")
        new_email = collector.get_email()
        if new_email:
            update_data = {"email": new_email}
            if update_traveller(traveller_id, update_data):
                print("Email updated successfully!")
            else:
                print("Failed to update email.")
        else:
            print("Email cannot be empty. Update cancelled.")
    
    elif choice == 9:
        print("\n Update Phone Number:")
        new_phone = collector.get_phone()
        if new_phone:
            update_data = {"mobile_phone": new_phone}
            if update_traveller(traveller_id, update_data):
                print("Phone number updated successfully!")
            else:
                print("Failed to update phone number.")
        else:
            print("Phone number cannot be empty. Update cancelled.")
    
    elif choice == 10:
        print("\n Update Driving License:")
        new_license = collector.get_driving_license()
        if new_license:
            update_data = {"driving_license": new_license}
            if update_traveller(traveller_id, update_data):
                print("Driving license updated successfully!")
            else:
                print("Failed to update driving license.")
        else:
            print("Driving license cannot be empty. Update cancelled.")
    
    elif choice == 11:
        print("Update cancelled.")
        return
    
    else:
        print("Invalid field selection. Please choose 1-11.")

def add_scooter_menu(current_user="unknown"):
    print("\n" + "=" * 50)
    print("    ADD NEW SCOOTER")
    print("=" * 50)
    print("Please provide the following information:")
    
    
    scooter_data = {}
    
    print("\n Basic Information:")
    scooter_data['brand'] = collector.get_brand()
    if not scooter_data['brand']:
        print("Brand is required. Operation cancelled.")
        return
    
    scooter_data['model'] = collector.get_model()
    if not scooter_data['model']:
        print("Model is required. Operation cancelled.")
        return
    
    scooter_data['serial_number'] = collector.get_serial_number()
    if not scooter_data['serial_number']:
        print("Serial number is required. Operation cancelled.")
        return
    
    print("\nPerformance Information:")
    scooter_data['top_speed'] = collector.get_top_speed()
    if not scooter_data['top_speed']:
        print("Top speed is required. Operation cancelled.")
        return
    
    scooter_data['battery_capacity'] = collector.get_battery_capacity()
    if not scooter_data['battery_capacity']:
        print("Battery capacity is required. Operation cancelled.")
        return
    
    scooter_data['state_of_charge'] = collector.get_state_of_charge()
    if not scooter_data['state_of_charge']:
        print("State of charge is required. Operation cancelled.")
        return
    
    print("\n Target Range Information:")
    target_min, target_max = collector.get_target_range(username=current_user, field_name="target_range")
    if target_min is None or target_max is None:
        print("Target range is required. Operation cancelled.")
        return
    scooter_data['target_range_min'] = target_min
    scooter_data['target_range_max'] = target_max
    
    print("\n Location Information:")
    lat, lon = collector.get_coordinates(username=current_user, field_name="coordinates")
    if lat is None or lon is None:
        print("Coordinates are required. Operation cancelled.")
        return
    scooter_data['latitude'] = lat
    scooter_data['longitude'] = lon
    
    print("\n Status Information:")
    scooter_data['out_of_service'] = collector.get_boolean_input("Is the scooter out of service?", username=current_user, field_name="out_of_service")
    
    scooter_data['mileage'] = collector.get_mileage()
    if not scooter_data['mileage']:
        print("Mileage is required. Operation cancelled.")
        return
    
    scooter_data['last_maintenance_date'] = collector.get_maintenance_date()
    if not scooter_data['last_maintenance_date']:
        print("Last maintenance date is required. Operation cancelled.")
        return
    
    print("\n Creating scooter...")
    if create_scooter(scooter_data):
        print("Scooter added successfully!")
    else:
        print("Failed to add scooter. Please check your input.")

def search_travellers_menu():
    search_term = collector.get_validated_input(
        "Enter search term (name, email, phone, or traveller ID): ",
        lambda x: (len(x) > 0, "Search term cannot be empty") if len(x) > 0 else (False, "Search term cannot be empty"),
        "Search term cannot be empty",
        username="unknown",
        field_name="search_term"
    )
    if search_term:
        search_travellers(search_term)

def search_scooters_menu():
    search_term = collector.get_validated_input(
        "Enter search term (brand, model, or serial number): ",
        lambda x: (len(x) > 0, "Search term cannot be empty") if len(x) > 0 else (False, "Search term cannot be empty"),
        "Search term cannot be empty",
        username="unknown",
        field_name="search_term"
    )
    if search_term:
        search_scooters(search_term)

def update_scooter_menu_service_engineer(username="unknown"):
    from crud_operations import list_scooters
    from database import get_connection, close_connection
    
    print("\n" + "=" * 60)
    print("    UPDATE SCOOTER (SERVICE ENGINEER)")
    print("=" * 60)
    print("WARNING: This will update scooter information!")
    print()
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM Scooters')
    count = cursor.fetchone()[0]
    close_connection(conn)
    
    if count == 0:
        print("📋 No scooters found in the system.")
        print("   Cannot update scooters when none exist.")
        return
    
    list_scooters()
    
    print("\nEnter the ID of the Scooter to update:")
    scooter_id = collector.get_validated_input(
        "Scooter ID: ",
        lambda x: (x.isdigit(), "Must be a number") if x.isdigit() else (False, "Must be a number"),
        "Invalid scooter ID. Must be a number.",
        username="unknown",
        field_name="scooter_id"
    )
    if not scooter_id:
        print("Scooter ID is required. Operation cancelled")
        return
    
    from crud_operations import update_scooter
    from database import get_connection, close_connection
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM Scooters WHERE id = ?', (int(scooter_id),))
    scooter_exists = cursor.fetchone()
    close_connection(conn)
    
    if not scooter_exists:
        print(f"No scooter found with ID {scooter_id}")
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
    
    choice = collector.get_menu_choice("Enter your choice (1-6): ", 6, username=username)
    
    if choice == 1:
        print("\nUpdate State of Charge:")
        new_value = collector.get_state_of_charge()
        if new_value is not None:
            update_data = {"state_of_charge": new_value}
            if update_scooter(int(scooter_id), update_data):
                print("State of charge updated successfully!")
            else:
                print("Failed to update state of charge.")
        else:
            print("Update cancelled.")
    
    elif choice == 2:
        print("\n Update Location:")
        lat, lon = collector.get_coordinates(username=username, field_name="coordinates")
        if lat is not None and lon is not None:
            update_data = {"latitude": lat, "longitude": lon}
            if update_scooter(int(scooter_id), update_data):
                print("Location updated successfully!")
            else:
                print("Failed to update location.")
        else:
            print("Update cancelled.")
    
    elif choice == 3:
        print("\n Update Out of Service Status:")
        new_value = collector.get_boolean_input("Is the scooter out of service?", username=username, field_name="out_of_service")
        update_data = {"out_of_service": new_value}
        if update_scooter(int(scooter_id), update_data):
            status = "out of service" if new_value else "in service"
            print(f"Scooter status updated to {status}!")
        else:
            print("Failed to update service status.")
    
    elif choice == 4:
        print("\nUpdate Mileage:")
        new_value = collector.get_mileage()
        if new_value is not None:
            update_data = {"mileage": new_value}
            if update_scooter(int(scooter_id), update_data):
                print("Mileage updated successfully!")
            else:
                print("Failed to update mileage.")
        else:
            print("Update cancelled.")
    
    elif choice == 5:
        print("\nUpdate Last Maintenance Date:")
        new_value = collector.get_maintenance_date()
        if new_value:
            update_data = {"last_maintenance_date": new_value}
            if update_scooter(int(scooter_id), update_data):
                print("Last maintenance date updated successfully!")
            else:
                print("Failed to update maintenance date.")
        else:
            print("Update cancelled.")
    
    elif choice == 6:
        print("Update cancelled.")
        return
    
    else:
        print("Invalid field selection. Please choose 1-6.")

def update_scooter_menu(username="unknown"):
    from crud_operations import list_scooters
    from database import get_connection, close_connection
    
    print("\n" + "=" * 60)
    print("UPDATE SCOOTER")
    print("=" * 60)
    print("WARNING: This will update scooter information!")
    print()
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM Scooters')
    count = cursor.fetchone()[0]
    close_connection(conn)
    
    if count == 0:
        print("No scooters found in the system.")
        print("Cannot update scooters when none exist.")
        return
    
    list_scooters()
    
    print("\nEnter the ID of the Scooter to update:")
    scooter_id = collector.get_validated_input(
        "Scooter ID: ",
        lambda x: (x.isdigit(), "Must be a number") if x.isdigit() else (False, "Must be a number"),
        "Invalid scooter ID. Must be a number.",
        username="unknown",
        field_name="scooter_id"
    )
    if not scooter_id:
        print("Scooter ID is required. Operation cancelled")
        return
    
    from crud_operations import update_scooter
    import sqlite3
    from database import get_connection, close_connection
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM Scooters WHERE id = ?', (int(scooter_id),))
    scooter_exists = cursor.fetchone()
    close_connection(conn)
    
    if not scooter_exists:
        print(f"No scooter found with ID {scooter_id}")
        return
    
    print("\n" + "=" * 50)
    print("UPDATE SCOOTER (SYSTEM ADMIN)")
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
    
    choice = collector.get_menu_choice("Enter your choice (1-12): ", 12, username=username)
    
    if choice == 1:
        print("\n Update Brand:")
        new_value = collector.get_brand()
        if new_value:
            update_data = {"brand": new_value}
            if update_scooter(int(scooter_id), update_data):
                print("Brand updated successfully!")
            else:
                print("Failed to update brand.")
        else:
            print("Update cancelled.")
    
    elif choice == 2:
        print("\n Update Model:")
        new_value = collector.get_model()
        if new_value:
            update_data = {"model": new_value}
            if update_scooter(int(scooter_id), update_data):
                print("Model updated successfully!")
            else:
                print("Failed to update model.")
        else:
            print("Update cancelled.")
    
    elif choice == 3:
        print("\n Update Serial Number:")
        new_value = collector.get_serial_number()
        if new_value:
            update_data = {"serial_number": new_value}
            if update_scooter(int(scooter_id), update_data):
                print("Serial number updated successfully!")
            else:
                print("Failed to update serial number.")
        else:
            print("Update cancelled.")
    
    elif choice == 4:
        print("\n Update Top Speed:")
        new_value = collector.get_top_speed()
        if new_value is not None:
            update_data = {"top_speed": new_value}
            if update_scooter(int(scooter_id), update_data):
                print("Top speed updated successfully!")
            else:
                print("Failed to update top speed.")
        else:
            print("Update cancelled.")
    
    elif choice == 5:
        print("\n Update Battery Capacity:")
        new_value = collector.get_battery_capacity()
        if new_value is not None:
            update_data = {"battery_capacity": new_value}
            if update_scooter(int(scooter_id), update_data):
                print("Battery capacity updated successfully!")
            else:
                print("Failed to update battery capacity.")
        else:
            print("Update cancelled.")
    
    elif choice == 6:
        print("\n Update State of Charge:")
        new_value = collector.get_state_of_charge()
        if new_value is not None:
            update_data = {"state_of_charge": new_value}
            if update_scooter(int(scooter_id), update_data):
                print("State of charge updated successfully!")
            else:
                print("Failed to update state of charge.")
        else:
            print("Update cancelled.")
    
    elif choice == 7:
        print("\n Update Target Range:")
        min_range, max_range = collector.get_target_range(username=username, field_name="target_range")
        if min_range is not None and max_range is not None:
            update_data = {"target_range_min": min_range, "target_range_max": max_range}
            if update_scooter(int(scooter_id), update_data):
                print("Target range updated successfully!")
            else:
                print("Failed to update target range.")
        else:
            print("Update cancelled.")
    
    elif choice == 8:
        print("\n Update Location:")
        lat, lon = collector.get_coordinates(username=username, field_name="coordinates")
        if lat is not None and lon is not None:
            update_data = {"latitude": lat, "longitude": lon}
            if update_scooter(int(scooter_id), update_data):
                print("Location updated successfully!")
            else:
                print("Failed to update location.")
        else:
            print("Update cancelled.")
    
    elif choice == 9:
        print("\n Update Out of Service Status:")
        new_value = collector.get_boolean_input("Is the scooter out of service?", username=username, field_name="out_of_service")
        update_data = {"out_of_service": new_value}
        if update_scooter(int(scooter_id), update_data):
            status = "out of service" if new_value else "in service"
            print(f"Scooter status updated to {status}!")
        else:
            print("Failed to update service status.")
    
    elif choice == 10:
        print("\n Update Mileage:")
        new_value = collector.get_mileage()
        if new_value is not None:
            update_data = {"mileage": new_value}
            if update_scooter(int(scooter_id), update_data):
                print("Mileage updated successfully!")
            else:
                print("Failed to update mileage.")
        else:
            print("Update cancelled.")
    
    elif choice == 11:
        print("\n Update Last Maintenance Date:")
        new_value = collector.get_maintenance_date()
        if new_value:
            update_data = {"last_maintenance_date": new_value}
            if update_scooter(int(scooter_id), update_data):
                print("Last maintenance date updated successfully!")
            else:
                print("Failed to update maintenance date.")
        else:
            print("Update cancelled.")
    
    elif choice == 12:
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
    print("WARNING: This action cannot be undone!")
    print()
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM Travellers')
    count = cursor.fetchone()[0]
    close_connection(conn)
    
    if count == 0:
        print("No travellers found in the system.")
        print("Cannot delete travellers when none exist.")
        return
    
    list_travellers()
    
    print("\nEnter the ID of the Traveller to delete:")
    traveller_id = get_validated_id("Traveller ID: ", "Traveller")
    if not traveller_id:
        print("Traveller ID is required. Operation cancelled")
        return
    
    from crud_operations import search_traveller_by_id
    traveller = search_traveller_by_id(traveller_id)
    if not traveller:
        print(f"No traveller found with ID {traveller_id}")
        return
    
    confirm = input(f"Are you sure you want to delete traveller {traveller_id}? (y/n): ")
    if confirm.lower() == 'y':
        delete_traveller(traveller_id)
    else:
        print("Deletion cancelled.")

def delete_scooter_menu():
    from crud_operations import list_scooters
    from database import get_connection, close_connection
    
    print("\n" + "=" * 60)
    print("DELETE SCOOTER")
    print("=" * 60)
    print("WARNING: This action cannot be undone!")
    print()
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM Scooters')
    count = cursor.fetchone()[0]
    close_connection(conn)
    
    if count == 0:
        print("No scooters found in the system.")
        print("Cannot delete scooters when none exist.")
        return
    
    list_scooters()
    
    print("\nEnter the ID of the Scooter to delete:")
    scooter_id = collector.get_validated_input(
        "Scooter ID: ",
        lambda x: (x.isdigit(), "Must be a number") if x.isdigit() else (False, "Must be a number"),
        "Invalid scooter ID. Must be a number.",
        username="unknown",
        field_name="scooter_id"
    )
    if not scooter_id:
        print("Scooter ID is required. Operation cancelled")
        return
    
    from database import get_connection, close_connection
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM Scooters WHERE id = ?', (int(scooter_id),))
    scooter_exists = cursor.fetchone()
    close_connection(conn)
    
    if not scooter_exists:
        print(f"No scooter found with ID {scooter_id}")
        return
    
    confirm = input(f"Are you sure you want to delete scooter {scooter_id}? (y/n): ")
    if confirm.lower() == 'y':
        delete_scooter(int(scooter_id))
    else:
        print("Deletion cancelled.")

def add_system_admin(current_user):
    print("\n" + "=" * 50)
    print("    ADD SYSTEM ADMINISTRATOR")
    print("=" * 50)
    print("Please provide the following information:")
    
    from database import get_connection, close_connection
    from encryption import encrypt_data
    
    print("\n User Information:")
    
    while True:
        username = collector.get_username()
        if not username:
            print("Username entry cancelled.")
            return
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT id, username FROM Users')
            all_users = cursor.fetchall()
            
            existing_user = None
            for existing_id, existing_username in all_users:
                try:
                    decrypted_username = decrypt_data(existing_username)
                    if decrypted_username.lower() == username.lower():
                        existing_user = (existing_id, existing_username)
                        break
                except:
                    if existing_username.lower() == username.lower():
                        existing_user = (existing_id, existing_username)
                        break
            close_connection(conn)
            
            if existing_user:
                print(f"Username '{username}' is already taken. Please choose a different username.")
                continue
            else:
                print(f"Username '{username}' is available!")
                break
                
        except Exception as e:
            print(f"Error checking username availability: {e}")
            print("Please try again.")
            continue
    
    password = collector.get_password()
    if not password:
        print("Password entry cancelled.")
        return
    
    first_name = collector.get_validated_input(
        "First Name: ", 
        lambda x: validator.validate_pattern(x, 'name', 'first name'),
        "Invalid first name format",
        username=current_user,
        field_name="first_name"
    )
    if not first_name:
        print("First name is required. Operation cancelled.")
        return
    
    last_name = collector.get_validated_input(
        "Last Name: ", 
        lambda x: validator.validate_pattern(x, 'name', 'last name'),
        "Invalid last name format",
        username=current_user,
        field_name="last_name"
    )
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
    
    from database import get_connection, close_connection
    from encryption import encrypt_data
    
    print("\n User Information:")
    
    while True:
        username = collector.get_username()
        if not username:
            print("Username entry cancelled.")
            return
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT id, username FROM Users')
            all_users = cursor.fetchall()
            
            existing_user = None
            for existing_id, existing_username in all_users:
                try:
                    decrypted_username = decrypt_data(existing_username)
                    if decrypted_username.lower() == username.lower():
                        existing_user = (existing_id, existing_username)
                        break
                except:
                    if existing_username.lower() == username.lower():
                        existing_user = (existing_id, existing_username)
                        break
            close_connection(conn)
            
            if existing_user:
                print(f"Username '{username}' is already taken. Please choose a different username.")
                continue
            else:
                print(f"Username '{username}' is available!")
                break
                
        except Exception as e:
            print(f"Error checking username availability: {e}")
            print("Please try again.")
            continue
    
    password = collector.get_password()
    if not password:
        print("Password is required. Operation cancelled.")
        return
    
    first_name = collector.get_validated_input(
        "First Name: ", 
        lambda x: validator.validate_pattern(x, 'name', 'first name'),
        "Invalid first name format",
        username=current_user,
        field_name="first_name"
    )
    if not first_name:
        print("First name is required. Operation cancelled.")
        return
    
    last_name = collector.get_validated_input(
        "Last Name: ", 
        lambda x: validator.validate_pattern(x, 'name', 'last name'),
        "Invalid last name format",
        username=current_user,
        field_name="last_name"
    )
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
    print("\n=== SERVICE ENGINEERS ===")
    list_users("super_admin")

def delete_my_account_menu(current_user):
    from database import get_connection, close_connection
    from crud_operations import delete_user_by_id
    from session_management import get_current_user_id
    
    print("\n" + "=" * 60)
    print("    DELETE MY ACCOUNT")
    print("=" * 60)
    print("WARNING: This action cannot be undone!")
    print("You will be permanently removed from the system!")
    print()

    user_id = get_current_user_id(current_user)
    
    if not user_id:
        print("ERROR: Could not find your user account.")
        return
    
    from encryption import decrypt_data
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT role FROM Users WHERE id = ?', (user_id,))
    user_data = cursor.fetchone()
    close_connection(conn)
    
    if not user_data:
        print("ERROR: Could not find your user account in database.")
        return
    
    try:
        decrypted_role = decrypt_data(user_data[0])
    except:
        decrypted_role = user_data[0]
    
    if decrypted_role == "Super Admin":
        print("ERROR: Operation not permitted.")
        print("This is a security measure to prevent system lockout.")
        return
    
    print("Your Account Information:")
    print(f"Username: {current_user}")
    print(f"User ID: {user_id}")
    print(f"Role: {decrypted_role}")
    print()

    confirm = input("Are you sure you want to delete your account? (y/n): ")
    if confirm.lower() != 'y':
        print("Account deletion cancelled.")
        return
    
    if delete_user_by_id(user_id, current_user, decrypted_role):
        print("Your account has been deleted successfully!")
        print("The system will now close.")
        sys.exit(0)
    else:
        print("Failed to delete your account.")

def delete_system_admin():
    from database import get_connection, close_connection
    
    print("\n" + "=" * 60)
    print(" DELETE SYSTEM ADMINISTRATOR")
    print("=" * 60)
    print("WARNING: This action cannot be undone!")
    print("Super Admin account cannot be deleted.")
    print()
    
    from crud_operations import count_users_by_role
    count = count_users_by_role("System Admin")
    
    if count == 0:
        print("No System Administrators found in the system.")
        print("   Cannot delete System Administrators when none exist.")
        return
    
    from crud_operations import list_system_admins
    list_system_admins("super_admin")
    
    print("\nEnter the ID of the System Administrator to delete:")
    user_id = input("User ID: ")
    
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
    print("WARNING: This action cannot be undone!")
    print()
    
    from crud_operations import count_users_by_role
    count = count_users_by_role("Service Engineer")
    
    if count == 0:
        print("No Service Engineers found in the system.")
        print("   Cannot delete Service Engineers when none exist.")
        return
    
    from crud_operations import list_service_engineers
    list_service_engineers("super_admin")
    
    print("\nEnter the ID of the Service Engineer to delete:")
    user_id = input("User ID: ")
    
    if not user_id:
        print("User ID is required.")
        return
    
    try:
        user_id = int(user_id)
        delete_user_by_id(user_id, "super_admin", "Service Engineer")
    except ValueError:
        print("Invalid user ID. Please enter a number.")
        return

def reset_system_admin_password_menu():
    from crud_operations import list_system_admins, reset_user_password
    from database import get_connection, close_connection
    
    print("\n" + "=" * 60)
    print("    RESET SYSTEM ADMIN PASSWORD")
    print("=" * 60)
    print("WARNING: This will generate a temporary password!")
    print("The user will be forced to change it on next login.")
    print()
    
    from crud_operations import count_users_by_role
    count = count_users_by_role("System Admin")
    
    if count == 0:
        print("No System Administrators found in the system.")
        print("   Cannot reset passwords when none exist.")
        return
    
    list_system_admins("super_admin")
    
    print("\nEnter the ID of the System Administrator to reset password:")
    user_id = input("User ID: ")
    
    if not user_id:
        print("User ID is required.")
        return
    
    try:
        user_id = int(user_id)
        
        from crud_operations import validate_user_exists_with_role
        is_valid, username, role = validate_user_exists_with_role(user_id, "System Admin")
        if not is_valid:
            return
        
        print(f"\nWARNING: This will reset the password for System Admin ID {user_id}")
        print("A temporary password will be generated and the user must change it on next login.")
        
        confirm = input("Are you sure you want to proceed? (y/n): ")
        if confirm.lower() != 'y':
            print("Password reset cancelled.")
            return
        
        if reset_user_password(user_id, "super_admin"):
            print("\nPassword reset completed successfully!")
        else:
            print("\nPassword reset failed.")
            
    except ValueError:
        print("Invalid user ID. Please enter a number.")
        return

def reset_service_engineer_password_menu():
    from crud_operations import list_service_engineers, reset_user_password
    from database import get_connection, close_connection
    
    print("\n" + "=" * 60)
    print("    RESET SERVICE ENGINEER PASSWORD")
    print("=" * 60)
    print("WARNING: This will generate a temporary password!")
    print("The user will be forced to change it on next login.")
    print()
    
    from crud_operations import count_users_by_role
    count = count_users_by_role("Service Engineer")
    
    if count == 0:
        print("No Service Engineers found in the system.")
        print("   Cannot reset passwords when none exist.")
        return
    
    list_service_engineers("super_admin")
    
    print("\nEnter the ID of the Service Engineer to reset password:")
    user_id = input("User ID: ")
    
    if not user_id:
        print("User ID is required.")
        return
    
    try:
        user_id = int(user_id)
        
        from crud_operations import validate_user_exists_with_role
        is_valid, username, role = validate_user_exists_with_role(user_id, "Service Engineer")
        if not is_valid:
            return
        
        print(f"\nWARNING: This will reset the password for Service Engineer ID {user_id}")
        print("A temporary password will be generated and the user must change it on next login.")
        
        confirm = input("Are you sure you want to proceed? (y/n): ")
        if confirm.lower() != 'y':
            print("Password reset cancelled.")
            return
        
        if reset_user_password(user_id, "super_admin"):
            print("\nPassword reset completed successfully!")
        else:
            print("\nPassword reset failed.")
            
    except ValueError:
        print("Invalid user ID. Please enter a number.")
        return

def view_logs(username):
    print("\n=== SYSTEM LOGS ===")
    print("1. View All Logs")
    print("2. View Suspicious Activities")
    print("3. Back")
    
    choice = collector.get_menu_choice("Enter your choice (1-3): ", 3, username=username, field_name="log_menu_choice")
    
    if choice == 1:
        from system_logging import display_logs_paginated
        display_logs_paginated()
    elif choice == 2:
        from system_logging import display_suspicious_logs_paginated
        display_suspicious_logs_paginated(username)

def generate_restore_code_menu(username):
    from crud_operations import list_system_admins
    from database import get_connection, close_connection
    from encryption import decrypt_data
    
    print("\n" + "=" * 60)
    print("    GENERATE RESTORE CODE")
    print("=" * 60)
    print("Select a System Administrator for the restore code:")
    print()
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, username, first_name, last_name, role
            FROM Users
            ORDER BY registration_date DESC
        ''')
        
        all_users = cursor.fetchall()
        close_connection(conn)
        
        system_admins = []
        for user_id, username, first_name, last_name, role in all_users:
            try:
                decrypted_username = decrypt_data(username)
                decrypted_role = decrypt_data(role)
                if decrypted_role == 'System Admin' and decrypted_username != 'super_admin':
                    system_admins.append((user_id, username, first_name, last_name))
            except:
                if role == 'System Admin' and username != 'super_admin':
                    system_admins.append((user_id, username, first_name, last_name))
        
        if not system_admins:
            print("No System Administrators found in the system.")
            print("Note: Super Admin account cannot be used for restore codes.")
            return
        
        print("Available System Administrators:")
        print("-" * 60)
        print(f"{'No.':<4} {'ID':<5} {'Username':<15} {'Name':<25}")
        print("-" * 60)
        
        admin_list = []
        for i, (user_id, username, first_name, last_name) in enumerate(system_admins, 1):
            try:
                decrypted_username = decrypt_data(username)
                decrypted_first = decrypt_data(first_name)
                decrypted_last = decrypt_data(last_name)
                full_name = f"{decrypted_first} {decrypted_last}"
            except:
                decrypted_username = username
                full_name = f"{first_name} {last_name}"
            
            admin_list.append(decrypted_username)
            print(f"{i:<4} {user_id:<5} {decrypted_username:<15} {full_name:<25}")
        
        print("-" * 60)
        
        choice = collector.get_validated_input(
            f"Select System Administrator (1-{len(system_admins)}): ",
            lambda x: (x.isdigit() and 1 <= int(x) <= len(system_admins), f"Please enter a number between 1 and {len(system_admins)}") if x.isdigit() and 1 <= int(x) <= len(system_admins) else (False, f"Please enter a number between 1 and {len(system_admins)}"),
            f"Please enter a number between 1 and {len(system_admins)}",
            username=username,
            field_name="system_admin_choice"
        )
        
        if not choice:
            print("Selection cancelled.")
            return
        
        selected_admin = admin_list[int(choice) - 1]
        print(f"\nSelected System Administrator: {selected_admin}")
        
    except Exception as e:
        print(f"Error retrieving System Administrators: {e}")
        return
    
    backup_files = list_backups()
    if not backup_files:
        print("No backup files found. Create a backup first.")
        return
    
    print("\nAvailable backups:")
    print("-" * 40)
    for i, backup in enumerate(backup_files, 1):
        print(f"{i}. {backup}")
    print("-" * 40)
    
    backup_choice = collector.get_validated_input(
        f"Select backup (1-{len(backup_files)}): ",
        lambda x: (x.isdigit() and 1 <= int(x) <= len(backup_files), f"Please enter a number between 1 and {len(backup_files)}") if x.isdigit() and 1 <= int(x) <= len(backup_files) else (False, f"Please enter a number between 1 and {len(backup_files)}"),
        f"Please enter a number between 1 and {len(backup_files)}",
        username=username,
        field_name="backup_choice"
    )
    
    if backup_choice and backup_choice.isdigit() and 1 <= int(backup_choice) <= len(backup_files):
        backup_file = backup_files[int(backup_choice) - 1]
        print(f"\nSelected backup: {backup_file}")
        print(f"Generating restore code for: {selected_admin}")
        generate_restore_code(selected_admin, backup_file)
    else:
        print("Invalid backup selection.")

def revoke_restore_code_menu(username):
    code = collector.get_validated_input(
        "Enter restore code to revoke: ",
        lambda x: (len(x) > 0, "Restore code cannot be empty") if len(x) > 0 else (False, "Restore code cannot be empty"),
        "Restore code cannot be empty",
        username=username,
        field_name="restore_code"
    )
    if not code:
        print("Restore code cannot be empty")
        return
    revoke_restore_code(code)

def restore_backup_menu(username):
    code = collector.get_validated_input(
        "Enter restore code: ",
        lambda x: (len(x) > 0, "Restore code cannot be empty") if len(x) > 0 else (False, "Restore code cannot be empty"),
        "Restore code cannot be empty",
        username=username,
        field_name="restore_code"
    )
    if not code:
        print("Restore code cannot be empty")
        return
    restore_backup(code, username)

if __name__ == "__main__":
    main()
