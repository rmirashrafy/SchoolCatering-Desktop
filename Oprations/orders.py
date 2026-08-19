import sqlite3
from LocalDataBase.database import get_connection

def create_order(school_id, created_by_user_id, order_type='Delivery', school_staff_id=None, notes=None):
    """
    Creates a new order header in 'Draft' status.
    order_type must be either 'Delivery' or 'Return'.
    """
    if order_type not in ('Delivery', 'Return'):
        print(f"Error: Invalid order_type '{order_type}'. Must be 'Delivery' or 'Return'.")
        return None

    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO orders (school_id, school_staff_id, created_by_user_id, order_type, status, notes)
            VALUES (?, ?, ?, ?, 'Draft', ?)
        ''', (school_id, school_staff_id, created_by_user_id, order_type, notes))
        
        conn.commit()
        order_id = cursor.lastrowid
        print(f"Order #{order_id} ({order_type}) created in 'Draft' status for School ID {school_id}.")
        return order_id

    except sqlite3.IntegrityError as e:
        print(f"Foreign Key Error: Check if school_id, staff_id, or user_id exist. {e}")
        return None
    except Exception as e:
        print(f"Error creating order: {e}")
        return None
    finally:
        conn.close()


def update_order_status(order_id, new_status):
    """
    Updates the status of an order ('Draft', 'Finalized', 'Canceled').
    """
    valid_statuses = ('Draft', 'Finalized', 'Canceled')
    if new_status not in valid_statuses:
        print(f"Error: Invalid status '{new_status}'. Must be one of {valid_statuses}")
        return False

    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE orders 
        SET status = ? 
        WHERE order_id = ?
    ''', (new_status, order_id))
    
    conn.commit()
    updated = cursor.rowcount > 0
    conn.close()
    
    if updated:
        print(f"Order #{order_id} status changed to '{new_status}'.")
    else:
        print(f"Order #{order_id} not found.")
    return updated


def recalculate_order_total(order_id):
    """
    Recalculates total_amount from order_items table and updates the order header.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT COALESCE(SUM(subtotal), 0.0) 
        FROM order_items 
        WHERE order_id = ?
    ''', (order_id,))
    
    new_total = cursor.fetchone()[0]
    
    cursor.execute('''
        UPDATE orders 
        SET total_amount = ? 
        WHERE order_id = ?
    ''', (new_total, order_id))
    
    conn.commit()
    conn.close()
    return new_total


def get_orders(school_id=None, status=None, order_type=None, start_date=None, end_date=None):
    """
    Retrieves orders with school and user details based on filter parameters.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    query = '''
        SELECT 
            o.order_id,
            o.order_date,
            s.school_name,
            st.full_name AS staff_name,
            u.full_name AS created_by,
            o.order_type,
            o.total_amount,
            o.status,
            o.notes
        FROM orders o
        JOIN schools s ON o.school_id = s.school_id
        JOIN users u ON o.created_by_user_id = u.user_id
        LEFT JOIN school_staff st ON o.school_staff_id = st.staff_id
        WHERE 1=1
    '''
    params = []

    if school_id:
        query += ' AND o.school_id = ?'
        params.append(school_id)
    if status:
        query += ' AND o.status = ?'
        params.append(status)
    if order_type:
        query += ' AND o.order_type = ?'
        params.append(order_type)
    if start_date:
        query += ' AND o.order_date >= ?'
        params.append(f"{start_date} 00:00:00")
    if end_date:
        query += ' AND o.order_date <= ?'
        params.append(f"{end_date} 23:59:59")

    query += ' ORDER BY o.order_date DESC'

    cursor.execute(query, tuple(params))
    rows = cursor.fetchall()
    conn.close()

    result = []
    for r in rows:
        result.append({
            "order_id": r[0],
            "order_date": r[1],
            "school_name": r[2],
            "staff_name": r[3],
            "created_by": r[4],
            "order_type": r[5],
            "total_amount": r[6],
            "status": r[7],
            "notes": r[8]
        })
    return result


# ==========================================
# Testing Module
# ==========================================
# if __name__ == "__main__":
#     print("--- Testing Orders Header Operations ---")
    
#     # 1. Create a draft delivery order for School #1 by User #1
#     ord_id = create_order(school_id=1, created_by_user_id=1, order_type='Delivery', notes="Morning delivery")
    
#     # 2. Get active orders
#     print("\n--- Orders List ---")
#     print(get_orders(school_id=1))
    
#     # 3. Change status to Finalized
#     update_order_status(ord_id, 'Finalized')
