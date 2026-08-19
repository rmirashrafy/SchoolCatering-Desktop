import sqlite3
from LocalDataBase.database import get_connection

def create_user(username, password, full_name, role='Staff'):
    """
    Creates a new user in the system.
    Accepted roles: 'Admin' or 'Staff'
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO users (username, password_hash, full_name, role)
            VALUES (?, ?, ?, ?)
        ''', (username, password, full_name, role))
        
        conn.commit()
        user_id = cursor.lastrowid
        print(f"User '{username}' created successfully with ID: {user_id}")
        return user_id

    except sqlite3.IntegrityError:
        # Triggered when the username already exists due to the UNIQUE constraint
        print(f"Error: Username '{username}' is already taken.")
        return None
        
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
        
    finally:
        conn.close()


def login_user(username, password):
    """
    Validates user credentials.
    Returns a dictionary of user details if active and successful.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT user_id, username, full_name, role, is_active
        FROM users
        WHERE username = ? AND password_hash = ?
    ''', (username, password))
    
    user = cursor.fetchone()
    conn.close()
    
    if user:
        user_id, uname, full_name, role, is_active = user
        
        if is_active == 1:
            print(f"Login successful. Welcome, {full_name}!")
            return {
                "user_id": user_id,
                "username": uname,
                "full_name": full_name,
                "role": role
            }
        else:
            print("Access denied: User account is inactive.")
            return None
    else:
        print("Invalid username or password.")
        return None


# ==========================================
# Testing Module
# ==========================================
# if __name__ == "__main__":
#     print("--- Testing User Creation ---")
#     admin_id = create_user("admin", "123456", "System Administrator", "Admin")
#     staff_id = create_user("ali", "1234", "Ali Mohammadi", "Staff")
    
#     print("\n--- Testing Login System ---")
#     current_user = login_user("admin", "123456")
#     failed_login = login_user("admin", "wrong_password")
