import sqlite3
from LocalDataBase.database import get_connection

def record_expense(category_id, amount, created_by_user_id, description=None, school_id=None, worker_id=None):
    """
    Records a new operational expense.
    Requires category_id, amount (> 0), and created_by_user_id.
    Optionally links to a school_id or worker_id.
    """
    if amount <= 0:
        print("Error: Expense amount must be greater than zero.")
        return None

    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO expenses (category_id, amount, description, school_id, worker_id, created_by_user_id)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (category_id, amount, description, school_id, worker_id, created_by_user_id))
        
        conn.commit()
        expense_id = cursor.lastrowid
        print(f"Expense recorded successfully with ID: {expense_id} (Amount: {amount})")
        return expense_id

    except sqlite3.IntegrityError as e:
        print(f"Foreign Key Error: Ensure category_id, user_id, school_id, and worker_id exist. {e}")
        return None
    except Exception as e:
        print(f"Error recording expense: {e}")
        return None
    finally:
        conn.close()


def get_expenses(start_date=None, end_date=None, category_id=None, school_id=None):
    """
    Retrieves filtered expenses with full details (category name, school name, creator name).
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    query = '''
        SELECT 
            e.expense_id,
            e.expense_date,
            c.category_name,
            e.amount,
            e.description,
            s.school_name,
            w.full_name AS worker_name,
            u.full_name AS created_by
        FROM expenses e
        JOIN expense_categories c ON e.category_id = c.category_id
        JOIN users u ON e.created_by_user_id = u.user_id
        LEFT JOIN schools s ON e.school_id = s.school_id
        LEFT JOIN users w ON e.worker_id = w.user_id
        WHERE 1=1
    '''
    params = []

    if start_date:
        query += ' AND e.expense_date >= ?'
        params.append(f"{start_date} 00:00:00")
    if end_date:
        query += ' AND e.expense_date <= ?'
        params.append(f"{end_date} 23:59:59")
    if category_id:
        query += ' AND e.category_id = ?'
        params.append(category_id)
    if school_id:
        query += ' AND e.school_id = ?'
        params.append(school_id)

    query += ' ORDER BY e.expense_date DESC'

    cursor.execute(query, tuple(params))
    rows = cursor.fetchall()
    conn.close()

    result = []
    for r in rows:
        result.append({
            "expense_id": r[0],
            "expense_date": r[1],
            "category_name": r[2],
            "amount": r[3],
            "description": r[4],
            "school_name": r[5],
            "worker_name": r[6],
            "created_by": r[7]
        })
    return result


def get_total_expenses_by_category(start_date=None, end_date=None):
    """
    Calculates total expenditure grouped by category for financial summary reports.
    """
    conn = get_connection()
    cursor = conn.cursor()

    query = '''
        SELECT 
            c.category_name,
            SUM(e.amount) AS total_amount,
            COUNT(e.expense_id) AS transaction_count
        FROM expenses e
        JOIN expense_categories c ON e.category_id = c.category_id
        WHERE 1=1
    '''
    params = []

    if start_date:
        query += ' AND e.expense_date >= ?'
        params.append(f"{start_date} 00:00:00")
    if end_date:
        query += ' AND e.expense_date <= ?'
        params.append(f"{end_date} 23:59:59")

    query += ' GROUP BY c.category_id ORDER BY total_amount DESC'

    cursor.execute(query, tuple(params))
    rows = cursor.fetchall()
    conn.close()

    return [{"category_name": r[0], "total_amount": r[1], "transaction_count": r[2]} for r in rows]



# ==========================================
# Testing Module
# ==========================================
# if __name__ == "__main__":
#     print("--- Testing Expenses Operations ---")

#     # Assuming category_id=1 exists, created_by_user_id=1 exists
#     # 1. Record general expense
#     exp1 = record_expense(
#         category_id=1, 
#         amount=45.50, 
#         created_by_user_id=1, 
#         description="Electricity Bill - August"
#     )

#     # 2. Record worker advance
#     exp2 = record_expense(
#         category_id=2, 
#         amount=20.00, 
#         created_by_user_id=1, 
#         description="Cash advance for transport", 
#         worker_id=2
#     )

#     # 3. Retrieve Expense Report
#     print("\n--- Detailed Expenses List ---")
#     print(get_expenses())

#     # 4. Summary by Category
#     print("\n--- Expense Summary by Category ---")
    print(get_total_expenses_by_category())
