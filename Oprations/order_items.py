import sqlite3
from LocalDataBase.database import get_connection
from orders import recalculate_order_total
from items import adjust_stock

def add_item_to_order(order_id, item_id, quantity, unit_price=None):
    """
    Adds an item line to an order.
    If unit_price is not provided, fetches current selling_price from items table.
    Updates current stock in inventory and recalculates order total_amount.
    """
    if quantity <= 0:
        print("Error: Quantity must be greater than zero.")
        return None

    conn = get_connection()
    cursor = conn.cursor()

    try:
        # 1. Fetch item details (price and current stock) if unit_price is not given
        cursor.execute('SELECT selling_price, current_stock FROM items WHERE item_id = ?', (item_id,))
        item_row = cursor.fetchone()
        
        if not item_row:
            print(f"Error: Item ID {item_id} does not exist.")
            return None
            
        default_price, current_stock = item_row[0], item_row[1]
        
        # Use provided unit_price or fall back to default selling_price
        price_to_use = unit_price if unit_price is not None else default_price
        total_price = round(quantity * price_to_use, 2)

        # 2. Check if the order is still in 'Draft' status
        cursor.execute('SELECT status, order_type FROM orders WHERE order_id = ?', (order_id,))
        order_row = cursor.fetchone()
        
        if not order_row:
            print(f"Error: Order ID {order_id} does not exist.")
            return None
            
        order_status, order_type = order_row[0], order_row[1]
        if order_status == 'Canceled':
            print(f"Error: Cannot add items to a Canceled order.")
            return None

        # 3. Check stock availability for Delivery orders
        if order_type == 'Delivery' and current_stock < quantity:
            print(f"Warning: Insufficient stock for Item ID {item_id}. Available: {current_stock}, Requested: {quantity}")
            return None

        # 4. Insert or Update order item (UPSERT if item already exists in same order)
        cursor.execute('''
            INSERT INTO order_items (order_id, item_id, quantity, unit_price, total_price)
            VALUES (?, ?, ?, ?, ?)
        ''', (order_id, item_id, quantity, price_to_use, total_price))
        
        order_item_id = cursor.lastrowid

        # 5. Deduct stock for Delivery or increase stock for Return
        stock_change = -quantity if order_type == 'Delivery' else quantity
        adjust_stock(item_id, stock_change)

        conn.commit()
        print(f"Item ID {item_id} (Qty: {quantity}) added to Order #{order_id}.")

        # 6. Recalculate main order total
        recalculate_order_total(order_id)
        return order_item_id

    except Exception as e:
        print(f"Error adding item to order: {e}")
        return None
    finally:
        conn.close()


def populate_order_from_school_menu(order_id, school_id):
    """
    Auto-populates a Draft order using default items & quantities 
    configured in school_canteen_menu for the specified school.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT m.item_id, m.default_quantity, i.selling_price
        FROM school_canteen_menu m
        JOIN items i ON m.item_id = i.item_id
        WHERE m.school_id = ? AND m.default_quantity > 0
    ''', (school_id,))
    
    menu_items = cursor.fetchall()
    conn.close()

    if not menu_items:
        print(f"No preset menu items found for School ID {school_id}.")
        return False

    added_count = 0
    for item_id, default_qty, price in menu_items:
        res = add_item_to_order(order_id, item_id, default_qty, unit_price=price)
        if res:
            added_count += 1

    print(f"Successfully populated Order #{order_id} with {added_count} menu items.")
    return True


def get_order_items(order_id):
    """
    Retrieves all item lines for a specific order with item details.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT 
            oi.order_item_id,
            oi.order_id,
            oi.item_id,
            i.item_name,
            i.unit_of_measure,
            oi.quantity,
            oi.unit_price,
            oi.total_price
        FROM order_items oi
        JOIN items i ON oi.item_id = i.item_id
        WHERE oi.order_id = ?
    ''', (order_id,))

    rows = cursor.fetchall()
    conn.close()

    return [{
        "order_item_id": r[0],
        "order_id": r[1],
        "item_id": r[2],
        "item_name": r[3],
        "unit_of_measure": r[4],
        "quantity": r[5],
        "unit_price": r[6],
        "total_price": r[7]
    } for r in rows]


def remove_item_from_order(order_item_id):
    """
    Removes an item line from an order, restores inventory stock, and updates order total.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT oi.order_id, oi.item_id, oi.quantity, o.order_type 
        FROM order_items oi
        JOIN orders o ON oi.order_id = o.order_id
        WHERE oi.order_item_id = ?
    ''', (order_item_id,))
    
    row = cursor.fetchone()
    if not row:
        print(f"Order item ID {order_item_id} not found.")
        conn.close()
        return False

    order_id, item_id, quantity, order_type = row[0], row[1], row[2], row[3]

    # Revert inventory stock impact
    stock_revert = quantity if order_type == 'Delivery' else -quantity
    adjust_stock(item_id, stock_revert)

    # Delete order item row
    cursor.execute('DELETE FROM order_items WHERE order_item_id = ?', (order_item_id,))
    conn.commit()
    conn.close()

    # Recalculate main order total
    recalculate_order_total(order_id)
    print(f"Order Item ID {order_item_id} removed from Order #{order_id}. Stock reverted.")
    return True


# ==========================================
# Testing Module
# ==========================================
# if __name__ == "__main__":
#     print("--- Testing Order Items Operations ---")

#     # Assuming order_id=1 and item_id=1 exist
#     # 1. Add single item manually
#     add_item_to_order(order_id=1, item_id=1, quantity=20.0)

#     # 2. Populate entire order automatically from school preset menu
#     populate_order_from_school_menu(order_id=1, school_id=1)

#     # 3. Get all items in order
#     print("\n--- Order Items List ---")
#     items = get_order_items(order_id=1)
#     for i in items:
#         print(i)
