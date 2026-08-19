import sqlite3
from LocalDataBase.database import get_connection

VALID_ITEM_TYPES = ('Raw_Material', 'Prepared_Food', 'Prepackaged')

def create_item(item_name, item_type, unit_of_measure, initial_stock=0.0, cost_price=0.0, selling_price=0.0):
    """
    Creates a new inventory item.
    item_type must be one of: 'Raw_Material', 'Prepared_Food', 'Prepackaged'
    """
    if item_type not in VALID_ITEM_TYPES:
        print(f"Error: Invalid item_type '{item_type}'. Must be one of {VALID_ITEM_TYPES}")
        return None

    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO items (item_name, item_type, unit_of_measure, current_stock, cost_price, selling_price)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (item_name, item_type, unit_of_measure, initial_stock, cost_price, selling_price))
        
        conn.commit()
        item_id = cursor.lastrowid
        print(f"Item '{item_name}' ({item_type}) added successfully with ID: {item_id}")
        return item_id

    except Exception as e:
        print(f"Error creating item: {e}")
        return None
    finally:
        conn.close()


def get_all_items(item_type=None):
    """
    Retrieves all items, or filters by item_type if specified.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    if item_type:
        if item_type not in VALID_ITEM_TYPES:
            print(f"Error: Invalid item_type filter '{item_type}'.")
            conn.close()
            return []
        cursor.execute('''
            SELECT item_id, item_name, item_type, unit_of_measure, current_stock, cost_price, selling_price
            FROM items WHERE item_type = ?
        ''', (item_type,))
    else:
        cursor.execute('''
            SELECT item_id, item_name, item_type, unit_of_measure, current_stock, cost_price, selling_price
            FROM items
        ''')
        
    items = cursor.fetchall()
    conn.close()
    
    result = []
    for item in items:
        result.append({
            "item_id": item[0],
            "item_name": item[1],
            "item_type": item[2],
            "unit_of_measure": item[3],
            "current_stock": item[4],
            "cost_price": item[5],
            "selling_price": item[6]
        })
    return result


def update_item_prices(item_id, cost_price=None, selling_price=None):
    """
    Updates cost price and/or selling price for an item.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    fields = []
    values = []
    
    if cost_price is not None:
        fields.append("cost_price = ?")
        values.append(cost_price)
    if selling_price is not None:
        fields.append("selling_price = ?")
        values.append(selling_price)
        
    if not fields:
        print("No price fields provided for update.")
        conn.close()
        return False
        
    values.append(item_id)
    query = f"UPDATE items SET {', '.join(fields)} WHERE item_id = ?"
    
    cursor.execute(query, tuple(values))
    conn.commit()
    updated = cursor.rowcount > 0
    conn.close()
    
    if updated:
        print(f"Prices for Item ID {item_id} updated successfully.")
    else:
        print(f"Item ID {item_id} not found.")
    return updated


def adjust_stock(item_id, quantity_change):
    """
    Adjusts stock level. 
    Use positive quantity_change for restock/purchases (+50).
    Use negative quantity_change for sales/deliveries (-10).
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # Verify item exists and check current stock
    cursor.execute('SELECT current_stock FROM items WHERE item_id = ?', (item_id,))
    row = cursor.fetchone()
    
    if not row:
        print(f"Error: Item ID {item_id} does not exist.")
        conn.close()
        return False
        
    current_stock = row[0]
    new_stock = current_stock + quantity_change
    
    if new_stock < 0:
        print(f"Warning: Stock adjustment results in negative stock ({new_stock}). Transaction halted.")
        conn.close()
        return False

    cursor.execute('''
        UPDATE items SET current_stock = ? WHERE item_id = ?
    ''', (new_stock, item_id))
    
    conn.commit()
    conn.close()
    print(f"Stock for Item ID {item_id} adjusted by {quantity_change:+.2f}. New Stock: {new_stock:.2f}")
    return True


# ==========================================
# Testing Module
# ==========================================
# if __name__ == "__main__":
#     print("--- Testing Items Management ---")
    
#     # 1. Create Items across different types
#     i1_id = create_item("Fresh Milk 1L", "Prepackaged", "Bottle", initial_stock=100.0, cost_price=0.40, selling_price=0.60)
#     i2_id = create_item("Chicken Sandwich", "Prepared_Food", "Piece", initial_stock=0.0, cost_price=0.30, selling_price=0.50)
#     i3_id = create_item("Wheat Flour", "Raw_Material", "Kg", initial_stock=50.0, cost_price=0.20, selling_price=0.0)
    
#     # 2. Get All Prepared Food Items
#     print("\n--- Prepared Foods List ---")
#     print(get_all_items(item_type="Prepared_Food"))
    
#     # 3. Update Prices
#     print("\n--- Update Prices ---")
#     update_item_prices(i2_id, cost_price=0.35, selling_price=0.55)
    
#     # 4. Stock Adjustment Tests
#     print("\n--- Stock Adjustments ---")
#     adjust_stock(i2_id, 30.0)   # Cooked 30 sandwiches -> +30 stock
#     adjust_stock(i2_id, -5.0)   # Delivered 5 sandwiches -> -5 stock
