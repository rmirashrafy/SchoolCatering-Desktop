import sqlite3

DB_NAME = "kitchen_erp.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # users 
    cursor.execute('''
     CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        full_name TEXT NOT NULL,
        role TEXT CHECK(role IN ('Admin', 'Staff')) NOT NULL,
        is_active INTEGER DEFAULT 1
    );
    ''')

    # schools
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS schools (
        school_id INTEGER PRIMARY KEY AUTOINCREMENT,
        school_name TEXT NOT NULL,
        address TEXT,
        phone TEXT,
        is_active INTEGER DEFAULT 1
    );
    ''')

    # school_staff
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS school_staff (
        staff_id INTEGER PRIMARY KEY AUTOINCREMENT,
        school_id INTEGER NOT NULL,
        full_name TEXT NOT NULL,
        phone TEXT,
        role_title TEXT,
        is_active INTEGER DEFAULT 1,
        FOREIGN KEY (school_id) REFERENCES schools(school_id)
    );
    ''')

    # items
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS items (
        item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name TEXT NOT NULL,
        item_type TEXT CHECK(item_type IN ('Raw_Material', 'Prepared_Food', 'Prepackaged')) NOT NULL,
        unit_of_measure TEXT NOT NULL,
        current_stock REAL DEFAULT 0.0,
        cost_price REAL DEFAULT 0.0,
        selling_price REAL DEFAULT 0.0
    );
    ''')

    # school_canteen_menu
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS school_canteen_menu (
        menu_id INTEGER PRIMARY KEY AUTOINCREMENT,
        school_id INTEGER NOT NULL,
        item_id INTEGER NOT NULL,
        default_quantity REAL DEFAULT 0.0,
        FOREIGN KEY (school_id) REFERENCES schools(school_id),
        FOREIGN KEY (item_id) REFERENCES items(item_id),
        UNIQUE(school_id, item_id)
    );
    ''')

    # expense_categories
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS expense_categories (
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_name TEXT UNIQUE NOT NULL
    );
    ''')

    # expenses
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        expense_date DATETIME DEFAULT CURRENT_TIMESTAMP,
        description TEXT,
        school_id INTEGER,
        worker_id INTEGER,
        created_by_user_id INTEGER NOT NULL,
        FOREIGN KEY (category_id) REFERENCES expense_categories(category_id),
        FOREIGN KEY (school_id) REFERENCES schools(school_id),
        FOREIGN KEY (worker_id) REFERENCES users(user_id),
        FOREIGN KEY (created_by_user_id) REFERENCES users(user_id)
    );
    ''')

    # orders 
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        school_id INTEGER NOT NULL,
        school_staff_id INTEGER,
        created_by_user_id INTEGER NOT NULL,
        order_type TEXT CHECK(order_type IN ('Delivery', 'Return')) NOT NULL,
        order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
        total_amount REAL DEFAULT 0.0,
        status TEXT CHECK(status IN ('Draft', 'Finalized', 'Canceled')) DEFAULT 'Draft',
        notes TEXT,
        FOREIGN KEY (school_id) REFERENCES schools(school_id),
        FOREIGN KEY (school_staff_id) REFERENCES school_staff(staff_id),
        FOREIGN KEY (created_by_user_id) REFERENCES users(user_id)
    );
    ''')

    # order_items
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS order_items (
        order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        item_id INTEGER NOT NULL,
        quantity REAL NOT NULL,
        unit_price REAL,
        total_price REAL NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders(order_id),
        FOREIGN KEY (item_id) REFERENCES items(item_id)
    );
    ''')

    # order_returns
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS order_returns (
        return_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        processed_by_user_id INTEGER NOT NULL,
        return_date DATETIME DEFAULT CURRENT_TIMESTAMP,
        total_return_credit REAL DEFAULT 0.0,
        FOREIGN KEY (order_id) REFERENCES orders(order_id),
        FOREIGN KEY (processed_by_user_id) REFERENCES users(user_id)
    );
    ''')

    # order_return_items  
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS order_return_items (
        return_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        return_id INTEGER NOT NULL,
        item_id INTEGER NOT NULL,
        returned_quantity REAL NOT NULL,
        disposition TEXT CHECK(disposition IN ('Restock', 'Waste')) NOT NULL,
        credit_amount REAL NOT NULL,
        FOREIGN KEY (return_id) REFERENCES order_returns(return_id),
        FOREIGN KEY (item_id) REFERENCES items(item_id)
    );
    ''')

    conn.commit()
    conn.close()
    print("build successfully.")

if __name__ == "__main__":
    init_db()
