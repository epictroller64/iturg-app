from typing import List, Optional
from models.database.PostView import PostView
from database import execute, select


async def create_post_view(product_table_id: int, view_count: int) -> int:
    """Create a new post view record"""
    query = """
        INSERT INTO post_views (product_table_id, view_count)
        VALUES (?, ?)
    """
    return await execute(query, (product_table_id, view_count))


async def get_post_view(id: int) -> Optional[PostView]:
    """Get a post view by id"""
    query = """
        SELECT * FROM post_views WHERE id = ?
    """
    rows = await select(query, (id,))
    if not rows:
        return None
    return PostView(**dict(rows[0]))


async def get_post_views_by_product_id(product_table_id: int) -> List[PostView]:
    """Get all post views for a product"""
    query = """
        SELECT * FROM post_views WHERE product_table_id = ?
    """
    rows = await select(query, (product_table_id,))
    return [PostView(**dict(row)) for row in rows]


async def update_post_view(id: int, view_count: int) -> None:
    """Update a post view's count"""
    query = """
        UPDATE post_views 
        SET view_count = ?
        WHERE id = ?
    """
    await execute(query, (view_count, id))


async def delete_post_view(id: int) -> None:
    """Delete a post view"""
    query = """
        DELETE FROM post_views WHERE id = ?
    """
    await execute(query, (id,))


async def increment_view_count(id: int) -> None:
    """Increment the view count by 1"""
    query = """
        UPDATE post_views
        SET view_count = view_count + 1
        WHERE id = ?
    """
    await execute(query, (id,))
