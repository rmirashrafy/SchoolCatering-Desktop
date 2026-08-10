import sqlite3
from database import get_connection

# --- مدیریت مدارس ---
def get_all_schools():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM schools ORDER BY id ASC")
    schools = [row[0] for row in cursor.fetchall()]
    conn.close()
    return schools

def add_school(name):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO schools (name) VALUES (?)", (name,))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

# --- مدیریت رسیدهای ثابت (Fixed Receipts) ---
def save_fixed_receipt(receipt_type, amount, date, worker_name=None, image_path=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO fixed_receipts (receipt_type, worker_name, amount, receipt_date, image_path)
        VALUES (?, ?, ?, ?, ?)
    """, (receipt_type, worker_name, amount, date, image_path))
    conn.commit()
    conn.close()

def get_all_fixed_receipts():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, receipt_type, worker_name, amount, receipt_date, image_path FROM fixed_receipts ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

# --- مدیریت فاکتور فروش / برگشتی مدارس ---
def get_sales_invoice_items(school_name, invoice_type):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT sii.category, sii.food_name, sii.quantity, sii.unit_price, sii.total_price
        FROM sales_invoice_items sii
        JOIN sales_invoices si ON sii.sales_invoice_id = si.id
        WHERE si.school_name = ? AND si.invoice_type = ?
    """, (school_name, invoice_type))
    rows = cursor.fetchall()
    conn.close()

    items = []
    for row in rows:
        items.append({
            "category": row[0],
            "food": row[1],
            "qty": row[2],
            "price": row[3],
            "total": row[4]
        })
    return items

def save_sales_invoice(school_name, invoice_type, items_list):
    conn = get_connection()
    cursor = conn.cursor()
    
    # پاک کردن آخرین فاکتور ثبت‌شده این مدرسه برای این نوع و جایگزینی با اطلاعات جدید
    cursor.execute("""
        DELETE FROM sales_invoices WHERE school_name = ? AND invoice_type = ?
    """, (school_name, invoice_type))

    cursor.execute("""
        INSERT INTO sales_invoices (school_name, invoice_type) VALUES (?, ?)
    """, (school_name, invoice_type))
    invoice_id = cursor.lastrowid

    for item in items_list:
        cursor.execute("""
            INSERT INTO sales_invoice_items (sales_invoice_id, category, food_name, quantity, unit_price, total_price)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (invoice_id, item.get("category", ""), item.get("food", ""), item.get("qty", 1), item.get("price", 0), item.get("total", 0)))

    conn.commit()
    conn.close()

# --- مدیریت مخارج مدارس (School Expenses) ---
def save_school_expense(school_name, title, amount, date, notes="", image_path=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO school_expenses (school_name, title, amount, expense_date, notes, image_path)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (school_name, title, amount, date, notes, image_path))
    conn.commit()
    conn.close()

def get_school_expenses(school_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, title, amount, expense_date, notes, image_path
        FROM school_expenses WHERE school_name = ? ORDER BY id DESC
    """, (school_name,))
    rows = cursor.fetchall()
    conn.close()
    return rows
