import aiosqlite
import os
from typing import List
from aiosqlite import Row
import asyncio
# Add at the top of the file with other imports
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATABASE_PATH = os.path.join(PROJECT_ROOT, 'products.db')

async def execute_batch(query: str, params: List[tuple]):
    """Execute a batch of queries"""
    try:
        conn = await get_db_connection()
        cursor = await conn.cursor()
        await cursor.executemany(query, params)
        await conn.commit()
        await conn.close()
    except Exception as e:
        await conn.rollback()
        await conn.close()
        await cursor.close()
        raise e

async def execute(query: str, params: tuple = ()):
    """Execute a query and return the lastrowid"""
    conn = await get_db_connection()
    cursor = await conn.cursor()
    try:
        await cursor.execute(query, params)
        lastrowid = cursor.lastrowid
        await conn.commit()
        await conn.close()
        return lastrowid
    except Exception as e:
        try:
            await conn.rollback()
            await conn.close()
            await cursor.close()
        except Exception:
            pass
        raise e


async def select(query: str, params: tuple = ()) -> List[Row]:
    """Select a query and return the rows"""
    conn = await get_db_connection()
    cursor = await conn.cursor()
    try:
        cursor.row_factory = aiosqlite.Row
        await cursor.execute(query, params)
        rows = await cursor.fetchall()
        await cursor.close()
        await conn.close()
        return rows
    except Exception as e:
        print(e)
        await conn.rollback()
        await conn.close()
        await cursor.close()
        raise e

async def get_db_connection():
    """Get SQLite database connection"""
    return await aiosqlite.connect(DATABASE_PATH)

async def setup_database():
    """Initialize SQLite database and create necessary tables"""
    conn = await get_db_connection()
    cursor = await conn.cursor()
    
    await cursor.execute('''
        CREATE TABLE IF NOT EXISTS products_archive (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id TEXT NOT NULL,
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
    await cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id TEXT NOT NULL,
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

    await cursor.execute('''
        CREATE TABLE IF NOT EXISTS price_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_table_id INTEGER NOT NULL,
            price REAL,
            found_at TIMESTAMP
        )
    ''')
    await cursor.execute(""
                   "CREATE TABLE IF NOT EXISTS level1_groups ( "
                   "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                   "group_value TEXT NOT NULL, "
                   "product_table_id INTEGER NOT NULL "
                   ")"
                   )

    # Level 2 groups are created based on the level 1 groups, a more precise grouping
    await cursor.execute(""
                   "CREATE TABLE IF NOT EXISTS level2_groups ( "
                   "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                   "product_table_id INTEGER NOT NULL, "
                   "device TEXT, "
                   "chip TEXT, "
                   "ram TEXT, "
                   "screen_size TEXT, "
                   "generation TEXT, "
                   "storage TEXT, "
                   "color TEXT, "
                   "status TEXT, "
                   "year TEXT, "
                   "watch_mm TEXT "
                   ")"
                   )
    
    await conn.commit()
    await conn.close()
