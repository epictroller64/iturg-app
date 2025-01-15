from okidoki import OkidokiScraper
from product_pipeline import ProductPipeline
from pricehistory_pipeline import PriceHistoryPipeline
from models.ScraperConfig import ScraperConfig
from datetime import datetime, timedelta
from factory import LoggerFactory
from repository.product import get_product
import time

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

    def scrape_apple_products(self):
       """Scrape apple products from across different platforms (marketplaces)"""
       while True:
            if self.next_scrape_time < datetime.now():
                self.logger.info("Starting apple scraper at " + str(datetime.now()))
                self.scrape_okdioki_products("apple")
                # Add more providers later
                self.on_scrape_complete()
            else:
                self.logger.info("Waiting for next scrape at " + str(self.next_scrape_time))
                time.sleep(1)

        
    def scrape_okdioki_products(self, keyword: str):
        okidoki_products = self.okidoki_scraper.scrape_by_keyword(keyword)
        for okidoki_product in okidoki_products:
            # Check if product has been recently scraped
            existing_product = get_product(okidoki_product.id, prefer_cache=True)
            if existing_product and existing_product.updated_at > datetime.now() - timedelta(hours=self.config.hours_between_updates):
                self.logger.info(f"Product {okidoki_product.id} has been recently scraped, skipping...")
                continue
            full_product = self.okidoki_scraper.scrape_product_details(okidoki_product)
            self.product_pipeline.process_okidoki_product(full_product)

    def on_scrape_complete(self):
        self.logger.info("Scrape complete at " + str(datetime.now()))
        self.next_scrape_time = datetime.now() + timedelta(seconds=self.config.time_between_scrapes)
        self.logger.info("Next scrape at " + str(self.next_scrape_time))

