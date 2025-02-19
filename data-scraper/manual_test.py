from manual_testing.okidoki_test import OkidokiTest
from manual_testing.soov_test import SoovTest
from manual_testing.hv_test import HvTest
from dotenv import load_dotenv
from services.scraping.okidoki import OkidokiScraper
from models.scraping.ScraperConfig import ScraperConfig
from models.scraping.PreScrapedOkidokiProduct import PreScrapedOkidokiProduct
load_dotenv(override=True)
#okidoki_test = OkidokiTest()
#okidoki_test.start('https://www.okidoki.ee/item/iphone-14-pro/13160364/')

#soov_test = SoovTest()
#soov_test.start('https://soov.ee/25717198-iphone-13-pro-gold-128gb/details.html')

okidoki_scraper = OkidokiScraper(ScraperConfig(max_pages=-1))
products = okidoki_scraper.scrape_product_details(PreScrapedOkidokiProduct("13133133", "iPhone 14 Pro", "/item/aplle-iphone-16-pro-karl-lagerfeld-black/13133133/"))
print(products)
