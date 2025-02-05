from services.parsers.hv_parser import HVParser
from manual_testing.base_tester import BaseTester
from bs4 import BeautifulSoup
from typing import List
import asyncio

class HvTest(BaseTester):
    def __init__(self):
        super().__init__()
        self.parser = HVParser()

    def start(self, url: str):
        test_functions = [
            self.test_product_images,
            self.test_product_listings
        ]
        self.run_tests(url, test_functions)

    def test_product_listings(self, soup: BeautifulSoup) -> List[BeautifulSoup]:
        first_post = self.parser.get_first_post(soup)
        listings = asyncio.run(self.parser.parse_listings_from_post(first_post.text))
        self.print_table(["#", "Listing"], [(str(i+1), listing) for i, listing in enumerate(listings)], "🛒 Product Listings")
        self.print_key_value("Listing Count", str(len(listings)))

    
    def test_product_images(self, soup):
        first_post = self.parser.get_first_post(soup)
        images = self.parser.get_images_from_post(first_post)
        rows = [(str(i+1), img) for i, img in enumerate(images)]
        self.print_table(["#", "Image URL"], rows, "🖼️ Product Images")
        self.print_key_value("Image Count", str(len(images)))
        