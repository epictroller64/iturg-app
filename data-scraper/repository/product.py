from datetime import datetime
from cache_store import CacheStore
from database import get_db_connection, select, execute
from models.Product import Product
import json
from typing import Optional, List
from models.ProductPreviewDTO import ProductPreviewDTO
import asyncio

async def get_all_products_preview(search: Optional[str] = None, page: Optional[int] = 1, page_size: Optional[int] = 10, sort_by: Optional[str] = "updated_at", sort_order: Optional[str] = "desc") -> List[ProductPreviewDTO]:
    """Get all products from the database with their latest prices"""
    
    sort_order = "DESC" if sort_order == "desc" else "ASC"
    
    where_clauses = []
    params = []
    
    if search:
        where_clauses.append("p.name LIKE ?")
        params.append(f"%{search}%")
        
    where_sql = " WHERE " + " AND ".join(where_clauses) if where_clauses else ""
    
    valid_sort_columns = ["updated_at", "price", "name"]
    if sort_by not in valid_sort_columns:
        sort_by = "updated_at"
        
    order_by = f"ORDER BY {sort_by} {sort_order}"
    
    pagination = f"LIMIT {page_size} OFFSET {(page - 1) * page_size}"
    
    query = f'''
        SELECT p.id, p.product_id, p.name, ph.price, p.images, p.platform 
        FROM products AS p 
        LEFT JOIN (
            SELECT product_id, platform, price, found_at
            FROM price_history
            WHERE (product_id, platform, found_at) IN (
                SELECT product_id, platform, MAX(found_at)
                FROM price_history
                GROUP BY product_id, platform
            )
        ) ph ON p.id = ph.product_id AND p.platform = ph.platform
        {where_sql}
        {order_by}
        {pagination}
    '''
    
    rows = await select(query, params)
    
    return [ProductPreviewDTO(
        id=row['id'],
        product_id=row['product_id'],
        name=row['name'],
        price=float(row['price']) if row['price'] is not None else 0.0,
        imageUrl=json.loads(row['images'])[0] if row['images'] and json.loads(row['images']) else "",
        platform=row['platform']
    ) for row in rows]

async def get_all_products() -> List[Product]:
    """Get all products from the database"""
    rows = await select('SELECT * FROM products')
    products = []
    for row in rows:
        row_dict = dict(row)
        row_dict['images'] = json.loads(row_dict['images'])
        row_dict['category'] = json.loads(row_dict['category'])
        products.append(Product(**row_dict))
    return products

async def get_product_by_product_id_and_platform(product_id: str, platform: str, prefer_cache: bool = True) -> Optional[Product]:
    """Get product from the database based on product_id and platform"""
    if prefer_cache:
        product = cache_store.get_product_by_product_id_and_platform(product_id, platform)
        if product:
            return product
    try:
        rows = await select('SELECT * FROM products WHERE product_id = ? AND platform = ?', (product_id, platform))
        if rows:
            result = rows[0]
            product = Product(
                id=result[0],
                product_id=result[1],
                platform=result[2], 
                name=result[3],
                description=result[4],
                category=json.loads(result[5]),
                brand=result[6],
                seller_url=result[7],
                product_url=result[8],
                location=result[9],
                created_at=datetime.fromisoformat(result[10]),
                updated_at=datetime.fromisoformat(result[11]),
                images=json.loads(result[12])
            )
            cache_store.set_product_by_product_id_and_platform(product_id, platform, product)
            return product
        return None
    except Exception as e:
        print(f"Error getting product by product_id and platform: {e}")
        return None

async def get_product(id: int, prefer_cache: bool = True) -> Optional[Product]:
    """Get product from the database based on id"""
    if prefer_cache:
        product = cache_store.get_product(id)
        if product:
            return product
            
    try:
        rows = await select('SELECT * FROM products WHERE id = ?', (id,))
        if rows and len(rows) > 0:
            result = rows[0]
            # Convert tuple to Product object
            product = Product(
                id=result[0],
                product_id=result[1],
                platform=result[2], 
                name=result[3],
                description=result[4],
                category=json.loads(result[5]),
                brand=result[6],
                seller_url=result[7],
                product_url=result[8],
                location=result[9],
                created_at=datetime.fromisoformat(result[10]),
                updated_at=datetime.fromisoformat(result[11]),
                images=json.loads(result[12])
            )
            cache_store.set_product(product.id, product)
            return product
        return None
    except Exception as e:  
        print(f"Error getting product by id: {e}")
        return None

async def upsert_product(product: Product) -> int:
    """Insert or update product in the database"""
    try:
        existing_product = await get_product(product.id, prefer_cache=True)
        
        current_time = datetime.now().isoformat()
        images_json = json.dumps(product.images)
        category_json = json.dumps(product.category)
        lastrowid = None
        if existing_product:
            lastrowid = existing_product.id
            await execute('''
                UPDATE products 
                SET platform=?, name=?, description=?, category=?, brand=?, 
                    seller_url=?, product_url=?, location=?, updated_at=?, images=?
                WHERE id=?
            ''', (product.platform, product.name, product.description, category_json,
                 product.brand, product.seller_url, product.product_url,
                 product.location, current_time, images_json, product.id))
        else:
            lastrowid = await execute('''
                INSERT INTO products (product_id, platform, name, description, category, brand,
                                    seller_url, product_url, location, created_at, updated_at, images)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (product.product_id, product.platform, product.name, product.description,
                 category_json, product.brand, product.seller_url, product.product_url,
                 product.location, current_time, current_time, images_json))
        return lastrowid
    except Exception as e:
        print(f"Error upserting product: {e}")
        raise e



cache_store = CacheStore([])

async def init_cache():
    products = await get_all_products()
    global cache_store
    cache_store = CacheStore(products)

asyncio.run(init_cache())