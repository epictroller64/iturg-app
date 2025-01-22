from repository.product import get_all_products
from product_pipeline import ProductPipeline
from database import execute, select, execute_batch
from models.ScraperConfig import ScraperConfig
from classifier import Classifier
from parser import Parser

async def fix_descriptions():
    """Fix descriptions by removing unwanted elements and adding a new column for the cleaned description"""
    products = await get_all_products()
    product_pipeline = ProductPipeline(config=ScraperConfig(hours_between_updates=1))
    for product in products:
        product = product_pipeline.cleanup_product(product)
        await execute(f"UPDATE products SET description = ? WHERE id = ?", (product.description, product.id))


async def fix_level2_groups():
    """Redoing level2 groups without pulling data from openai. Use existing level1 groups"""
    classifier = Classifier()
    # get level1 groups
    products = await select("SELECT * FROM products")
    for product in products:
        productid = product['id']
        level1_groups = await select("SELECT * FROM level1_groups WHERE product_table_id = ?", (productid,))
        features = [group['group_value'] for group in level1_groups]
        classified = classifier.classify_features(features)
        await execute("INSERT INTO level2_groups (product_table_id, device, chip, ram, screen_size, generation, storage, color, status, year, watch_mm) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (product['id'], classified.device, classified.chip, classified.ram, classified.screen_size, classified.generation, classified.storage, classified.color, classified.status, classified.year, classified.watch_mm))


async def fix_level2_groups_by_title():
    """Skip openai and just split title into different words, then classify"""
    products = await select("SELECT * FROM products")
    classifier = Classifier()
    for product in products:
        title = product['name']
        words = title.split()
        classified = classifier.classify_features(words)
        await execute("INSERT INTO level2_groups (product_table_id, device, chip, ram, screen_size, generation, storage, color, status, year, watch_mm) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (product['id'], classified.device, classified.chip, classified.ram, classified.screen_size, classified.generation, classified.storage, classified.color, classified.status, classified.year, classified.watch_mm))


async def recreate_level1_groups():
    products = await get_all_products()
    parser = Parser()
    classifier = Classifier()
    for product in products:
        openai_response = await parser.ask_openai(product)
        features = openai_response.features
        group1_values = [(feature, product.id) for feature in features]
        await execute_batch('INSERT OR IGNORE INTO level1_groups (group_value, product_table_id) VALUES (?, ?)', group1_values)
        classified = classifier.classify_features(features)
        await execute("INSERT INTO level2_groups (product_table_id, device, chip, ram, screen_size, generation, storage, color, status, year, watch_mm) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (product.id, classified.device, classified.chip, classified.ram, classified.screen_size, classified.generation, classified.storage, classified.color, classified.status, classified.year, classified.watch_mm))
