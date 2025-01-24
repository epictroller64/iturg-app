from models.ScraperConfig import ScraperConfig
from models.PreScrapedSoovProduct import PreScrapedSoovProduct
import requests
from factory import LoggerFactory
import time
from bs4 import BeautifulSoup
from Error import Error

class SoovScraper:

    session: requests.Session
    product_queue: list[PreScrapedSoovProduct]
    headers: dict = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }
    config: ScraperConfig
    def scrape_by_keyword(self, keyword: str):
        if self.config.max_pages == -1:
            self.config.max_pages = 1000000 # Set to a very high number to scrape all pages
        for i in range(1, self.config.max_pages + 1):
            self.logger.info(f"Scraping page {i} with keyword {keyword}")
            url = f"https://soov.ee/keyword-{keyword}/tuup-müüa/{i}/listings.html"
            retry_count = 0
            while retry_count < self.config.retry_count:
                try:
                    response = self.session.get(url, headers=self.headers)
                    if response.status_code == 200:
                        break
                    retry_count += 1
                    if retry_count < self.config.retry_count:
                        self.logger.warning(f"Failed to scrape page {i} with status code {response.status_code}, retrying in {self.config.retry_delay} seconds...")
                        time.sleep(self.config.retry_delay)
                except Exception as e:
                    retry_count += 1
                    if retry_count < self.config.retry_count:
                        self.logger.warning(f"Failed to scrape page {i} with error {e}, retrying in {self.config.retry_delay} seconds...")
                        time.sleep(self.config.retry_delay)
            
            if retry_count == self.config.retry_count:
                raise Error(f"Failed to scrape page {i} after {self.config.retry_count} retries", self.logger)
            soup = BeautifulSoup(response.text, 'html.parser')
            products = soup.find_all('div', class_='category-view')
            if len(products) == 0:
                self.logger.info(f"No products found on page {i}")
                break
            for product in products:
                try:
                    product_name = product.find('h5', class_='add-title').find('a').text.strip()
                    product_href = product.find('h5', class_='add-title').find('a')['href']
                    product_id = product_href.split('/')[1].split('-')[0]
                    self.product_queue.append(PreScrapedSoovProduct(product_id, product_name, product_href))
                except Exception as e:
                    self.logger.error(f"Failed to scrape product {product} with error {e}", self.logger)
            self.logger.info(f"Scraped {len(products)} products from page {i}")



    def __init__(self, config: ScraperConfig):
        self.session = requests.Session()
        self.product_queue = []
        self.config = config
        self.logger = LoggerFactory.get_logger("soov")