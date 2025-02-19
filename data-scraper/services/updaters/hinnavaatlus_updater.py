from factory import LoggerFactory
from repository.product import  delete_product, insert_product_to_archive
from services.scraping.hinnavaatlus import HinnavaatlusScraper
from models.scraping.ScraperConfig import ScraperConfig
from models.scraping.PreScrapedHVProduct import PreScrapedHVProduct
from models.scraping.ScrapedHVProduct import ScrapedHVProduct
from typing import List
from models.database.Product import Product


class HinnavaatlusUpdater:
    def __init__(self, config: ScraperConfig):
        self.logger = LoggerFactory.get_logger("HinnavaatlusUpdater")
        self.config = config
        self.hinnavaatlus_scraper = HinnavaatlusScraper(config)

    async def update_child_products_in_db(self, updated_products: List[ScrapedHVProduct]):
        if len(updated_products) == 0:
            return
        self.logger.info(f"Updating child products for base id: {updated_products[0].product_id}")
        if not updated_products[0].active:
            for product in updated_products:
                try:
                    await self.archive_product(product)
                except Exception as e:
                    self.logger.error(f"Error archiving product {product.product_id}: {e}")


    async def update_hinnavaatlus_products(self, products: List[Product]):
        self.logger.info("Updating all Hinnavaatlus products")

        hinnavaatlus_products = [product for product in products if product.platform == "hinnavaatlus"]

        processed_base_ids = set()
        for product in hinnavaatlus_products:
            base_id = product.product_id.split('-')[0]
            if base_id in processed_base_ids:
                continue
            child_products = [p for p in hinnavaatlus_products if p.product_id.split('-')[0] == base_id]

            first_child_product = child_products[0]
            updated_products = await self.hinnavaatlus_scraper.scrape_product_details(PreScrapedHVProduct(
                id=str(first_child_product.product_id), 
                title=first_child_product.name, 
                transaction_type="M",
                category=first_child_product.category,
                location=first_child_product.location,
                link=first_child_product.product_url
                ))
            await self.update_child_products_in_db(updated_products)
            processed_base_ids.add(base_id)


    async def archive_product(self, product: ScrapedHVProduct):
        self.logger.info(f"Archiving product {product.product_id}")
        await delete_product(product.product_id)
        await insert_product_to_archive(product)
