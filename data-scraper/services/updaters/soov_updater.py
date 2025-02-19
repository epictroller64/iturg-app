from services.scraping.soov import SoovScraper
from factory import LoggerFactory
from models.scraping.PreScrapedSoovProduct import PreScrapedSoovProduct
from models.scraping.ScraperConfig import ScraperConfig
from models.database.Product import Product
from typing import List
from product_pipeline import ProductPipeline


class SoovUpdater:
    def __init__(self, config: ScraperConfig):
        self.logger = LoggerFactory.get_logger("SoovUpdater")
        self.soov_scraper = SoovScraper(config)
        self.product_pipeline = ProductPipeline(config)

    async def update_soov_products(self, products: List[Product]):
        for product in products:
            if product.platform == "soov":
                self.logger.info(f"Updating product {product.product_id}")
                price_history = product.price_history
                price = 0
                if len(price_history) > 0:
                    price = price_history[-1].price
                updated_products = self.soov_scraper.scrape_product_details(PreScrapedSoovProduct(str(product.product_id), product.name, product.product_url, price))
                for updated_product in updated_products:
                    await self.product_pipeline.process_soov_product(updated_product)

