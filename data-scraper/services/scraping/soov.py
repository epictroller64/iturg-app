from typing import List, Optional
from models.scraping.ScraperConfig import ScraperConfig
from models.scraping.PreScrapedSoovProduct import PreScrapedSoovProduct
from models.scraping.ScrapedSoovProduct import ScrapedSoovProduct
import requests
from factory import LoggerFactory
import time
from services.parsers.soov_parser import SoovParser

class SoovScraper:
    BASE_URL = "https://soov.ee/keyword-{}/tuup-müüa/{}/listings.html"
    DEFAULT_MAX_PAGES = 1000000

    def __init__(self, config: ScraperConfig):
        self.session = requests.Session()
        self.product_queue: List[PreScrapedSoovProduct] = []
        self.config = config
        self.logger = LoggerFactory.get_logger("soov")
        self.parser = SoovParser()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
        }

    def _make_request(self, url: str) -> Optional[requests.Response]:
        for retry in range(self.config.retry_count + 1):
            try:
                response = self.session.get(url, headers=self.headers)
                if response.status_code == 200:
                    return response
                if retry < self.config.retry_count:
                    self.logger.warning(f"Failed request (Status {response.status_code}), retrying...")
                    time.sleep(self.config.retry_delay)
            except Exception as e:
                if retry < self.config.retry_count:
                    self.logger.warning(f"Request error: {str(e)}, retrying...")
                    time.sleep(self.config.retry_delay)
        return None

    def update_product_details(self, product: ScrapedSoovProduct) -> ScrapedSoovProduct:
        response = self._make_request(product.product_url)
        if response:
            soup = self.parser.get_soup(response.text)
            product.active = self.parser.get_product_active_status(soup)
        return product

    def scrape_product_details(self, product: PreScrapedSoovProduct) -> List[ScrapedSoovProduct]:
        response = self._make_request(product.href)
        if not response:
            raise Exception(f"Failed to fetch product details for {product.id}")
        
        soup = self.parser.get_soup(response.text)
        return [ScrapedSoovProduct(
            product_id=product.id,
            name=product.name,
            price=product.price,
            description=self.parser.get_product_description(soup),
            categories=self.parser.get_product_category(soup),
            images=self.parser.get_product_images(soup),
            brand="NA",
            seller_url=self.parser.get_product_seller_url(soup),
            product_url=product.href,
            location=self.parser.get_product_location(soup) or '',
            time=self.parser.get_product_time(soup),
            active=self.parser.get_product_active_status(soup)
        )]

    def scrape_by_keyword(self, keyword: str) -> List[PreScrapedSoovProduct]:
        max_pages = self.DEFAULT_MAX_PAGES if self.config.max_pages == -1 else self.config.max_pages
        encoded_keyword = requests.utils.quote(keyword)
        
        for page in range(1, max_pages + 1):
            self.logger.info(f"Scraping page {page} with keyword {keyword}")
            url = self.BASE_URL.format(encoded_keyword, page)
            
            response = self._make_request(url)
            if not response:
                self.logger.error(f"Failed to scrape page {page}")
                break
                
            soup = self.parser.get_soup(response.text)
            if self.parser.get_is_end_of_results(soup):
                self.logger.info(f"No more results found on page {page}")
                break
                
            products = self.parser.get_products(soup)
            if not products:
                self.logger.info(f"No products found on page {page}")
                break
                
            new_products = []
            for product in products:
                try:
                    price = self.parser.get_product_price(product)
                    link = self.parser.get_product_link(product)
                    if link:
                        product_name = self.parser.get_product_name(product)
                        product_id = link.split('-')[0].split('/')[-1]
                        new_products.append(PreScrapedSoovProduct(product_id, product_name, link, price))
                except Exception as e:
                    self.logger.error(f"Failed to scrape product: {str(e)}")
                    
            self.product_queue.extend(new_products)
            self.logger.info(f"Successfully scraped {len(new_products)}/{len(products)} products from page {page}")
            
            if page < max_pages:
                time.sleep(self.config.time_between_pages)

        return self.product_queue
