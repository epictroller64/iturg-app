from okidoki import OkidokiScraper, PreScrapedOkidokiProduct
from product_pipeline import ProductPipeline
from pricehistory_pipeline import PriceHistoryPipeline
from models.ScraperConfig import ScraperConfig
from datetime import datetime, timedelta
from factory import LoggerFactory
from repository.product import get_product_by_product_id_and_platform
import time
from typing import List

class Scraper:

    okidoki_scraper: OkidokiScraper
    product_pipeline: ProductPipeline
    pricehistory_pipeline: PriceHistoryPipeline
    config: ScraperConfig
    next_scrape_time: datetime


    def __init__(self, config: ScraperConfig):
        self.okidoki_scraper = OkidokiScraper(config)
        self.product_pipeline = ProductPipeline(config)
        self.pricehistory_pipeline = PriceHistoryPipeline()
        self.config = config
        self.next_scrape_time = datetime.now()
        self.logger = LoggerFactory.get_logger("Scraper")

    async def scrape_apple_products(self):
       """Scrape apple products from across different platforms (marketplaces)"""
       while True:
            if self.next_scrape_time < datetime.now():
                self.logger.info("Starting apple scraper at " + str(datetime.now()))
                await self.scrape_okdioki_products(["apple", "iphone", "imac", "macbook", "ipad"])
                # Add more providers later
                self.on_scrape_complete()
            else:
                self.logger.info("Waiting for next scrape at " + str(self.next_scrape_time))
                time.sleep(1)

        
    async def scrape_okdioki_products(self, keywords: List[str]):
        okidoki_products: List[PreScrapedOkidokiProduct] = []
        ## Run through all keywords and scrape products
        for keyword in keywords:
            okidoki_products.extend(self.okidoki_scraper.scrape_by_keyword(keyword))

        ## Filter out duplicates
        filtered_okidoki_products: List[PreScrapedOkidokiProduct] = []
        for okidoki_product in okidoki_products:
            if okidoki_product.id not in [product.id for product in filtered_okidoki_products]:
                filtered_okidoki_products.append(okidoki_product)

        self.logger.info(f"Found {len(filtered_okidoki_products)} unique products")
        ## Process products
        for okidoki_product in filtered_okidoki_products:
            # Check if product has been recently scraped
            existing_product = await get_product_by_product_id_and_platform(okidoki_product.id, "okidoki", prefer_cache=True)
            if existing_product and existing_product.updated_at > datetime.now() - timedelta(hours=self.config.hours_between_updates):
                self.logger.info(f"Product {okidoki_product.id} has been recently scraped, skipping...")
                continue
            full_product = self.okidoki_scraper.scrape_product_details(okidoki_product)
            await self.product_pipeline.process_okidoki_product(full_product)

    def on_scrape_complete(self):
        self.logger.info("Scrape complete at " + str(datetime.now()))
        self.next_scrape_time = datetime.now() + timedelta(seconds=self.config.time_between_scrapes)
        self.logger.info("Next scrape at " + str(self.next_scrape_time))

