import sqlite3
from LocalDataBase.database import get_connection

def create_school_staff(school_id, full_name, phone=None, role_title="Canteen Representative"):
    """
    Registers a new staff member or contact person for a specific school.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO school_staff (school_id, full_name, phone, role_title)
            VALUES (?, ?, ?, ?)
        ''', (school_id, full_name, phone, role_title))
        
        conn.commit()
        staff_id = cursor.lastrowid
        print(f"Staff member '{full_name}' added successfully with ID: {staff_id}")
        return staff_id

    except sqlite3.IntegrityError as e:
        # Fails if provided school_id does not exist in the schools table
        print(f"Foreign Key Error: Invalid school_id ({school_id}). {e}")
        return None
    except Exception as e:
        print(f"Error creating school staff: {e}")
        return None
    finally:
        conn.close()


def get_staff_by_school(school_id, active_only=True):
    """
    Retrieves all staff members assigned to a specific school.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    query = '''
        SELECT staff_id, school_id, full_name, phone, role_title, is_active 
        FROM school_staff 
        WHERE school_id = ?
    '''
    if active_only:
        query += ' AND is_active = 1'
        
    cursor.execute(query, (school_id,))
    staff_records = cursor.fetchall()
    conn.close()
    
    result = []
    for row in staff_records:
        result.append({
            "staff_id": row[0],
            "school_id": row[1],
            "full_name": row[2],
            "phone": row[3],
            "role_title": row[4],
            "is_active": row[5]
        })
    return result


def update_school_staff(staff_id, full_name=None, phone=None, role_title=None):
    """
    Updates staff member details dynamically.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    fields = []
    values = []
    
    if full_name is not None:
        fields.append("full_name = ?")
        values.append(full_name)
    if phone is not None:
        fields.append("phone = ?")
        values.append(phone)
    if role_title is not None:
        fields.append("role_title = ?")
        values.append(role_title)
        
    if not fields:
        print("No fields provided for update.")
        conn.close()
        return False
        
    values.append(staff_id)
    query = f"UPDATE school_staff SET {', '.join(fields)} WHERE staff_id = ?"
    
    cursor.execute(query, tuple(values))
    conn.commit()
    updated = cursor.rowcount > 0
    conn.close()
    
    if updated:
        print(f"Staff ID {staff_id} updated successfully.")
    else:
        print(f"Staff ID {staff_id} not found.")
    return updated


def toggle_staff_active_status(staff_id, is_active):
    """
    Soft-deletes or reactivates a school staff member.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE school_staff SET is_active = ? WHERE staff_id = ?
    ''', (1 if is_active else 0, staff_id))
    
    conn.commit()
    success = cursor.rowcount > 0
    conn.close()
    
    status_str = "activated" if is_active else "deactivated"
    if success:
        print(f"Staff ID {staff_id} has been {status_str}.")
    return success


# ==========================================
# Testing Module
# ==========================================
# if __name__ == "__main__":
#     print("--- Testing School Staff Management ---")
    
#     # 1. Add staff for school_id = 1
#     staff1_id = create_school_staff(
#         school_id=1, 
#         full_name="Khamis Al-Busaidi", 
#         phone="96898887766", 
#         role_title="Canteen Supervisor"
#     )
    
#     staff2_id = create_school_staff(
#         school_id=1, 
#         full_name="Salem Al-Harthy", 
#         phone="96895554433", 
#         role_title="Delivery Receiver"
#     )
    
#     # 2. Retrieve active staff for School #1
#     print("\n--- Staff List for School #1 ---")
#     print(get_staff_by_school(school_id=1, active_only=True))
    
#     # 3. Update staff phone number
#     print("\n--- Update Staff Details ---")
#     update_school_staff(staff1_id, phone="96899000000")
    
#     # 4. Soft-delete staff member
#     print("\n--- Soft Delete Staff ---")
#     toggle_staff_active_status(staff2_id, is_active=False)
