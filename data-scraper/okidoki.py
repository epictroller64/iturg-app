from curl_cffi import requests
from bs4 import BeautifulSoup
from models.OkidokiProduct import PreScrapedOkidokiProduct, ScrapedOkidokiProduct
from factory import LoggerFactory
from Error import Error
from models.ScraperConfig import ScraperConfig
import time

class OkidokiScraper:
    session: requests.Session
    product_queue: list[PreScrapedOkidokiProduct]
    headers: dict = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }
    config: ScraperConfig

    def __init__(self, config: ScraperConfig):
        self.session = requests.Session()
        self.product_queue = []
        self.config = config
        self.logger = LoggerFactory.get_logger("okidoki")
    
    def scrape_product_details(self, product: PreScrapedOkidokiProduct):
        url = f"https://www.okidoki.ee{product.href}"

        retry_count = 0
        while retry_count < self.config.retry_count:
            try:
                response = self.session.get(url, headers=self.headers)
                if response.status_code == 200:
                    break
                retry_count += 1
                if retry_count < self.config.retry_count:
                    self.logger.warning(f"Failed to scrape product {product.id} with status code {response.status_code}, retrying in {self.config.retry_delay} seconds...")
                    time.sleep(self.config.retry_delay)
            except Exception as e:
                retry_count += 1
                if retry_count < self.config.retry_count:
                    self.logger.warning(f"Failed to scrape product {product.id} with error {e}, retrying in {self.config.retry_delay} seconds...")
                    time.sleep(self.config.retry_delay)
        
        if retry_count == self.config.retry_count:
            raise Error(f"Failed to scrape product {product.id} after {self.config.retry_count} retries", self.logger)

        soup = BeautifulSoup(response.text, 'html.parser')
        product_name = product.name
        product_price = soup.find('p', class_='price').text.strip()
        product_description = str(soup.find('div', id='description'))
        product_images = [img['src'] for img in soup.find_all('img', attrs={'data-photos': 'main-list'})]
        product_category = soup.find('ul', class_='breadcrumbs').find_all('li')[1].find('span').text.strip()
        seller_url = soup.find('div', class_='user-block__popup-footer').find('a')['href']
        location = soup.find('span', attrs={'itemprop': 'address'}).text.strip()
        time = soup.find('div', class_='stats-views__item').find('span').text.strip()

        return ScrapedOkidokiProduct(product.id, product_name, product_price, product_description, product_images, product_category, "NA", seller_url, product.href, location, time)

    def scrape_by_keyword(self, keyword: str):
        if self.config.max_pages == -1:
            self.config.max_pages = 1000000 # Set to a very high number to scrape all pages
        for i in range(1, self.config.max_pages + 1):
            self.logger.info(f"Scraping page {i} with keyword {keyword}")
            url = f"https://www.okidoki.ee/buy/all/?p={i}&query={keyword}&pp={self.config.page_size}"
            
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
            products = soup.find_all('li', class_='classifieds__item')
            if len(products) == 0:
                self.logger.info(f"No products found on page {i}")
                break
            for product in products:
                try:
                    product_name = product.find('h3').text.strip()
                    product_href = product.find('a')['href']
                    product_id = product_href.split('/')[-2]
                    self.product_queue.append(PreScrapedOkidokiProduct(product_id, product_name, product_href))
                except Exception as e:
                    self.logger.error(f"Failed to scrape product {product} with error {e}", self.logger)
            self.logger.info(f"Scraped {len(products)} products from page {i}")

            ## Now lets check if next button exists or not
            next_button = soup.find('a', class_='pager__next')
            if not next_button:
                self.logger.info(f"No next button found on page {i}, stopping...")
                break
            time.sleep(self.config.time_between_pages)
        return self.product_queue
    


