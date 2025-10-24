"""
Urban Mobility Backend System - Main Application
Console-based interface for managing scooter network
"""

import os
import sys
from database import initialize_db
from authentication import login, change_password
from system_logging import log_action, check_suspicious_activities, get_logs, get_suspicious_logs
from backup import create_backup, generate_restore_code, restore_backup, list_backups, revoke_restore_code, list_restore_codes
from crud_operations import *
from input_validation import *

def exit_system(username):
    """Properly exit the system with cleanup"""
    print("\nExiting Urban Mobility Backend System...")
    log_action(username, "System exit")
    print("Thank you for using Urban Mobility Backend System!")
    sys.exit(0)

def main():
    """Main application entry point"""
    print("=" * 60)
    print("    URBAN MOBILITY BACKEND SYSTEM")
    print("    Secure Scooter Network Management")
    print("=" * 60)
    
    # Initialize database
    initialize_db()
    
    # Login
    username, role = login()
    if not username:
        print("Login failed. Exiting system.")
        return
    
    # Check for suspicious activities
    suspicious_count = check_suspicious_activities()
    if suspicious_count > 0:
        print(f"\n⚠️  ALERT: {suspicious_count} suspicious activities detected in the last 24 hours!")
        print("Please review the logs for details.")
    
    # Log successful login
    log_action(username, "Logged in successfully")
    
    # Display role-based menu
    while True:
        try:
            if role == "Super Admin":
                super_admin_menu(username)
            elif role == "System Admin":
                system_admin_menu(username)
            elif role == "Service Engineer":
                service_engineer_menu(username)
            else:
                print("Invalid role. Exiting system.")
                break
        except KeyboardInterrupt:
            exit_system(username)
        except Exception as e:
            print(f"An error occurred: {e}")
            log_action(username, f"System error: {e}", suspicious=True)

def super_admin_menu(username):
    """Super Admin menu"""
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
        print("10. Exit System")
        print("-" * 50)
        
        choice = input("Enter your choice (1-10): ").strip()
        
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
            exit_system(username)
        else:
            print("Invalid choice. Please try again.")

def system_admin_menu(username):
    """System Admin menu"""
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
            list_users(username)
        elif choice == "9":
            exit_system(username)
        else:
            print("Invalid choice. Please try again.")

def service_engineer_menu(username):
    """Service Engineer menu"""
    while True:
        print("\n" + "=" * 50)
        print("    SERVICE ENGINEER MENU")
        print("=" * 50)
        print("1.  Change Password")
        print("2.  Search Scooters")
        print("3.  Update Scooter Information")
        print("4.  Exit System")
        print("-" * 50)
        
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == "1":
            change_password(username)
        elif choice == "2":
            search_scooters_menu()
        elif choice == "3":
            update_scooter_menu_service_engineer()
        elif choice == "4":
            exit_system(username)
        else:
            print("Invalid choice. Please try again.")

def manage_system_admins(username):
    """Manage System Administrators"""
    while True:
        print("\n=== MANAGE SYSTEM ADMINISTRATORS ===")
        print("1. Add System Administrator")
        print("2. List System Administrators")
        print("3. Delete System Administrator")
        print("4. Reset Password")
        print("5. Back to Main Menu")
        
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == "1":
            add_system_admin(username)
        elif choice == "2":
            list_system_admins()
        elif choice == "3":
            delete_system_admin()
        elif choice == "4":
            reset_password_menu()
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")

def manage_service_engineers(username):
    """Manage Service Engineers"""
    while True:
        print("\n=== MANAGE SERVICE ENGINEERS ===")
        print("1. Add Service Engineer")
        print("2. List Service Engineers")
        print("3. Delete Service Engineer")
        print("4. Reset Password")
        print("5. Back to Main Menu")
        
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == "1":
            add_service_engineer(username)
        elif choice == "2":
            list_service_engineers()
        elif choice == "3":
            delete_service_engineer()
        elif choice == "4":
            reset_password_menu()
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")

def manage_travellers(username):
    """Manage Travellers"""
    while True:
        print("\n=== MANAGE TRAVELLERS ===")
        print("1. Add Traveller")
        print("2. Search Travellers")
        print("3. Delete Traveller")
        print("4. Back to Main Menu")
        
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == "1":
            add_traveller_menu()
        elif choice == "2":
            search_travellers_menu()
        elif choice == "3":
            delete_traveller_menu()
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")

def manage_scooters(username):
    """Manage Scooters"""
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
    """Add new traveller interface with guided input"""
    print("\n" + "=" * 50)
    print("    ADD NEW TRAVELLER")
    print("=" * 50)
    print("Please provide the following information:")
    
    from input_validation import get_birthday, get_gender, get_zip_code, get_city, get_email, get_phone, get_driving_license
    
    traveller_data = {}
    
    # Collect traveller information with validation
    print("\n📝 Personal Information:")
    traveller_data['first_name'] = input("👤 First Name: ").strip()
    if not traveller_data['first_name']:
        print("❌ First name is required. Operation cancelled.")
        return
    
    traveller_data['last_name'] = input("👤 Last Name: ").strip()
    if not traveller_data['last_name']:
        print("❌ Last name is required. Operation cancelled.")
        return
    
    traveller_data['birthday'] = get_birthday()
    if not traveller_data['birthday']:
        print("❌ Birthday is required. Operation cancelled.")
        return
    
    traveller_data['gender'] = get_gender()
    if not traveller_data['gender']:
        print("❌ Gender is required. Operation cancelled.")
        return
    
    print("\n🏠 Address Information:")
    traveller_data['street_name'] = input("🏠 Street Name: ").strip()
    if not traveller_data['street_name']:
        print("❌ Street name is required. Operation cancelled.")
        return
    
    traveller_data['house_number'] = input("🏠 House Number: ").strip()
    if not traveller_data['house_number']:
        print("❌ House number is required. Operation cancelled.")
        return
    
    traveller_data['zip_code'] = get_zip_code()
    if not traveller_data['zip_code']:
        print("❌ Zip code is required. Operation cancelled.")
        return
    
    traveller_data['city'] = get_city()
    if not traveller_data['city']:
        print("❌ City is required. Operation cancelled.")
        return
    
    print("\n📞 Contact Information:")
    traveller_data['email'] = get_email()
    if not traveller_data['email']:
        print("❌ Email is required. Operation cancelled.")
        return
    
    traveller_data['mobile_phone'] = get_phone()
    if not traveller_data['mobile_phone']:
        print("❌ Mobile phone is required. Operation cancelled.")
        return
    
    print("\n🚗 License Information:")
    traveller_data['driving_license'] = get_driving_license()
    if not traveller_data['driving_license']:
        print("❌ Driving license is required. Operation cancelled.")
        return
    
    # Create traveller
    print("\n🔄 Creating traveller...")
    if create_traveller(traveller_data):
        print("✅ Traveller added successfully!")
    else:
        print("❌ Failed to add traveller. Please check your input.")

def add_scooter_menu():
    """Add new scooter interface with comprehensive validation"""
    print("\n" + "=" * 50)
    print("    ADD NEW SCOOTER")
    print("=" * 50)
    print("Please provide the following information:")
    
    from input_validation import (get_brand, get_model, get_serial_number, get_top_speed, 
                                get_battery_capacity, get_state_of_charge, get_target_range,
                                get_coordinates, get_boolean_input, get_mileage, get_maintenance_date)
    
    scooter_data = {}
    
    # Collect scooter information with comprehensive validation
    print("\n🏍️ Basic Information:")
    scooter_data['brand'] = get_brand()
    if not scooter_data['brand']:
        print("❌ Brand is required. Operation cancelled.")
        return
    
    scooter_data['model'] = get_model()
    if not scooter_data['model']:
        print("❌ Model is required. Operation cancelled.")
        return
    
    scooter_data['serial_number'] = get_serial_number()
    if not scooter_data['serial_number']:
        print("❌ Serial number is required. Operation cancelled.")
        return
    
    print("\n⚡ Performance Information:")
    scooter_data['top_speed'] = get_top_speed()
    if not scooter_data['top_speed']:
        print("❌ Top speed is required. Operation cancelled.")
        return
    
    scooter_data['battery_capacity'] = get_battery_capacity()
    if not scooter_data['battery_capacity']:
        print("❌ Battery capacity is required. Operation cancelled.")
        return
    
    scooter_data['state_of_charge'] = get_state_of_charge()
    if not scooter_data['state_of_charge']:
        print("❌ State of charge is required. Operation cancelled.")
        return
    
    print("\n🎯 Target Range Information:")
    target_min, target_max = get_target_range()
    if target_min is None or target_max is None:
        print("❌ Target range is required. Operation cancelled.")
        return
    scooter_data['target_range_min'] = target_min
    scooter_data['target_range_max'] = target_max
    
    print("\n📍 Location Information:")
    lat, lon = get_coordinates()
    if lat is None or lon is None:
        print("❌ Coordinates are required. Operation cancelled.")
        return
    scooter_data['latitude'] = lat
    scooter_data['longitude'] = lon
    
    print("\n🔧 Status Information:")
    scooter_data['out_of_service'] = get_boolean_input("🚫 Is the scooter out of service?")
    
    scooter_data['mileage'] = get_mileage()
    if not scooter_data['mileage']:
        print("❌ Mileage is required. Operation cancelled.")
        return
    
    scooter_data['last_maintenance_date'] = get_maintenance_date()
    if not scooter_data['last_maintenance_date']:
        print("❌ Last maintenance date is required. Operation cancelled.")
        return
    
    # Create scooter
    print("\n🔄 Creating scooter...")
    if create_scooter(scooter_data):
        print("✅ Scooter added successfully!")
    else:
        print("❌ Failed to add scooter. Please check your input.")

def search_travellers_menu():
    """Search travellers interface"""
    search_term = input("Enter search term (name, email, phone, or customer ID): ").strip()
    if search_term:
        search_travellers(search_term)

def search_scooters_menu():
    """Search scooters interface"""
    search_term = input("Enter search term (brand, model, or serial number): ").strip()
    if search_term:
        search_scooters(search_term)

def update_scooter_menu_service_engineer():
    """Update scooter interface for Service Engineers (limited fields)"""
    from input_validation import (get_state_of_charge, get_coordinates, get_boolean_input, 
                                get_mileage, get_maintenance_date)
    
    scooter_id = input("Enter Scooter ID to update: ").strip()
    if not scooter_id.isdigit():
        print("❌ Invalid scooter ID. Must be a number.")
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
        # State of Charge
        print("\n🔋 Update State of Charge:")
        new_value = get_state_of_charge()
        if new_value is not None:
            update_data = {"state_of_charge": new_value}
            if update_scooter(int(scooter_id), update_data):
                print("✅ State of charge updated successfully!")
            else:
                print("❌ Failed to update state of charge.")
        else:
            print("❌ Update cancelled.")
    
    elif field_choice == "2":
        # Location (Coordinates)
        print("\n📍 Update Location:")
        lat, lon = get_coordinates()
        if lat is not None and lon is not None:
            update_data = {"latitude": lat, "longitude": lon}
            if update_scooter(int(scooter_id), update_data):
                print("✅ Location updated successfully!")
            else:
                print("❌ Failed to update location.")
        else:
            print("❌ Update cancelled.")
    
    elif field_choice == "3":
        # Out of Service Status
        print("\n🚫 Update Out of Service Status:")
        new_value = get_boolean_input("Is the scooter out of service?")
        update_data = {"out_of_service": new_value}
        if update_scooter(int(scooter_id), update_data):
            status = "out of service" if new_value else "in service"
            print(f"✅ Scooter status updated to {status}!")
        else:
            print("❌ Failed to update service status.")
    
    elif field_choice == "4":
        # Mileage
        print("\n📏 Update Mileage:")
        new_value = get_mileage()
        if new_value is not None:
            update_data = {"mileage": new_value}
            if update_scooter(int(scooter_id), update_data):
                print("✅ Mileage updated successfully!")
            else:
                print("❌ Failed to update mileage.")
        else:
            print("❌ Update cancelled.")
    
    elif field_choice == "5":
        # Last Maintenance Date
        print("\n🔧 Update Last Maintenance Date:")
        new_value = get_maintenance_date()
        if new_value:
            update_data = {"last_maintenance_date": new_value}
            if update_scooter(int(scooter_id), update_data):
                print("✅ Last maintenance date updated successfully!")
            else:
                print("❌ Failed to update maintenance date.")
        else:
            print("❌ Update cancelled.")
    
    elif field_choice == "6":
        print("❌ Update cancelled.")
        return
    
    else:
        print("❌ Invalid field selection. Please choose 1-6.")

def update_scooter_menu():
    """Update scooter interface for System Admins (all fields)"""
    from input_validation import (get_brand, get_model, get_serial_number, get_top_speed,
                                get_battery_capacity, get_state_of_charge, get_target_range,
                                get_coordinates, get_boolean_input, get_mileage, get_maintenance_date)
    
    scooter_id = input("Enter Scooter ID to update: ").strip()
    if not scooter_id.isdigit():
        print("❌ Invalid scooter ID. Must be a number.")
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
        # Brand
        print("\n🏍️ Update Brand:")
        new_value = get_brand()
        if new_value:
            update_data = {"brand": new_value}
            if update_scooter(int(scooter_id), update_data):
                print("✅ Brand updated successfully!")
            else:
                print("❌ Failed to update brand.")
        else:
            print("❌ Update cancelled.")
    
    elif field_choice == "2":
        # Model
        print("\n🏍️ Update Model:")
        new_value = get_model()
        if new_value:
            update_data = {"model": new_value}
            if update_scooter(int(scooter_id), update_data):
                print("✅ Model updated successfully!")
            else:
                print("❌ Failed to update model.")
        else:
            print("❌ Update cancelled.")
    
    elif field_choice == "3":
        # Serial Number
        print("\n🔢 Update Serial Number:")
        new_value = get_serial_number()
        if new_value:
            update_data = {"serial_number": new_value}
            if update_scooter(int(scooter_id), update_data):
                print("✅ Serial number updated successfully!")
            else:
                print("❌ Failed to update serial number.")
        else:
            print("❌ Update cancelled.")
    
    elif field_choice == "4":
        # Top Speed
        print("\n⚡ Update Top Speed:")
        new_value = get_top_speed()
        if new_value is not None:
            update_data = {"top_speed": new_value}
            if update_scooter(int(scooter_id), update_data):
                print("✅ Top speed updated successfully!")
            else:
                print("❌ Failed to update top speed.")
        else:
            print("❌ Update cancelled.")
    
    elif field_choice == "5":
        # Battery Capacity
        print("\n🔋 Update Battery Capacity:")
        new_value = get_battery_capacity()
        if new_value is not None:
            update_data = {"battery_capacity": new_value}
            if update_scooter(int(scooter_id), update_data):
                print("✅ Battery capacity updated successfully!")
            else:
                print("❌ Failed to update battery capacity.")
        else:
            print("❌ Update cancelled.")
    
    elif field_choice == "6":
        # State of Charge
        print("\n🔋 Update State of Charge:")
        new_value = get_state_of_charge()
        if new_value is not None:
            update_data = {"state_of_charge": new_value}
            if update_scooter(int(scooter_id), update_data):
                print("✅ State of charge updated successfully!")
            else:
                print("❌ Failed to update state of charge.")
        else:
            print("❌ Update cancelled.")
    
    elif field_choice == "7":
        # Target Range
        print("\n🎯 Update Target Range:")
        min_range, max_range = get_target_range()
        if min_range is not None and max_range is not None:
            update_data = {"target_range_min": min_range, "target_range_max": max_range}
            if update_scooter(int(scooter_id), update_data):
                print("✅ Target range updated successfully!")
            else:
                print("❌ Failed to update target range.")
        else:
            print("❌ Update cancelled.")
    
    elif field_choice == "8":
        # Location (Coordinates)
        print("\n📍 Update Location:")
        lat, lon = get_coordinates()
        if lat is not None and lon is not None:
            update_data = {"latitude": lat, "longitude": lon}
            if update_scooter(int(scooter_id), update_data):
                print("✅ Location updated successfully!")
            else:
                print("❌ Failed to update location.")
        else:
            print("❌ Update cancelled.")
    
    elif field_choice == "9":
        # Out of Service Status
        print("\n🚫 Update Out of Service Status:")
        new_value = get_boolean_input("Is the scooter out of service?")
        update_data = {"out_of_service": new_value}
        if update_scooter(int(scooter_id), update_data):
            status = "out of service" if new_value else "in service"
            print(f"✅ Scooter status updated to {status}!")
        else:
            print("❌ Failed to update service status.")
    
    elif field_choice == "10":
        # Mileage
        print("\n📏 Update Mileage:")
        new_value = get_mileage()
        if new_value is not None:
            update_data = {"mileage": new_value}
            if update_scooter(int(scooter_id), update_data):
                print("✅ Mileage updated successfully!")
            else:
                print("❌ Failed to update mileage.")
        else:
            print("❌ Update cancelled.")
    
    elif field_choice == "11":
        # Last Maintenance Date
        print("\n🔧 Update Last Maintenance Date:")
        new_value = get_maintenance_date()
        if new_value:
            update_data = {"last_maintenance_date": new_value}
            if update_scooter(int(scooter_id), update_data):
                print("✅ Last maintenance date updated successfully!")
            else:
                print("❌ Failed to update maintenance date.")
        else:
            print("❌ Update cancelled.")
    
    elif field_choice == "12":
        print("❌ Update cancelled.")
        return
    
    else:
        print("❌ Invalid field selection. Please choose 1-12.")

def delete_traveller_menu():
    """Delete traveller interface"""
    customer_id = input("Enter Customer ID to delete: ").strip()
    if customer_id:
        confirm = input(f"Are you sure you want to delete traveller {customer_id}? (y/n): ").strip().lower()
        if confirm == 'y':
            delete_traveller(customer_id)

def delete_scooter_menu():
    """Delete scooter interface"""
    scooter_id = input("Enter Scooter ID to delete: ").strip()
    if scooter_id.isdigit():
        confirm = input(f"Are you sure you want to delete scooter {scooter_id}? (y/n): ").strip().lower()
        if confirm == 'y':
            delete_scooter(int(scooter_id))

def add_system_admin(current_user):
    """Add System Administrator with guided input"""
    print("\n" + "=" * 50)
    print("    ADD SYSTEM ADMINISTRATOR")
    print("=" * 50)
    print("Please provide the following information:")
    
    from input_validation import get_username, get_password, get_first_name, get_last_name
    
    print("\n👤 User Information:")
    username = get_username()
    if not username:
        print("❌ Username is required. Operation cancelled.")
        return
    
    password = get_password()
    if not password:
        print("❌ Password is required. Operation cancelled.")
        return
    
    first_name = input("👤 First Name: ").strip()
    if not first_name:
        print("❌ First name is required. Operation cancelled.")
        return
    
    last_name = input("👤 Last Name: ").strip()
    if not last_name:
        print("❌ Last name is required. Operation cancelled.")
        return
    
    print("\n🔄 Creating System Administrator...")
    # Hash the password
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
        print("✅ System Administrator created successfully!")
    else:
        print("❌ Failed to create System Administrator.")

def add_service_engineer(current_user):
    """Add Service Engineer with guided input"""
    print("\n" + "=" * 50)
    print("    ADD SERVICE ENGINEER")
    print("=" * 50)
    print("Please provide the following information:")
    
    from input_validation import get_username, get_password, get_first_name, get_last_name
    
    print("\n👤 User Information:")
    username = get_username()
    if not username:
        print("❌ Username is required. Operation cancelled.")
        return
    
    password = get_password()
    if not password:
        print("❌ Password is required. Operation cancelled.")
        return
    
    first_name = input("👤 First Name: ").strip()
    if not first_name:
        print("❌ First name is required. Operation cancelled.")
        return
    
    last_name = input("👤 Last Name: ").strip()
    if not last_name:
        print("❌ Last name is required. Operation cancelled.")
        return
    
    print("\n🔄 Creating Service Engineer...")
    # Hash the password
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
        print("✅ Service Engineer created successfully!")
    else:
        print("❌ Failed to create Service Engineer.")

def list_system_admins():
    """List System Administrators"""
    print("\n=== SYSTEM ADMINISTRATORS ===")
    # Implementation to filter and show only System Admins
    list_users("super_admin")

def list_service_engineers():
    """List Service Engineers"""
    print("\n=== SERVICE ENGINEERS ===")
    # Implementation to filter and show only Service Engineers
    list_users("super_admin")

def delete_system_admin():
    """Delete System Administrator"""
    username = input("Enter username to delete: ").strip()
    delete_user(username, "super_admin")

def delete_service_engineer():
    """Delete Service Engineer"""
    username = input("Enter username to delete: ").strip()
    delete_user(username, "super_admin")

def reset_password_menu():
    """Reset password interface"""
    username = input("Enter username to reset password: ").strip()
    new_password = input("Enter new temporary password: ").strip()
    
    if not username or not new_password:
        print("❌ Username and password are required.")
        return
    
    # Hash the new password
    from authentication import hash_password
    hashed_password = hash_password(new_password)
    
    # Update password
    if update_user_password(username, hashed_password, "super_admin"):
        print("✅ Password reset successfully!")
    else:
        print("❌ Failed to reset password.")

def view_logs(username):
    """View system logs"""
    print("\n=== SYSTEM LOGS ===")
    print("1. View All Logs")
    print("2. View Suspicious Activities")
    print("3. Back")
    
    choice = input("Enter your choice (1-3): ").strip()
    
    if choice == "1":
        logs = get_logs()
        if isinstance(logs, list):
            for log in logs[-20:]:  # Show last 20 entries
                print(log)
        else:
            print(logs)
    elif choice == "2":
        suspicious_logs = get_suspicious_logs()
        if isinstance(suspicious_logs, list):
            for log in suspicious_logs:
                print(log)
        else:
            print(suspicious_logs)

def generate_restore_code_menu(username):
    """Generate restore code interface"""
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
    """Revoke restore code interface"""
    code = input("Enter restore code to revoke: ").strip()
    if not code:
        print("Restore code cannot be empty")
        return
    revoke_restore_code(code)

def restore_backup_menu(username):
    """Restore backup interface"""
    code = input("Enter restore code: ").strip()
    if not code:
        print("Restore code cannot be empty")
        return
    restore_backup(code, username)

if __name__ == "__main__":
    main()
