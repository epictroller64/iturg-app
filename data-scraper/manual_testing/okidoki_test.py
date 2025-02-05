from services.parsers.okidoki_parser import OkidokiParser
from manual_testing.base_tester import BaseTester

class OkidokiTest(BaseTester):
    def __init__(self):
        super().__init__()
        self.parser = OkidokiParser()

    def start(self, url: str):
        test_functions = [
            self.test_product_price,
            self.test_product_images,
            self.test_product_seller_url,
            self.test_product_location,
            self.test_product_time,
            self.test_product_category,
            self.test_product_description
        ]
        self.run_tests(url, test_functions)

    def test_product_price(self, soup):
        price = self.parser.get_product_price(soup)
        self.print_key_value("Product Price", price)
        
    def test_product_images(self, soup):
        images = self.parser.get_product_images(soup)
        rows = [(str(i+1), img) for i, img in enumerate(images)]
        self.print_table(["#", "Image URL"], rows, "🖼️ Product Images")
        self.print_key_value("Image Count", str(len(images)))

    def test_product_seller_url(self, soup):
        seller_url = self.parser.get_product_seller_url(soup)
        self.print_key_value("Seller URL", seller_url)
        
    def test_product_location(self, soup):
        location = self.parser.get_product_location(soup)
        self.print_key_value("Location", location)
        
    def test_product_time(self, soup):
        time = self.parser.get_product_time(soup)
        self.print_key_value("Time Posted", time)
        
    def test_product_category(self, soup):
        category = self.parser.get_product_category(soup)
        self.print_key_value("Category", category)
        
    def test_product_description(self, soup):
        description = self.parser.get_product_description(soup)
        self.print_key_value("Description", description)
