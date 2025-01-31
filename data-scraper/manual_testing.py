from hinnavaatlus import HinnavaatlusScraper
from models.ScraperConfig import ScraperConfig


def soov_detect_active_status():
    pass


def hv_test_scrape():
    hv_scraper = HinnavaatlusScraper(ScraperConfig(max_pages=-1))
    hv_scraper.scrape_products()
    print(len(hv_scraper.product_queue))

hv_test_scrape()
