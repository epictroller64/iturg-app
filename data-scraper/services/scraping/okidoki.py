from typing import List
from curl_cffi import requests
from models.scraping.PreScrapedOkidokiProduct import PreScrapedOkidokiProduct
from models.scraping.ScrapedOkidokiProduct import ScrapedOkidokiProduct
from factory import LoggerFactory
from Error import Error
from models.scraping.ScraperConfig import ScraperConfig
import time
from services.parsers.okidoki_parser import OkidokiParser

class OkidokiScraper:
    session: requests.Session
    product_queue: list[PreScrapedOkidokiProduct]
    headers: dict = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }
    config: ScraperConfig
    parser: OkidokiParser

    def __init__(self, config: ScraperConfig):
        self.session = requests.Session()
        self.product_queue = []
        self.config = config
        self.logger = LoggerFactory.get_logger("okidoki")
        self.parser = OkidokiParser()

    def __del__(self):
        if hasattr(self, 'session'):
            self.session.close()

    def _make_request(self, url: str, context: str) -> requests.Response:
        retry_count = 0
        while retry_count < self.config.retry_count:
            try:
                response = self.session.get(url, headers=self.headers)
                if response.status_code == 200:
                    return response
                retry_count += 1
                if retry_count < self.config.retry_count:
                    self.logger.warning(f"Failed to scrape {context} with status code {response.status_code}, retrying in {self.config.retry_delay} seconds...")
                    time.sleep(self.config.retry_delay)
            except Exception as e:
                retry_count += 1
                if retry_count < self.config.retry_count:
                    self.logger.warning(f"Failed to scrape {context} with error {e}, retrying in {self.config.retry_delay} seconds...")
                    time.sleep(self.config.retry_delay)
        
        raise Error(f"Failed to scrape {context} after {self.config.retry_count} retries", self.logger)

    def scrape_product_details(self, product: PreScrapedOkidokiProduct) -> List[ScrapedOkidokiProduct]:
        url = f"https://www.okidoki.ee{product.href}"
        response = self._make_request(url, f"product {product.id}")
        was_redirected = response.url != url
        if was_redirected:
            self.logger.info(f"Product {product.id} is not active anymore")
            return [ScrapedOkidokiProduct(
                product_id=product.id,
                name=product.name,
                product_url=product.href,
                price=0,
                description="",
                images=[],
                categories=[],
                brand="",
                time="",
                seller_url="",
                location="",
                active=False
            )]
        soup = self.parser.get_soup(response.text)
        is_active = self.parser.is_active_listing(soup)
        product_name = product.name
        product_price = self.parser.get_product_price(soup)
        product_description = self.parser.get_product_description(soup)
        product_images = self.parser.get_product_images(soup)
        product_category = self.parser.get_product_category(soup)
        seller_url = self.parser.get_product_seller_url(soup)
        location = self.parser.get_product_location(soup)
        time = self.parser.get_product_time(soup)
        return [ScrapedOkidokiProduct(
                                    product_id=product.id,
                                     name=product_name,
                                     price=product_price,
                                     description=product_description,
                                     images=product_images,
                                     categories=product_category,
                                     brand="NA",
                                     seller_url=seller_url,
                                     product_url=product.href,
                                     location=location,
                                     time=time,
                                     active=is_active)
                                     ]


    def scrape_by_keyword(self, keyword: str) -> List[PreScrapedOkidokiProduct]:
        if self.config.max_pages == -1:
            self.config.max_pages = 1000000 # Set to a very high number to scrape all pages
        for i in range(1, self.config.max_pages + 1):
            self.logger.info(f"Scraping page {i} with keyword {keyword}")
            url = f"https://www.okidoki.ee/buy/all/?p={i}&query={keyword}&pp={self.config.page_size}"
            
            response = self._make_request(url, f"page {i}")
            products, has_next_page = self.parser.parse_product_list(response.text)
            self.product_queue.extend(products)
            if not has_next_page:
                break
            self.logger.info(f"Scraped {len(products)} products from page {i}")
            time.sleep(self.config.time_between_pages)
        return self.product_queue
    


