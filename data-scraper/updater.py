from models.scraping.ScraperConfig import ScraperConfig
from repository.product import get_all_products
from product_pipeline import ProductPipeline
from factory import LoggerFactory
from backup_manager import BackupManager
from models.database.Product import Product
from services.scraping.soov import SoovScraper
from services.scraping.okidoki import OkidokiScraper
from services.scraping.hinnavaatlus import HinnavaatlusScraper
class Updater:
    config: ScraperConfig
    logger: LoggerFactory
    product_pipeline: ProductPipeline
    soov_scraper: SoovScraper
    okidoki_scraper: OkidokiScraper
    backup_manager: BackupManager


    def __init__(self, config: ScraperConfig):
        self.config = config
        self.logger = LoggerFactory.get_logger("Updater")
        self.product_pipeline = ProductPipeline(config)
        self.soov_scraper = SoovScraper(config)
        self.okidoki_scraper = OkidokiScraper(config)
        self.backup_manager = BackupManager()

    async def update_product_details(self, product: Product):
        if product.platform == "soov":
            updated_product = self.soov_scraper.update_product_details(product)
        elif product.platform == "okidoki":
            updated_product = self.okidoki_scraper.update_product_details(product)

        return updated_product

    async def update_all_product_details(self):
        self.backup_manager.create_backup()
        products = await get_all_products()
        for product in products:
            self.logger.info(f"Updating product {product.product_id} with platform {product.platform}")
            await self.update_product_details(product)

