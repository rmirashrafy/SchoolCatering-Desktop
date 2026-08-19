import sqlite3
from LocalDataBase.database import get_connection

def create_school(school_name, address=None, phone=None):
    """
    Registers a new contracted school.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO schools (school_name, address, phone)
            VALUES (?, ?, ?)
        ''', (school_name, address, phone))
        
        conn.commit()
        school_id = cursor.lastrowid
        print(f"School '{school_name}' added successfully with ID: {school_id}")
        return school_id

    except Exception as e:
        print(f"Error creating school: {e}")
        return None
        
    finally:
        conn.close()


def get_all_schools(active_only=True):
    """
    Retrieves all schools.
    If active_only is True, returns only active contracts.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    if active_only:
        cursor.execute('''
            SELECT school_id, school_name, address, phone, is_active 
            FROM schools 
            WHERE is_active = 1
        ''')
    else:
        cursor.execute('''
            SELECT school_id, school_name, address, phone, is_active 
            FROM schools
        ''')
        
    schools = cursor.fetchall()
    conn.close()
    
    # Format list of dictionaries for clean usage
    result = []
    for s in schools:
        result.append({
            "school_id": s[0],
            "school_name": s[1],
            "address": s[2],
            "phone": s[3],
            "is_active": s[4]
        })
    return result


def update_school(school_id, school_name=None, address=None, phone=None):
    """
    Updates school details dynamically based on provided fields.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # Build query dynamically
    fields = []
    values = []
    
    if school_name is not None:
        fields.append("school_name = ?")
        values.append(school_name)
    if address is not None:
        fields.append("address = ?")
        values.append(address)
    if phone is not None:
        fields.append("phone = ?")
        values.append(phone)
        
    if not fields:
        print("No fields provided to update.")
        conn.close()
        return False
        
    values.append(school_id)
    query = f"UPDATE schools SET {', '.join(fields)} WHERE school_id = ?"
    
    cursor.execute(query, tuple(values))
    conn.commit()
    updated = cursor.rowcount > 0
    conn.close()
    
    if updated:
        print(f"School ID {school_id} updated successfully.")
    else:
        print(f"School ID {school_id} not found.")
    return updated


def toggle_school_active_status(school_id, is_active):
    """
    Soft-deletes or reactivates a school contract (1 = Active, 0 = Inactive).
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE schools SET is_active = ? WHERE school_id = ?
    ''', (1 if is_active else 0, school_id))
    
    conn.commit()
    success = cursor.rowcount > 0
    conn.close()
    
    status_str = "activated" if is_active else "deactivated"
    if success:
        print(f"School ID {school_id} has been {status_str}.")
    return success


# ==========================================
# Testing Module
# ==========================================
# if __name__ == "__main__":
#     print("--- Testing School Management ---")
    
#     # 1. Add Schools
#     s1_id = create_school("Al-Noor Private School", "Muscat Main St", "96891234567")
#     s2_id = create_school("Al-Amal High School", "Seeb District", "96897654321")
    
#     # 2. Get Active Schools
#     print("\n--- Active Schools List ---")
#     print(get_all_schools(active_only=True))
    
#     # 3. Update School Info
#     print("\n--- Update School Info ---")
#     update_school(s1_id, phone="96890000000")
    
#     # 4. Soft Delete (Deactivate)
#     print("\n--- Deactivate School ---")
#     toggle_school_active_status(s2_id, is_active=False)
