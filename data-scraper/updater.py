from models.scraping.ScraperConfig import ScraperConfig
from repository.product import get_all_products
from product_pipeline import ProductPipeline
from factory import LoggerFactory
from backup_manager import BackupManager
from services.scraping.soov import SoovScraper
from services.scraping.okidoki import OkidokiScraper
from services.scraping.hinnavaatlus import HinnavaatlusScraper
from services.updaters.okidoki_updater import OkidokiUpdater
from services.updaters.hinnavaatlus_updater import HinnavaatlusUpdater
from services.updaters.soov_updater import SoovUpdater


class Updater:
    config: ScraperConfig
    logger: LoggerFactory
    product_pipeline: ProductPipeline
    soov_scraper: SoovScraper
    okidoki_scraper: OkidokiScraper
    hinnavaatlus_scraper: HinnavaatlusScraper
    backup_manager: BackupManager


    def __init__(self, config: ScraperConfig):
        self.config = config
        self.logger = LoggerFactory.get_logger("Updater")
        self.product_pipeline = ProductPipeline(config)
        self.soov_scraper = SoovScraper(config)
        self.okidoki_scraper = OkidokiScraper(config)
        self.hinnavaatlus_scraper = HinnavaatlusScraper(config)
        self.backup_manager = BackupManager()


    async def update_all_products(self):
        soov_updater = SoovUpdater(self.config)
        okidoki_updater = OkidokiUpdater(self.config)
        hinnavaatlus_updater = HinnavaatlusUpdater(self.config)
        all_products = await get_all_products()
        await okidoki_updater.update_okidoki_products(all_products)
        await soov_updater.update_soov_products(all_products)
        await hinnavaatlus_updater.update_hinnavaatlus_products(all_products)

