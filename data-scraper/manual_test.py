from manual_testing.okidoki_test import OkidokiTest
from manual_testing.soov_test import SoovTest
from manual_testing.hv_test import HvTest
from dotenv import load_dotenv
from services.scraping.okidoki import OkidokiScraper
from models.scraping.ScraperConfig import ScraperConfig
from models.scraping.PreScrapedOkidokiProduct import PreScrapedOkidokiProduct
from services.scraping.soov import SoovScraper
from models.scraping.PreScrapedSoovProduct import PreScrapedSoovProduct
load_dotenv(override=True)
#okidoki_test = OkidokiTest()
#okidoki_test.start('https://www.okidoki.ee/item/iphone-14-pro/13160364/')

#soov_test = SoovTest()
#soov_test.start('https://soov.ee/25717198-iphone-13-pro-gold-128gb/details.html')

soov_scraper = SoovScraper(ScraperConfig(max_pages=-1))
products = soov_scraper.scrape_product_details(PreScrapedSoovProduct("25712082", "iPhone 15 Pro Max", "https://soov.ee/25712082-apple-iphone-15-pro-max-512gb-garantii/details.html", 0))
print(products)
