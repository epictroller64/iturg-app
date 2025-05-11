import asyncio
from manual_testing.okidoki_test import OkidokiTest
from manual_testing.soov_test import SoovTest
from manual_testing.hv_test import HvTest
from dotenv import load_dotenv
from services.scraping.okidoki import OkidokiScraper
from models.scraping.ScraperConfig import ScraperConfig
from models.scraping.PreScrapedOkidokiProduct import PreScrapedOkidokiProduct
from services.scraping.soov import SoovScraper
from models.scraping.PreScrapedHVProduct import PreScrapedHVProduct
from services.updaters.hinnavaatlus_updater import HinnavaatlusScraper
load_dotenv(override=True)

#okidoki_test = OkidokiTest()
#okidoki_test.start('https://www.okidoki.ee/item/iphone-14-pro/13160364/')

#soov_test = SoovTest()
#soov_test.start('https://soov.ee/25717198-iphone-13-pro-gold-128gb/details.html')

hv_scraper = HinnavaatlusScraper(config=ScraperConfig())
result = asyncio.run(hv_scraper.scrape_product_details(PreScrapedHVProduct(id="8042", title="", transaction_type="", category=[], location="", link="viewtopic.php?t=860702")))
print(result)