from scraper import Scraper
from models.ScraperConfig import ScraperConfig

scraper = Scraper(ScraperConfig(max_pages=-1))
scraper.scrape_apple_products()
