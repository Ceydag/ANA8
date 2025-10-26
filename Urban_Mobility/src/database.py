import sqlite3
import os
from encryption import encrypt_data, decrypt_data

def initialize_db(): 
    db_path = 'urban_mobility.db'

    db_already_exists = os.path.exists(db_path)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        first_name TEXT,
        last_name TEXT,
        role TEXT NOT NULL,
        registration_date TEXT,
        temp_password BOOLEAN DEFAULT 0
    )
    ''')
    
 
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Travellers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        birthday TEXT NOT NULL,
        gender TEXT NOT NULL,
        street_name TEXT NOT NULL,
        house_number TEXT NOT NULL,
        zip_code TEXT NOT NULL,
        city TEXT NOT NULL,
        email TEXT NOT NULL,
        mobile_phone TEXT NOT NULL,
        driving_license TEXT NOT NULL,
        registration_date TEXT NOT NULL
    )
    ''')
    
 
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Scooters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        brand TEXT NOT NULL,
        model TEXT NOT NULL,
        serial_number TEXT UNIQUE NOT NULL,
        top_speed INTEGER,
        battery_capacity INTEGER,
        state_of_charge INTEGER,
        target_range_min INTEGER,
        target_range_max INTEGER,
        latitude REAL,
        longitude REAL,
        out_of_service BOOLEAN DEFAULT 0,
        mileage REAL DEFAULT 0,
        last_maintenance_date TEXT,
        in_service_date TEXT NOT NULL
    )
    ''')
    

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS RestoreCodes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT UNIQUE NOT NULL,
        system_admin_username TEXT NOT NULL,
        backup_filename TEXT NOT NULL,
        created_date TEXT NOT NULL,
        used BOOLEAN DEFAULT 0
    )
    ''')

    cursor.execute("SELECT COUNT(*) FROM Users WHERE username = 'super_admin'")
    admin_already_exists = cursor.fetchone()[0] > 0

    import bcrypt
    salt = bcrypt.gensalt()
    super_admin_password = bcrypt.hashpw('Admin_123?'.encode('utf-8'), salt)
    cursor.execute('''
    INSERT OR IGNORE INTO Users (username, password_hash, role, first_name, last_name, registration_date)
    VALUES (?, ?, ?, ?, ?, datetime('now'))
    ''', ('super_admin', super_admin_password, 'Super Admin', 'Super', 'Administrator'))

    
    conn.commit()
    conn.close()

    if not db_already_exists or not admin_already_exists:
        print("Database initialized successfully!")
        print("Super Admin account created")

def get_connection():
    try:
        import os
        if os.path.exists('src/urban_mobility.db'):
            db_path = 'src/urban_mobility.db'
        elif os.path.exists('urban_mobility.db'):
            db_path = 'urban_mobility.db'
        else:
            db_path = 'src/urban_mobility.db' 
        
        conn = sqlite3.connect(db_path, timeout=30.0)
        conn.execute('PRAGMA busy_timeout=30000')
        return conn
    except sqlite3.OperationalError as e:
        print(f"Database connection error: {e}")
        return None

def close_connection(conn):
    if conn:
        try:
            conn.close()
        except sqlite3.Error as e:
            print(f"Error closing database connection: {e}")

def unlock_database():
    try:
        conn = sqlite3.connect('urban_mobility.db', timeout=5.0)
        conn.close()
        return True
    except sqlite3.OperationalError:
        return False
