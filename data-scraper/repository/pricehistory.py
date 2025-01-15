from database import get_db_connection
from models.PriceHistory import PriceHistory

def insert_price_history(price_history: PriceHistory):
    """Insert price history into the database"""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO price_history (product_id, platform, price, found_at) VALUES (?, ?, ?, ?)', 
                      (price_history.product_id, price_history.platform, price_history.price, price_history.found_at))
        conn.commit()
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()


def get_price_history(product_id: str):
    """Get price history from the database"""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM price_history WHERE product_id = ?', (product_id,))
        results = cursor.fetchall()
        
        price_histories = []
        for result in results:
            price_history = PriceHistory(
                id=result[0],
                product_id=result[1],
                platform=result[2], 
                price=result[3],
                found_at=result[4]
            )
            price_histories.append(price_history)
            
        return price_histories
    except Exception as e:
        raise e
    finally:
        if conn:
            conn.close()