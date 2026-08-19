import sqlite3
from LocalDataBase.database import get_connection

def set_canteen_menu_item(school_id, item_id, default_quantity):
    """
    Adds or updates an item's default quantity for a specific school's canteen menu.
    If default_quantity is 0 or less, the item is removed from the template.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        if default_quantity <= 0:
            # Remove item from school template if quantity set to 0
            cursor.execute('''
                DELETE FROM school_canteen_menu 
                WHERE school_id = ? AND item_id = ?
            ''', (school_id, item_id))
            conn.commit()
            print(f"Item ID {item_id} removed from School ID {school_id} menu.")
            return True

        # UPSERT: Insert new record or update default_quantity if (school_id, item_id) exists
        cursor.execute('''
            INSERT INTO school_canteen_menu (school_id, item_id, default_quantity)
            VALUES (?, ?, ?)
            ON CONFLICT(school_id, item_id) DO UPDATE SET
                default_quantity = excluded.default_quantity
        ''', (school_id, item_id, default_quantity))
        
        conn.commit()
        print(f"Menu item updated: School ID {school_id} -> Item ID {item_id} (Default: {default_quantity})")
        return True

    except sqlite3.IntegrityError as e:
        print(f"Foreign Key Error: Check if school_id ({school_id}) or item_id ({item_id}) exists. {e}")
        return False
    except Exception as e:
        print(f"Error setting menu item: {e}")
        return False
    finally:
        conn.close()


def bulk_set_canteen_menu(school_id, menu_items):
    """
    Configures multiple menu items at once for a school.
    menu_items should be a list of tuples or dicts: [(item_id, default_quantity), ...]
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        for item in menu_items:
            if isinstance(item, dict):
                item_id, qty = item["item_id"], item["default_quantity"]
            else:
                item_id, qty = item[0], item[1]
                
            cursor.execute('''
                INSERT INTO school_canteen_menu (school_id, item_id, default_quantity)
                VALUES (?, ?, ?)
                ON CONFLICT(school_id, item_id) DO UPDATE SET
                    default_quantity = excluded.default_quantity
            ''', (school_id, item_id, qty))
            
        conn.commit()
        print(f"Successfully configured {len(menu_items)} menu items for School ID {school_id}.")
        return True
    except Exception as e:
        print(f"Error during bulk menu update: {e}")
        return False
    finally:
        conn.close()


def get_school_menu(school_id):
    """
    Retrieves the complete menu preset for a school, joined with Item details.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT 
            m.menu_id,
            m.school_id,
            m.item_id,
            i.item_name,
            i.item_type,
            i.unit_of_measure,
            i.selling_price,
            m.default_quantity
        FROM school_canteen_menu m
        JOIN items i ON m.item_id = i.item_id
        WHERE m.school_id = ?
    ''', (school_id,))
    
    records = cursor.fetchall()
    conn.close()
    
    menu = []
    for r in records:
        menu.append({
            "menu_id": r[0],
            "school_id": r[1],
            "item_id": r[2],
            "item_name": r[3],
            "item_type": r[4],
            "unit_of_measure": r[5],
            "selling_price": r[6],
            "default_quantity": r[7]
        })
    return menu


def remove_menu_item(school_id, item_id):
    """
    Explicitly removes an item from a school's canteen menu template.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        DELETE FROM school_canteen_menu 
        WHERE school_id = ? AND item_id = ?
    ''', (school_id, item_id))
    
    conn.commit()
    removed = cursor.rowcount > 0
    conn.close()
    
    if removed:
        print(f"Item ID {item_id} removed from School ID {school_id} menu.")
    else:
        print("Menu record not found.")
    return removed


# ==========================================
# Testing Module
# ==========================================
# if __name__ == "__main__":
#     print("--- Testing School Canteen Menu Operations ---")
    
#     # 1. Single Item Preset Setting
#     set_canteen_menu_item(school_id=1, item_id=1, default_quantity=50.0) # 50 Bottles of Milk
#     set_canteen_menu_item(school_id=1, item_id=2, default_quantity=30.0) # 30 Sandwiches
    
#     # 2. Bulk Menu Setup for School #2
#     bulk_set_canteen_menu(school_id=2, menu_items=[
#         {"item_id": 1, "default_quantity": 100.0},
#         {"item_id": 2, "default_quantity": 60.0}
#     ])
    
#     # 3. Retrieve Preset Menu for School #1
#     print("\n--- Menu Preset for School #1 ---")
#     school_1_menu = get_school_menu(school_id=1)
#     for entry in school_1_menu:
#         print(entry)
        
#     # 4. Update default quantity using UPSERT
#     print("\n--- Updating Item Preset ---")
#     set_canteen_menu_item(school_id=1, item_id=1, default_quantity=75.0) # Change Milk default from 50 to 75
