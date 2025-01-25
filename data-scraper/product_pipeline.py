from models.OkidokiProduct import ScrapedOkidokiProduct
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from factory import LoggerFactory
from models.Product import Product
from repository.product import get_product_by_product_id_and_platform, upsert_product
from pricehistory_pipeline import PriceHistoryPipeline
from models.ScraperConfig import ScraperConfig
from parser import Parser
import asyncio
from models.SoovProduct import SoovProduct

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
        existing_product = await get_product_by_product_id_and_platform(okidoki_product.id, "okidoki", prefer_cache=False)
        full_product = Product(
            id=0,
            product_id=okidoki_product.id,
            platform="okidoki",
            name=okidoki_product.name,
            description=self.cleanup_product(okidoki_product),
            category=okidoki_product.category,
            brand=okidoki_product.brand,
            seller_url=okidoki_product.seller_url,
            product_url=okidoki_product.product_url,
            location=okidoki_product.location,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            images=okidoki_product.images,
            price_history=[]
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
        
    def cleanup_product(self, product: ScrapedOkidokiProduct):
        soup = BeautifulSoup(product.description, 'html.parser')
        # remove unneeded elements 
        for element in soup.select('.a.hidden.description-trigger, .item-specifics, .location, .item-specifics-list'):
            element.decompose()
        product.description = str(soup)
        return product.description

    async def process_soov_product(self, soov_product: SoovProduct):
        """Process a SOOV product and insert into database, or insert price history if existing"""

        #skip product if category is not tech
        if "Elektroonika" not in soov_product.category:
            self.logger.info(f"Skipping SOOV product {soov_product.product_id} with category {soov_product.category}")
            return

        existing_product = await get_product_by_product_id_and_platform(soov_product.product_id, "soov", prefer_cache=False)
        full_product = Product(
            id=0,
            product_id=soov_product.product_id,
            platform="soov",
            name=soov_product.name,
            description=self.cleanup_soov_product(soov_product),
            category=soov_product.category,
            brand=soov_product.brand,
            seller_url=soov_product.seller_url,
            product_url=soov_product.product_url,
            location=soov_product.location,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            images=soov_product.images,
            price_history=[]
        )
        
        if not existing_product:
            product_table_id = await upsert_product(full_product)
            full_product.id = product_table_id
            await self.pricehistory_pipeline.process_price_history(product_table_id, soov_product.price, datetime.now())
            self.logger.info(f"Inserted SOOV product {soov_product.product_id} with price {soov_product.price}")
            task = asyncio.create_task(self.parser.parse_product(full_product))
            task.add_done_callback(self.on_product_parsed)
        else:
            if existing_product.updated_at < datetime.now() - timedelta(hours=self.config.hours_between_updates):
                await self.pricehistory_pipeline.process_price_history(existing_product.id, soov_product.price, datetime.now())
                full_product.id = existing_product.id
                full_product.created_at = existing_product.created_at
                await upsert_product(full_product)
        self.logger.info(f"Processed SOOV product {soov_product.product_id} with price {soov_product.price}")

    def cleanup_soov_product(self, product: SoovProduct):
        """SOOV-specific HTML cleanup logic"""
        return product.description
