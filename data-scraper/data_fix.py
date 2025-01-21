from repository.product import get_all_products
from product_pipeline import ProductPipeline
from database import execute
from models.ScraperConfig import ScraperConfig


async def fix_descriptions():
    """Fix descriptions by removing unwanted elements and adding a new column for the cleaned description"""
    products = await get_all_products()
    product_pipeline = ProductPipeline(config=ScraperConfig(hours_between_updates=1))
    for product in products:
        product = product_pipeline.cleanup_product(product)
        await execute(f"UPDATE products SET description = ? WHERE id = ?", (product.description, product.id))