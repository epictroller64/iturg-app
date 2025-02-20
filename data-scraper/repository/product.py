from datetime import datetime
from cache_store import CacheStore
from database import select, execute
import json
from typing import Optional, List
from models.database.Product import Product
from models.database.PriceHistory import PriceHistory
from models.dto.ProductPreviewDTO import ProductPreviewDTO
from repository.groups import get_level2_groups_by_product_table_id, get_level2_groups_by_device
from repository.postview import get_post_views_by_product_id
from asyncio import gather  # Add this import at the top of the file


def create_product_from_row(row: dict) -> Product:
    """Helper function to create a Product object from a database row"""
    return Product(
        id=row['id'],
        product_id=row['product_id'],
        platform=row['platform'],
        name=row['name'],
        description=row['description'],
        category=json.loads(row['category']) if isinstance(row['category'], str) else row['category'],
        brand=row['brand'],
        seller_url=row['seller_url'],
        product_url=row['product_url'],
        location=row['location'],
        created_at=datetime.fromisoformat(row['created_at']),
        updated_at=datetime.fromisoformat(row['updated_at']),
        images=json.loads(row['images']) if isinstance(row['images'], str) else row['images'],
        price_history=[],
        device=row.get('device', ''),
        chip=row.get('chip', ''),
        ram=row.get('ram', ''),
        screen_size=row.get('screen_size', ''),
        generation=row.get('generation', ''),
        storage=row.get('storage', ''),
        color=row.get('color', ''),
        status=row.get('status', ''),
        year=row.get('year', ''),
        watch_mm=row.get('watch_mm', '')
    )

def create_product_preview_from_row(row: dict) -> ProductPreviewDTO:
    """Helper function to create a ProductPreviewDTO object from a database row"""
    return ProductPreviewDTO(
        platform_product_id=row['product_id'],
        id=row['id'],
        name=row['name'],
        price=float(row['price']) if row['price'] is not None else 0.0,
        imageUrl=json.loads(row['images'])[0] if row['images'] and json.loads(row['images']) else "",
        platform=row['platform'],
        device=row['device'],
        chip=row['chip'],
        ram=row['ram'],
        screen_size=row['screen_size'],
        generation=row['generation'],
        storage=row['storage'],
        color=row['color'],
        status=row['status'],
        year=row['year'],
        watch_mm=row['watch_mm'],
        days_since_added=(datetime.now() - datetime.fromisoformat(str(row['created_at']))).days
    )

async def get_all_products_preview( search: Optional[str] = None,
    page: int = 1,
    page_size: int = 10,
    sort_by: str = "updated_at",
    sort_order: str = "desc",
    filters: Optional[str] = None) -> List[ProductPreviewDTO]:
    """Get all products from the database with their latest prices"""
    
    sort_order = "DESC" if sort_order == "desc" else "ASC"
    
    where_clauses = []
    params = []


    if filters:
        try:
            filter_dict = json.loads(filters)
            for field, value in filter_dict.items():
                if field == "minPrice":
                    where_clauses.append("ph.price >= ?")
                    params.append(value)
                elif field == "maxPrice":
                    where_clauses.append("ph.price <= ?")
                    params.append(value)
                else:
                    where_clauses.append(f"l2g.{field} = ?")
                    params.append(value)
        except Exception as e:
            print(f"Error parsing filters: {e}")
    
    if search:
        where_clauses.append("p.name LIKE ?")
        params.append(f"%{search}%")
        
    where_sql = " WHERE " + " AND ".join(where_clauses) if where_clauses else ""
    
    valid_sort_columns = ["updated_at", "price", "name"]
    if sort_by not in valid_sort_columns:
        sort_by = "created_at"
        
    # Map sort columns to their fully qualified names
    sort_column_map = {
        "created_at": "p.created_at",
        "price": "ph.price",
        "name": "p.name"
    }
    
    qualified_sort_by = sort_column_map[sort_by]
    order_by = f"ORDER BY {qualified_sort_by} {sort_order}"
    
    pagination = f"LIMIT {page_size} OFFSET {(page - 1) * page_size}"
    
    query = f'''
        SELECT p.id, p.product_id, p.name, ph.price, p.images, p.platform, l2g.device, l2g.chip, l2g.ram, l2g.screen_size, l2g.generation, l2g.storage, l2g.color, l2g.status, l2g.year, l2g.watch_mm, p.created_at
        FROM products AS p 
        JOIN level2_groups l2g ON p.id = l2g.product_table_id
        LEFT JOIN (
            SELECT product_table_id,  price, found_at
            FROM price_history
            WHERE (product_table_id, found_at) IN (
                SELECT product_table_id, MAX(found_at)
                FROM price_history
                GROUP BY product_table_id
            )
        ) ph ON p.id = ph.product_table_id
        {where_sql}
        {order_by}
        {pagination}
    '''
    
    rows = await select(query, params)
    if not rows:
        return []
        
    return [create_product_preview_from_row(row) for row in rows]

async def get_all_products() -> List[Product]:
    """Get all products from the database"""
    rows = await select('SELECT * FROM products LEFT JOIN level2_groups l2g ON products.id = l2g.product_table_id')
    products = []
    for row in rows:
        row_dict = dict(row)
        product = create_product_from_row(row_dict)
        # fill price history
        price_history_rows = await select('SELECT * FROM price_history WHERE product_table_id = ?', (row_dict['id'],))
        product.price_history = [PriceHistory(id=row[0], product_table_id=row[1], price=row[2], found_at=row[3]) for row in price_history_rows]
        products.append(product)
    return products

async def get_product_by_product_id_and_platform(product_id: str, platform: str, prefer_cache: bool = True) -> Optional[Product]:
    """Get product from the database based on product_id and platform"""
    if prefer_cache:
        product = cache_store.get_product_by_product_id_and_platform(product_id, platform)
        if product:
            return product
    try:
        rows = await select('SELECT * FROM products LEFT JOIN level2_groups l2g ON products.id = l2g.product_table_id WHERE product_id = ? AND platform = ?', (product_id, platform))
        if rows:
            product = create_product_from_row(dict(rows[0]))
            cache_store.set_product_by_product_id_and_platform(product_id, platform, product)
            return product
        return None
    except Exception as e:
        print(f"Error getting product by product_id and platform: {e}")
        return None

async def get_product(product_table_id: int, prefer_cache: bool = True) -> Optional[Product]:
    """Get product from the database based on id"""
    if product_table_id == 0:
        return None
    if prefer_cache:
        product = cache_store.get_product(product_table_id)
        if product:
            return product
            
    try:
        rows = await select('SELECT * FROM products p LEFT JOIN level2_groups l2g ON p.id = l2g.product_table_id WHERE p.id = ? ', (product_table_id,))
        if rows and len(rows) > 0:
            product = create_product_from_row(dict(rows[0]))

            # Get price history and post views concurrently
            price_history_rows, post_views = await gather(
                select('SELECT * FROM price_history WHERE product_table_id = ?', (product.id,)),
                get_post_views_by_product_id(product.id)
            )
            
            product.price_history = [PriceHistory(id=row[0], product_table_id=row[1], price=row[2], found_at=row[3]) for row in price_history_rows]
            product.post_views = post_views[0].view_count if post_views else 0

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

async def get_products_by_level2_group(field: str, value: str) -> List[ProductPreviewDTO]:
    valid_fields = {'device', 'chip', 'ram', 'screen_size', 'generation', 'storage', 'color', 'status', 'year', 'watch_mm'}
    
    if field not in valid_fields:
        raise ValueError(f"Invalid field: {field}. Allowed fields are: {', '.join(valid_fields)}")
    
    query = f'''
        SELECT p.id, p.product_id, p.name, ph.price, p.images, p.platform,
               l2g.device, l2g.chip, l2g.ram, l2g.screen_size, l2g.generation,
               l2g.storage, l2g.color, l2g.status, l2g.year, l2g.watch_mm
        FROM products p
        JOIN level2_groups l2g ON p.id = l2g.product_table_id 
        LEFT JOIN (
            SELECT product_table_id, price, found_at
            FROM price_history
        WHERE l2g.{field} = ?
    '''
    
    rows = await select(query, (value,))
    return [create_product_from_row(dict(row)) for row in rows]

async def get_similar_products(product_table_id: int) -> List[ProductPreviewDTO]:
    """Get similar products based on the product_table_id, excluding the original product"""
    # get original product level2 groups
    original_product_groups = await get_level2_groups_by_product_table_id(product_table_id)
    if not original_product_groups or len(original_product_groups) == 0:
        return []
    product_group = original_product_groups[0]
    if len(product_group.device) == 0:
        return []
    
    price_subquery = """
        LEFT JOIN (
            SELECT product_table_id, price, found_at
            FROM price_history
            WHERE (product_table_id, found_at) IN (
                SELECT product_table_id, MAX(found_at)
                FROM price_history
                GROUP BY product_table_id
            )
        ) ph ON p.id = ph.product_table_id
    """
    
    base_query = f"""
        SELECT p.id, p.product_id, p.name, ph.price, p.images, p.platform,
               l2g.device, l2g.chip, l2g.ram, l2g.screen_size, l2g.generation,
               l2g.storage, l2g.color, l2g.status, l2g.year, l2g.watch_mm,
               p.created_at
        FROM products p 
        JOIN level2_groups l2g ON p.id = l2g.product_table_id
        {price_subquery}
    """
    
    if product_group.device.lower().startswith("iphone"):
        query = f"{base_query} WHERE l2g.device = ? AND p.id != ? LIMIT 10"
        params = (product_group.device, product_table_id)
    elif product_group.device.lower().startswith("macbook") and product_group.chip:
        query = f"{base_query} WHERE l2g.chip = ? AND LOWER(l2g.device) LIKE LOWER(?) AND p.id != ? LIMIT 10"
        params = (product_group.chip, f"%{product_group.device}%", product_table_id)
    else:
        query = f"{base_query} WHERE LOWER(l2g.device) LIKE LOWER(?) AND p.id != ? LIMIT 10"
        params = (f"%{product_group.device}%", product_table_id)

    rows = await select(query, params)
    return [create_product_preview_from_row(row) for row in rows]

async def get_products_by_ids(ids: List[str]) -> List[ProductPreviewDTO]:
    """Get products by ids"""
    if not ids:
        return []
        
    placeholders = ','.join(['?' for _ in ids])
    query = f'''
        SELECT p.id, p.product_id, p.name, ph.price, p.images, p.platform,
               l2g.device, l2g.chip, l2g.ram, l2g.screen_size, l2g.generation,
               l2g.storage, l2g.color, l2g.status, l2g.year, l2g.watch_mm,
               p.created_at
        FROM products p
        JOIN level2_groups l2g ON p.id = l2g.product_table_id
        LEFT JOIN (
            SELECT product_table_id, price, found_at
            FROM price_history
            WHERE (product_table_id, found_at) IN (
                SELECT product_table_id, MAX(found_at)
                FROM price_history
                GROUP BY product_table_id
            )
        ) ph ON p.id = ph.product_table_id
        WHERE p.id IN ({placeholders})
    '''
    rows = await select(query, ids)
    return [create_product_preview_from_row(row) for row in rows]

async def delete_product(product_table_id: int):
    """Delete product from the database"""
    await execute('DELETE FROM products WHERE id = ?', (product_table_id,))

async def insert_product_to_archive(product: Product):
    """Insert product to the archive table"""
    images_json = json.dumps(product.images)
    category_json = json.dumps(product.category)
    await execute('INSERT INTO products_archive (product_id, platform, name, description, category, brand, seller_url, product_url, location, created_at, updated_at, images) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (product.product_id, product.platform, product.name, product.description, category_json, product.brand, product.seller_url, product.product_url, product.location, product.created_at, product.updated_at, images_json))


cache_store = CacheStore([])

async def init_cache():
    products = await get_all_products()
    global cache_store
    cache_store = CacheStore(products)
