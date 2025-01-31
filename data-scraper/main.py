from scraper import Scraper
from models.ScraperConfig import ScraperConfig
from parser import Parser
from dotenv import load_dotenv
import asyncio
from group_pipeline import Classifier
from data_fix import recreate_level1_groups
from database import setup_database
from updater import Updater
load_dotenv(override=True)
import os


scraper = Scraper(ScraperConfig(max_pages=-1))
updater = Updater(ScraperConfig(max_pages=-1))
async def start():
    await setup_database()
    await scraper.scrape_apple_products()
    await updater.update_all_product_details()

asyncio.run(start())
#classifier = Classifier()
#asyncio.run(classifier.test())

#parser = Parser('')
#parser.test_parse()

#asyncio.run(recreate_level1_groups())