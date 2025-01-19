from database import execute, select
from models.PriceHistory import PriceHistory

async def insert_price_history(price_history: PriceHistory):
    """Insert price history into the database"""
    try:
        await execute('INSERT INTO price_history (product_table_id, price, found_at) VALUES (?, ?, ?)', 
                      (price_history.product_table_id, price_history.price, price_history.found_at))
    except Exception as e:
        raise e


async def get_price_history(product_id: str):
    """Get price history from the database"""
    try:
        results = await select('SELECT * FROM price_history WHERE product_id = ?', (product_id,))
        
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
