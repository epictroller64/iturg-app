import sqlite3


def get_db_connection():
    """Get SQLite database connection"""
    return sqlite3.connect('products.db')

def setup_database():
    """Initialize SQLite database and create necessary tables"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id TEXT PRIMARY KEY,
            platform TEXT NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            category TEXT,
            brand TEXT,
            seller_url TEXT,
            product_url TEXT,
            location TEXT,
            created_at TIMESTAMP,
            updated_at TIMESTAMP,
            images TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS price_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id TEXT NOT NULL,
            platform TEXT NOT NULL,
            price REAL,
            found_at TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

setup_database()