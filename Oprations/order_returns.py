import sqlite3
from LocalDataBase.database import get_connection
from items import adjust_stock

def create_return_header(order_id, processed_by_user_id):
    """
    Creates a new return process header for a given delivered order.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO order_returns (order_id, processed_by_user_id)
            VALUES (?, ?)
        ''', (order_id, processed_by_user_id))
        
        conn.commit()
        return_id = cursor.lastrowid
        print(f"Return record #{return_id} initialized for Order #{order_id}.")
        return return_id

    except sqlite3.IntegrityError as e:
        print(f"Foreign Key Error: Check if order_id ({order_id}) or user_id exist. {e}")
        return None
    except Exception as e:
        print(f"Error creating return header: {e}")
        return None
    finally:
        conn.close()


def add_return_item(return_id, item_id, returned_quantity, disposition, unit_credit_price=None):
    """
    Adds a returned item line to an order_returns record.
    disposition: 'Restock' (adds back to inventory) or 'Waste' (scrapped, no stock increase).
    unit_credit_price: If None, fetches the selling_price from items table to refund the school.
    """
    if disposition not in ('Restock', 'Waste'):
        print(f"Error: Invalid disposition '{disposition}'. Must be 'Restock' or 'Waste'.")
        return None

    if returned_quantity <= 0:
        print("Error: Returned quantity must be greater than zero.")
        return None

    conn = get_connection()
    cursor = conn.cursor()

    try:
        # 1. Fetch item unit price if not specified
        if unit_credit_price is None:
            cursor.execute('SELECT selling_price FROM items WHERE item_id = ?', (item_id,))
            row = cursor.fetchone()
            if not row:
                print(f"Error: Item ID {item_id} not found.")
                return None
            unit_credit_price = row[0]

        credit_amount = round(returned_quantity * unit_credit_price, 2)

        # 2. Insert item record into order_return_items
        cursor.execute('''
            INSERT INTO order_return_items (return_id, item_id, returned_quantity, disposition, credit_amount)
            VALUES (?, ?, ?, ?, ?)
        ''', (return_id, item_id, returned_quantity, disposition, credit_amount))

        return_item_id = cursor.lastrowid

        # 3. Handle inventory impact if disposition is 'Restock'
        if disposition == 'Restock':
            adjust_stock(item_id, returned_quantity)

        conn.commit()

        # 4. Update total return credit in the return header
        recalculate_return_total(return_id)
        
        print(f"Return item added: Item ID {item_id} (Qty: {returned_quantity}, Mode: {disposition}, Credit: {credit_amount})")
        return return_item_id

    except Exception as e:
        print(f"Error adding return item: {e}")
        return None
    finally:
        conn.close()


def recalculate_return_total(return_id):
    """
    Recalculates and updates total_return_credit in order_returns table.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT COALESCE(SUM(credit_amount), 0.0)
        FROM order_return_items
        WHERE return_id = ?
    ''', (return_id,))

    total_credit = cursor.fetchone()[0]

    cursor.execute('''
        UPDATE order_returns
        SET total_return_credit = ?
        WHERE return_id = ?
    ''', (total_credit, return_id))

    conn.commit()
    conn.close()
    return total_credit


def get_return_details(return_id):
    """
    Retrieves full return report including items, disposition status, and total refund credit.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT 
            r.return_id,
            r.order_id,
            r.return_date,
            r.total_return_credit,
            u.full_name AS processed_by
        FROM order_returns r
        JOIN users u ON r.processed_by_user_id = u.user_id
        WHERE r.return_id = ?
    ''', (return_id,))

    header = cursor.fetchone()
    if not header:
        conn.close()
        return None

    cursor.execute('''
        SELECT 
            ri.return_item_id,
            ri.item_id,
            i.item_name,
            i.unit_of_measure,
            ri.returned_quantity,
            ri.disposition,
            ri.credit_amount
        FROM order_return_items ri
        JOIN items i ON ri.item_id = i.item_id
        WHERE ri.return_id = ?
    ''', (return_id,))

    items = cursor.fetchall()
    conn.close()

    return {
        "return_id": header[0],
        "order_id": header[1],
        "return_date": header[2],
        "total_return_credit": header[3],
        "processed_by": header[4],
        "items": [{
            "return_item_id": r[0],
            "item_id": r[1],
            "item_name": r[2],
            "unit_of_measure": r[3],
            "returned_quantity": r[4],
            "disposition": r[5],
            "credit_amount": r[6]
        } for r in items]
    }


# ==========================================
# Testing Module
# ==========================================
# if __name__ == "__main__":
#     print("--- Testing Order Returns Operations ---")

#     # Assuming order_id=1 exists and processed_by_user_id=1 exists
#     # 1. Create return record header
#     ret_id = create_return_header(order_id=1, processed_by_user_id=1)

#     # 2. Add prepackaged item (Restock -> returned back to inventory)
#     add_return_item(return_id=ret_id, item_id=1, returned_quantity=5.0, disposition='Restock')

#     # 3. Add prepared food item (Waste -> expired/spoiled, no inventory update)
#     add_return_item(return_id=ret_id, item_id=2, returned_quantity=2.0, disposition='Waste')

#     # 4. Fetch full return report
#     print("\n--- Return Report Details ---")
#     print(get_return_details(ret_id))
