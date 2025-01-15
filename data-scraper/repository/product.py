from datetime import datetime
from cache_store import CacheStore
from database import get_db_connection
from models.Product import Product
import json
from typing import Optional, List
from models.ProductPreviewDTO import ProductPreviewDTO

def get_all_products_preview() -> List[ProductPreviewDTO]:
    """Get all products from the database"""
    products = get_all_products()
    return [ProductPreviewDTO(**product) for product in products]

def get_all_products() -> List[Product]:
    """Get all products from the database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    products = [Product(**row) for row in cursor.fetchall()]
    return products

def get_product(product_id: str, prefer_cache: bool = True) -> Optional[Product]:
    """Get product from the database"""
    if prefer_cache:
        product = cache_store.get_product(product_id)
        if product:
            return product
            
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
        result = cursor.fetchone()
        if result:
            # Convert tuple to Product object
            product = Product(
                id=result[0],
                platform=result[1], 
                name=result[2],
                description=result[3],
                category=result[4],
                brand=result[5],
                seller_url=result[6],
                product_url=result[7],
                location=result[8],
                created_at=datetime.fromisoformat(result[9]),
                updated_at=datetime.fromisoformat(result[10]),
                images=json.loads(result[11])
            )
            cache_store.set_product(product.id, product)
            return product
        return None
    finally:
        cursor.close()
        conn.close()

def insert_product(product: Product) -> None:
    """Insert or update product in the database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('SELECT id FROM products WHERE id = ?', (product.id,))
        exists = cursor.fetchone()
        
        current_time = datetime.now().isoformat()
        images_json = json.dumps(product.images)
        
        if exists:
            cursor.execute('''
                UPDATE products 
                SET platform=?, name=?, description=?, category=?, brand=?, 
                    seller_url=?, product_url=?, location=?, updated_at=?, images=?
                WHERE id=?
            ''', (product.platform, product.name, product.description, product.category,
                 product.brand, product.seller_url, product.product_url,
                 product.location, current_time, images_json, product.id))
        else:
            cursor.execute('''
                INSERT INTO products (id, platform, name, description, category, brand,
                                    seller_url, product_url, location, created_at, updated_at, images)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (product.id, product.platform, product.name, product.description,
                 product.category, product.brand, product.seller_url, product.product_url,
                 product.location, current_time, current_time, images_json))
        
        conn.commit()
    finally:
        cursor.close()
        conn.close()



cache_store = CacheStore(get_all_products())