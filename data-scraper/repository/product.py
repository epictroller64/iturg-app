from datetime import datetime
from cache_store import CacheStore
from database import select, execute
from models.Product import Product
import json
from typing import Optional, List
from models.ProductPreviewDTO import ProductPreviewDTO
from models.PriceHistory import PriceHistory
from repository.groups import get_level2_groups_by_product_table_id, get_level2_groups_by_device

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
        SELECT p.id, p.product_id, p.name, ph.price, p.images, p.platform, l2g.device, l2g.chip, l2g.ram, l2g.screen_size, l2g.generation, l2g.storage, l2g.color, l2g.status, l2g.year, l2g.watch_mm
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
        
    return [ProductPreviewDTO(
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
        watch_mm=row['watch_mm']
    ) for row in rows]

async def get_all_products() -> List[Product]:
    """Get all products from the database"""
    rows = await select('SELECT * FROM products')
    products = []
    for row in rows:
        row_dict = dict(row)
        row_dict['images'] = json.loads(row_dict['images'])
        row_dict['category'] = json.loads(row_dict['category'])
        product = Product(
            id=row_dict['id'],
            product_id=row_dict['product_id'],
            platform=row_dict['platform'],
            name=row_dict['name'],
            description=row_dict['description'],
            category=row_dict['category'],
            brand=row_dict['brand'],
            seller_url=row_dict['seller_url'],
            product_url=row_dict['product_url'],
            location=row_dict['location'],
            created_at=datetime.fromisoformat(row_dict['created_at']),
            updated_at=datetime.fromisoformat(row_dict['updated_at']),
            images=row_dict['images'],
            price_history=[]
        )
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
                images=json.loads(result[12]),
                price_history=[]
            )
            cache_store.set_product_by_product_id_and_platform(product_id, platform, product)
            return product
        return None
    except Exception as e:
        print(f"Error getting product by product_id and platform: {e}")
        return None

async def get_product(product_table_id: int, prefer_cache: bool = True) -> Optional[Product]:
    """Get product from the database based on id"""
    if prefer_cache:
        product = cache_store.get_product(product_table_id)
        if product:
            return product
            
    try:
        rows = await select('SELECT * FROM products  WHERE id = ?', (product_table_id,))
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
                images=json.loads(result[12]),
                price_history=[]
            )

            # Get price history
            price_history_rows = await select('SELECT * FROM price_history WHERE product_table_id = ?', (product.id,))
            product.price_history = [PriceHistory(id=row[0], product_table_id=row[1], price=row[2], found_at=row[3]) for row in price_history_rows]

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


async def get_products_by_level2_group(field: str, value: str) -> List[Product]:
    valid_fields = {'device', 'chip', 'ram', 'screen_size', 'generation', 'storage', 'color', 'status', 'year', 'watch_mm'}
    
    if field not in valid_fields:
        raise ValueError(f"Invalid field: {field}. Allowed fields are: {', '.join(valid_fields)}")
    
    query = f'''
        SELECT p.* 
        FROM products p
        JOIN level2_groups l2g ON p.id = l2g.product_table_id 
        WHERE l2g.{field} = ?
    '''
    
    rows = await select(query, (value,))
    
    products = []
    for row in rows:
        row_dict = dict(row)
        row_dict['images'] = json.loads(row_dict['images'])
        row_dict['category'] = json.loads(row_dict['category'])
        products.append(Product(
            id=row_dict['id'],
            product_id=row_dict['product_id'],
            platform=row_dict['platform'],
            name=row_dict['name'],
            description=row_dict['description'],
            category=row_dict['category'],
            brand=row_dict['brand'],
            seller_url=row_dict['seller_url'],
            product_url=row_dict['product_url'],
            location=row_dict['location'],
            created_at=datetime.fromisoformat(row_dict['created_at']),
            updated_at=datetime.fromisoformat(row_dict['updated_at']),
            images=row_dict['images'],
            price_history=[]
        ))
    return products

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
    
    if product_group.device.lower().startswith("iphone"):
        ## gather same model iphones
        query = f"""
            SELECT p.id, p.product_id, p.name, ph.price, p.images, p.platform, 
                   l2g.device, l2g.chip, l2g.ram, l2g.screen_size, l2g.generation, 
                   l2g.storage, l2g.color, l2g.status, l2g.year, l2g.watch_mm 
            FROM products p 
            JOIN level2_groups l2g ON p.id = l2g.product_table_id
            {price_subquery}
            WHERE l2g.device = ? AND p.id != ?
            LIMIT 10
        """
        rows = await select(query, (product_group.device, product_table_id))
    elif product_group.device.lower().startswith("macbook"):
        ## gather some based on the chip if it exists others add by random macbooks
        if len(product_group.chip) > 0:
            query = f"""
                SELECT p.id, p.product_id, p.name, ph.price, p.images, p.platform,
                       l2g.device, l2g.chip, l2g.ram, l2g.screen_size, l2g.generation,
                       l2g.storage, l2g.color, l2g.status, l2g.year, l2g.watch_mm
                FROM products p 
                JOIN level2_groups l2g ON p.id = l2g.product_table_id
                {price_subquery}
                WHERE l2g.chip = ? AND LOWER(l2g.device) LIKE LOWER(?) AND p.id != ?
                LIMIT 10
            """
            rows = await select(query, (product_group.chip, f"%{product_group.device}%", product_table_id))
        else:
            query = f"""
                SELECT p.id, p.product_id, p.name, ph.price, p.images, p.platform,
                       l2g.device, l2g.chip, l2g.ram, l2g.screen_size, l2g.generation,
                       l2g.storage, l2g.color, l2g.status, l2g.year, l2g.watch_mm
                FROM products p 
                JOIN level2_groups l2g ON p.id = l2g.product_table_id
                {price_subquery}
                WHERE LOWER(l2g.device) LIKE LOWER(?) AND p.id != ?
                LIMIT 10
            """
            rows = await select(query, (f"%{product_group.device}%", product_table_id))
    else:
        # Only gather same device
        query = f"""
            SELECT p.id, p.product_id, p.name, ph.price, p.images, p.platform,
                   l2g.device, l2g.chip, l2g.ram, l2g.screen_size, l2g.generation,
                   l2g.storage, l2g.color, l2g.status, l2g.year, l2g.watch_mm
            FROM products p 
            JOIN level2_groups l2g ON p.id = l2g.product_table_id
            {price_subquery}
            WHERE LOWER(l2g.device) LIKE LOWER(?) AND p.id != ?
            LIMIT 10
        """
        rows = await select(query, (f"%{product_group.device}%", product_table_id))

    return [ProductPreviewDTO(
        id=row['id'],
        platform_product_id=row['product_id'],
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
        watch_mm=row['watch_mm']
    ) for row in rows]


cache_store = CacheStore([])

async def init_cache():
    products = await get_all_products()
    global cache_store
    cache_store = CacheStore(products)
