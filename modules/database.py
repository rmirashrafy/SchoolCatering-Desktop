import sqlite3

DB_NAME = "school_system.db"

def get_connection():
    """ایجاد اتصال به دیتابیس لوکال SQLite"""
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    """ساخت تمام جداول مورد نیاز برنامه"""
    conn = get_connection()
    cursor = conn.cursor()

    # ۱. جدول مدارس
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS schools (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    )
    """)

    # ۲. جدول فاکتورهای اصلی خرید/هزینه‌های عمومی
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS invoices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        document_no TEXT,
        document_date TEXT,
        seller_name TEXT,
        buyer_name TEXT,
        payment_method TEXT,
        total_tax REAL DEFAULT 0,
        total_discount REAL DEFAULT 0,
        grand_total REAL DEFAULT 0,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # ۳. اقلام ریز فاکتور خرید
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS invoice_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        invoice_id INTEGER NOT NULL,
        item_name TEXT NOT NULL,
        quantity REAL DEFAULT 1,
        unit_price REAL DEFAULT 0,
        discount_percent REAL DEFAULT 0,
        tax_percent REAL DEFAULT 0,
        total_price REAL DEFAULT 0,
        FOREIGN KEY (invoice_id) REFERENCES invoices (id) ON DELETE CASCADE
    )
    """)

    # ۴. جدول رسیدها و قبوض ثابت (آب، برق، گاز، اجاره، حقوق)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS fixed_receipts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        receipt_type TEXT NOT NULL,
        worker_name TEXT,
        amount REAL NOT NULL,
        receipt_date TEXT NOT NULL,
        image_path TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # ۵. جدول فاکتورهای فروش و برگشتی مدارس
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales_invoices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        school_name TEXT NOT NULL,
        invoice_type TEXT NOT NULL, -- 'Sales' یا 'Returns'
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (school_name) REFERENCES schools (name) ON DELETE CASCADE
    )
    """)

    # ۶. اقلام ریز فاکتور فروش/برگشتی مدارس
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales_invoice_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sales_invoice_id INTEGER NOT NULL,
        category TEXT NOT NULL,
        food_name TEXT NOT NULL,
        quantity INTEGER NOT NULL DEFAULT 1,
        unit_price REAL NOT NULL DEFAULT 0,
        total_price REAL NOT NULL DEFAULT 0,
        FOREIGN KEY (sales_invoice_id) REFERENCES sales_invoices (id) ON DELETE CASCADE
    )
    """)

    # ۷. جدول مخارج اختصاصی مدارس (School Expenses)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS school_expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        school_name TEXT NOT NULL,
        title TEXT NOT NULL,
        amount REAL NOT NULL,
        expense_date TEXT NOT NULL,
        notes TEXT,
        image_path TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (school_name) REFERENCES schools (name) ON DELETE CASCADE
    )
    """)

    conn.commit()
    conn.close()
    print("✅ دیتابیس لوکال آماده‌سازی شد.")

if __name__ == "__main__":
    init_db()
