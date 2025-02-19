from services.scraping.okidoki import OkidokiScraper
from factory import LoggerFactory
from models.database.Product import Product
from typing import List
from models.scraping.PreScrapedOkidokiProduct import PreScrapedOkidokiProduct
from product_pipeline import ProductPipeline
from models.scraping.ScraperConfig import ScraperConfig


class OkidokiUpdater:

    def __init__(self, config: ScraperConfig):
        self.logger = LoggerFactory.get_logger("OkidokiUpdater")
        self.okidoki_scraper = OkidokiScraper(config)
        self.product_pipeline = ProductPipeline(config)

    async def update_okidoki_products(self, products: List[Product]):
        for product in products:
            if product.platform == "okidoki":
                self.logger.info(f"Updating product {product.product_id}")
                updated_products = self.okidoki_scraper.scrape_product_details(PreScrapedOkidokiProduct(str(product.product_id), product.name, product.product_url))
                for updated_product in updated_products:
                    await self.product_pipeline.process_okidoki_product(updated_product)
