from models.OkidokiProduct import ScrapedOkidokiProduct
from models.PriceHistory import PriceHistory
from datetime import datetime, timedelta
from factory import LoggerFactory
from models.Product import Product
from repository.product import get_product_by_product_id_and_platform, upsert_product
from pricehistory_pipeline import PriceHistoryPipeline
from models.ScraperConfig import ScraperConfig
from parser import Parser
import asyncio

class ProductPipeline:

    def __init__(self, config: ScraperConfig):
        self.logger = LoggerFactory.get_logger("ProductPipeline")
        self.pricehistory_pipeline = PriceHistoryPipeline()
        self.config = config
        self.parser = Parser()

    def on_product_parsed(self, task: asyncio.Task):
        try:
            task.result()
        except Exception as e:
            self.logger.error(f"Error parsing product: {e}")

    async def process_okidoki_product(self, okidoki_product: ScrapedOkidokiProduct):
        """Process an Okidoki product and insert it into the database, or insert price history if it already exists"""
        existing_product = await get_product_by_product_id_and_platform(okidoki_product.id, "okidoki", prefer_cache=True)
        full_product = Product(
            id=0,
            product_id=okidoki_product.id,
            platform="okidoki",
            name=okidoki_product.name,
            description=okidoki_product.description,
            category=okidoki_product.category,
            brand=okidoki_product.brand,
            seller_url=okidoki_product.seller_url,
            product_url=okidoki_product.product_url,
            location=okidoki_product.location,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            images=okidoki_product.images
        )
        if not existing_product:
            product_table_id = await upsert_product(full_product)
            full_product.id = product_table_id
            await self.pricehistory_pipeline.process_price_history(product_table_id, okidoki_product.price, datetime.now())
            self.logger.info(f"Inserted product {okidoki_product.id} with price {okidoki_product.price}")
            ## Parse product details, 
            task = asyncio.create_task(self.parser.parse_product(full_product))
            task.add_done_callback(self.on_product_parsed)
        # Check last update time to make any insertions
        else:
            if existing_product.updated_at < datetime.now() - timedelta(hours=self.config.hours_between_updates):
                await self.pricehistory_pipeline.process_price_history(existing_product.id, okidoki_product.price, datetime.now())
                full_product.id = existing_product.id
                full_product.created_at = existing_product.created_at
                await upsert_product(full_product)
        self.logger.info(f"Processed product {okidoki_product.id} with price {okidoki_product.price}")
        
