from repository.postview import get_post_view, update_post_view, create_post_view


async def increment_post_view(product_table_id: int):
    """Increment the post view count by 1"""
    post_view = await get_post_view(product_table_id)
    if post_view:
        await update_post_view(post_view.id, post_view.view_count + 1)
    else:
        await create_post_view(product_table_id, 1)


async def get_post_view_count(product_table_id: int):
    """Get the post view count"""
    post_view = await get_post_view(product_table_id)
    return post_view.view_count if post_view else 0




