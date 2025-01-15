from models.OkidokiProduct import ScrapedOkidokiProduct
from models.PriceHistory import PriceHistory
from datetime import datetime, timedelta
from factory import LoggerFactory
from models.Product import Product
from repository.product import get_product, insert_product
from pricehistory_pipeline import PriceHistoryPipeline
from models.ScraperConfig import ScraperConfig

class ProductPipeline:

    def __init__(self, config: ScraperConfig):
        self.logger = LoggerFactory.get_logger("ProductPipeline")
        self.pricehistory_pipeline = PriceHistoryPipeline()
        self.config = config

    def process_okidoki_product(self, okidoki_product: ScrapedOkidokiProduct):
        """Process an Okidoki product and insert it into the database, or insert price history if it already exists"""
        existing_product = get_product(okidoki_product.id, prefer_cache=False)
        if not existing_product:
            full_product = Product(okidoki_product.id, "okidoki", okidoki_product.name, okidoki_product.description, okidoki_product.category, okidoki_product.brand, okidoki_product.seller_url, okidoki_product.product_url, okidoki_product.location, datetime.now(), datetime.now(), okidoki_product.images)
            insert_product(full_product)
            self.pricehistory_pipeline.process_price_history(PriceHistory(okidoki_product.id, "okidoki", okidoki_product.price, datetime.now()))
            self.logger.info(f"Inserted product {okidoki_product.id} with price {okidoki_product.price}")
        # Check last update time to make any insertions
        else:
            if existing_product.updated_at < datetime.now() - timedelta(hours=self.config.hours_between_updates):
                self.pricehistory_pipeline.process_price_history(PriceHistory(okidoki_product.id, "okidoki", okidoki_product.price, datetime.now()))
        self.logger.info(f"Processed product {okidoki_product.id} with price {okidoki_product.price}")
        
