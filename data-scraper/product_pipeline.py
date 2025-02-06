from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from typing import Optional, Tuple
from factory import LoggerFactory
from repository.product import get_product_by_product_id_and_platform, upsert_product
from pricehistory_pipeline import PriceHistoryPipeline
from parser import Parser
import asyncio
from repository.product import delete_product, insert_product_to_archive
from models.scraping.ScrapedOkidokiProduct import ScrapedOkidokiProduct
from models.scraping.ScrapedSoovProduct import ScrapedSoovProduct
from models.scraping.ScrapedHVProduct import ScrapedHVProduct
from models.scraping.ScraperConfig import ScraperConfig
from models.database.Product import Product

class ProductPipeline:

    PLATFORM_OKIDOKI = "okidoki"
    PLATFORM_SOOV = "soov"
    PLATFORM_HINNAVAATLUS = "hinnavaatlus"
    SOOV_TECH_CATEGORY = "Elektroonika"

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

    async def _process_base_product(self, product_data: ScrapedOkidokiProduct | ScrapedSoovProduct | ScrapedHVProduct, platform: str, cleanup_func) -> Tuple[Optional[Product], Product]:
        product_id = product_data.product_id
        existing_product = await get_product_by_product_id_and_platform(product_id, platform, prefer_cache=False)
        
        cleaned_description = cleanup_func(product_data)
        full_product = Product(
            id=0,
            product_id=product_id,
            platform=platform,
            name=product_data.name,
            description=cleaned_description,
            category=product_data.categories,
            brand=product_data.brand,
            seller_url=product_data.seller_url,
            product_url=product_data.product_url,
            location=product_data.location,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            images=product_data.images,
            price_history=[]
        )
        
        return existing_product, full_product

    async def process_okidoki_product(self, okidoki_product: ScrapedOkidokiProduct):
        """Process an Okidoki product and insert it into the database, or insert price history if it already exists"""
        try:
            existing_product, full_product = await self._process_base_product(
                okidoki_product, self.PLATFORM_OKIDOKI, self.cleanup_product
            )
            now = datetime.now()
            if not existing_product:
                product_table_id = await upsert_product(full_product)
                full_product.id = product_table_id
                await self.pricehistory_pipeline.process_price_history(product_table_id, okidoki_product.price, now)
                self.logger.info(f"Inserted product {okidoki_product.product_id} with price {okidoki_product.price}")
                task = asyncio.create_task(self.parser.parse_product(full_product))
                task.add_done_callback(self.on_product_parsed)
            else:
                if not okidoki_product.active:
                    await self.archive_product(existing_product)
                    return
                else:
                    if existing_product.updated_at < now - timedelta(hours=self.config.hours_between_updates):
                        await self.pricehistory_pipeline.process_price_history(existing_product.id, okidoki_product.price, now)
                        full_product.id = existing_product.id
                        full_product.created_at = existing_product.created_at
                        await upsert_product(full_product)

            self.logger.info(f"Processed product {okidoki_product.product_id} with price {okidoki_product.price}")
        except Exception as e:
            self.logger.error(f"Error processing Okidoki product {okidoki_product.product_id}: {str(e)}")
            raise

    def cleanup_product(self, product: ScrapedOkidokiProduct):
        soup = BeautifulSoup(product.description, 'html.parser')
        for element in soup.select('.a.hidden.description-trigger, .item-specifics, .location, .item-specifics-list'):
            element.decompose()
        return str(soup)

    async def process_soov_product(self, soov_product: ScrapedSoovProduct):
        """Process a SOOV product and insert into database, or insert price history if existing"""
        try:
            if self.SOOV_TECH_CATEGORY.lower() not in [category.lower() for category in soov_product.categories]:
                return

            existing_product, full_product = await self._process_base_product(
                soov_product, self.PLATFORM_SOOV, self.cleanup_soov_product
            )
            if not existing_product:
                product_table_id = await upsert_product(full_product)
                full_product.id = product_table_id
                await self.pricehistory_pipeline.process_price_history(product_table_id, soov_product.price, datetime.now())
                self.logger.info(f"Inserted SOOV product {soov_product.product_id} with price {soov_product.price}")
                task = asyncio.create_task(self.parser.parse_product(full_product))
                task.add_done_callback(self.on_product_parsed)
            else:
                if not soov_product.active:
                    await self.archive_product(existing_product)
                    return
                else:
                    if existing_product.updated_at < datetime.now() - timedelta(hours=self.config.hours_between_updates):
                        await self.pricehistory_pipeline.process_price_history(existing_product.id, soov_product.price, datetime.now())
                        full_product.id = existing_product.id
                        full_product.created_at = existing_product.created_at
                        await upsert_product(full_product)
            self.logger.info(f"Processed SOOV product {soov_product.product_id} with price {soov_product.price}")
        except Exception as e:
            self.logger.error(f"Error processing SOOV product {soov_product.product_id}: {str(e)}")
            raise

    async def process_hinnavaatlus_product(self, hv_product: ScrapedHVProduct):
        """Process a Hinnavaatlus product and insert into database"""
        try:
            existing_product = await get_product_by_product_id_and_platform(
                hv_product.product_id,
                self.PLATFORM_HINNAVAATLUS,
                prefer_cache=False
            )
            full_product = Product(
                id=0,
                product_id=hv_product.product_id,
                platform=self.PLATFORM_HINNAVAATLUS,
                name=hv_product.name,
                description=hv_product.description,
                category=hv_product.categories,
                brand=hv_product.brand,
                seller_url=hv_product.seller_url,
                product_url=hv_product.product_url,
                location=hv_product.location,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                images=hv_product.images,
                price_history=[]
            )
            
            if not existing_product:
                product_table_id = await upsert_product(full_product)
                full_product.id = product_table_id
                await self.pricehistory_pipeline.process_price_history(product_table_id, hv_product.price, datetime.now())
                self.logger.info(f"Inserted Hinnavaatlus product {hv_product.product_id}")
                task = asyncio.create_task(self.parser.parse_product(full_product))
                task.add_done_callback(self.on_product_parsed)
            else:
                if not hv_product.active:
                    await self.archive_product(existing_product)
                    return
                else:
                    if existing_product.updated_at < datetime.now() - timedelta(hours=self.config.hours_between_updates):
                        await self.pricehistory_pipeline.process_price_history(existing_product.id, hv_product.price, datetime.now())

            self.logger.info(f"Processed Hinnavaatlus product {hv_product.product_id}")
        except Exception as e:
            self.logger.error(f"Error processing Hinnavaatlus product {hv_product.product_id}: {str(e)}")
            raise

    def cleanup_soov_product(self, product: ScrapedSoovProduct):
        """SOOV-specific HTML cleanup logic"""
        return product.description
    
    async def archive_product(self, product: Product):
        await delete_product(product.id)
        await insert_product_to_archive(product)
