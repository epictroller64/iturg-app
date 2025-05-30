from product_pipeline import ProductPipeline
from pricehistory_pipeline import PriceHistoryPipeline
from datetime import datetime, timedelta
from factory import LoggerFactory
from repository.product import get_product_by_product_id_and_platform
from typing import List, Set
import asyncio
from backup_manager import BackupManager
from services.scraping.okidoki import OkidokiScraper
from services.scraping.soov import SoovScraper
from services.scraping.hinnavaatlus import HinnavaatlusScraper
from models.scraping import ScraperConfig
from inspect import iscoroutinefunction

class Scraper:

    okidoki_scraper: OkidokiScraper
    soov_scraper: SoovScraper
    hinnavaatlus_scraper: HinnavaatlusScraper
    product_pipeline: ProductPipeline
    pricehistory_pipeline: PriceHistoryPipeline
    config: ScraperConfig
    next_scrape_time: datetime
    backup_manager: BackupManager

    def __init__(self, config: ScraperConfig):
        self.okidoki_scraper = OkidokiScraper(config)
        self.soov_scraper = SoovScraper(config)
        self.hinnavaatlus_scraper = HinnavaatlusScraper(config)
        self.product_pipeline = ProductPipeline(config)
        self.pricehistory_pipeline = PriceHistoryPipeline()
        self.config = config
        self.next_scrape_time = datetime.now()
        self.backup_manager = BackupManager()
        self.logger = LoggerFactory.get_logger("Scraper")
    

    async def update_product_details(self):
        pass

    async def scrape_apple_products(self):
        """Scrape apple products from across different platforms (marketplaces)"""
        while True:
            if self.next_scrape_time < datetime.now():
                self.logger.info(f"Starting apple scraper at {datetime.now()}")
                self.backup_manager.create_backup()
                await self.scrape_hinnavaatlus_products()
                await self.scrape_okidoki_products(["apple", "iphone", "imac", "macbook", "ipad"])
                await self.scrape_soov_products(["apple", "iphone", "imac", "macbook", "ipad"])

                self._update_next_scrape_time()
            else:
                self.logger.info(f"Waiting for next scrape at {self.next_scrape_time}")
                await asyncio.sleep(1)

    async def scrape_hinnavaatlus_products(self):
        products = self.hinnavaatlus_scraper.scrape_products()
        await self._process_products(products, "hinnavaatlus", self.hinnavaatlus_scraper.scrape_product_details)

    async def scrape_soov_products(self, keywords: List[str]):
        products = []
        for keyword in keywords:
            products.extend(self.soov_scraper.scrape_by_keyword(keyword))
        await self._process_products(products, "soov", self.soov_scraper.scrape_product_details)

    async def scrape_okidoki_products(self, keywords: List[str]):
        products = []
        for keyword in keywords:
            products.extend(self.okidoki_scraper.scrape_by_keyword(keyword))
        await self._process_products(products, "okidoki", self.okidoki_scraper.scrape_product_details)

    def _update_next_scrape_time(self):
        self.next_scrape_time = datetime.now() + timedelta(seconds=self.config.time_between_scrapes)
        self.logger.info(f"Next scrape at {self.next_scrape_time}")

    async def _process_products(self, products, platform, processor):
        seen_ids: Set[str] = set()
        unique_products = [p for p in products if not (p.id in seen_ids or seen_ids.add(p.id))]
        
        self.logger.info(f"Found {len(unique_products)} unique {platform} products")
        
        for product in unique_products:
            if (existing_product := await get_product_by_product_id_and_platform(
                product.id, platform, prefer_cache=True
            )) and existing_product.updated_at > datetime.now() - timedelta(hours=self.config.hours_between_updates):
                self.logger.info(f"Product {product.id} has been recently scraped, skipping...")
                continue
            
            full_products = await processor(product) if iscoroutinefunction(processor) else processor(product)
            for full_product in full_products:
                await getattr(self.product_pipeline, f'process_{platform}_product')(full_product)

