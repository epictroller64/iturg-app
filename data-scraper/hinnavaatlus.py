from models.ScraperConfig import ScraperConfig
from models.PreScrapedHVProduct import PreScrapedHVProduct
import requests
from factory import LoggerFactory
from bs4 import BeautifulSoup
from typing import List
from models.ScrapedHVProduct import ScrapedHVProduct
from datetime import datetime
import re
from parser import Parser

class HinnavaatlusScraper():
    session: requests.Session
    product_queue: list[PreScrapedHVProduct]
    headers: dict = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }
    config: ScraperConfig
    parser: Parser

    def __init__(self, config: ScraperConfig):
        self.session = requests.Session()
        self.parser = Parser()
        self.product_queue = []
        self.config = config
        self.logger = LoggerFactory.get_logger("hinnavaatlus")

    def parse_listing_type(self, listing_type: str) -> str:
        if 'M:' in listing_type:
            return 'M'
        elif 'O:' in listing_type:
            return 'O'
        else:
            return 'Unknown'
        
    def parse_listing_category(self, listing_category: str) -> List[str]:
        return listing_category.split(' : ')
    
    def parse_product_price(self, product_page: str) -> float:
        """Opted to use Openai instead"""
        text = product_page.lower().replace(' ', '')
        patterns = [
            r'ah:(\d+[.,]?\d*)',  # Matches AH: 100 or AH:100.50
            r'ok:(\d+[.,]?\d*)',  # Matches OK: 100 or OK:100.50
            r'(?:^|\s)(\d+[.,]?\d*)(?:eur|e|€)', # Matches 100EUR, 100e, 100€
            r'hind:(\d+[.,]?\d*)',  # Matches Hind: 100
            r'(?:^|\s)(\d+[.,]?\d*)(?:-|$)'  # Matches standalone numbers
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            if matches:
                try:
                    price_str = matches[0].replace(',', '.')
                    return float(price_str)
                except ValueError:
                    continue
        
        return 0.0

    async def scrape_product_details(self, product: PreScrapedHVProduct) -> ScrapedHVProduct:

        # get images from first post
        response = self.session.get(product.link, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        first_post = soup.find('span', class_='postbody')
        images = first_post.find_all('img')
        images = [image['src'].replace('thumb', 'image') for image in images]

        # gotta scrape product price from page description
        openai_response = await self.parser.parse_hv_post(product.link)
        new_products = []
        seller_url = ""
        seller_url_elements = soup.find_all('td a')

        # Extract product ID from URL t parameter
        product_id = ""
        if "t=" in product.link:
            product_id = product.link.split("t=")[1].split("&")[0]
        for elem in seller_url_elements:
            if elem.has_attr('href'):
                if elem['href'].startswith("profile.php?mode=viewprofile"):
                    seller_url = elem['href']
                    break

        # create new products based on same post
        for found_product in openai_response.products:
            # create new product
            new_product = ScrapedHVProduct(
                id=f"{product_id}-{found_product.title}",
                name=found_product.title,
                price=found_product.price,
                description=first_post.text.strip(),
                images=images,
                category=product.category,
                brand="Apple",
                seller_url=seller_url,
                product_url=product.link,
                location=product.location,
                time=datetime.now()
            )
            new_products.append(new_product)

        return new_products

    def scrape_products(self):
        page_num = 0
        start_param = 25 * page_num
        if self.config.max_pages == -1:
            self.config.max_pages = 1000000 # Set to a very high number to scrape all pages
        for page_num in range(0, self.config.max_pages):
            self.logger.info(f"Scraping page {page_num}")
            url = f"https://foorum.hinnavaatlus.ee/viewforum.php?f=91&start={start_param}"
            response = self.session.get(url, headers=self.headers)
            if response.status_code != 200:
                self.logger.error(f"Failed to scrape page {page_num} with status code {response.status_code}")
                continue
            soup = BeautifulSoup(response.text, 'html.parser')
            topics = soup.find_all('span', class_='topictitle')[1:]
            if len(topics) == 0:
                self.logger.info(f"No topics found on page {page_num}")
                break
            for topic in topics:
                title = topic.find('a', class_='topictitle')
                if title is None:
                    continue
                
                transaction_type = self.parse_listing_type(title.find('span', class_='gensmall').text.strip())
                if transaction_type != "M":
                    self.logger.info(f"Skipping non offer listing: {title.find('span', class_='gensmall').text.strip()}")
                    continue
                
                title_text = ''
                for content in title.contents:
                    if isinstance(content, str):
                        title_text = content.strip()
                        break
                
                product_title = title_text if title_text else 'Unknown Title'
                
                category = title.find('span', class_='gensmall').find_next('span', class_='gensmall').find('i').text.strip()
                
                location = title.find_all('span', class_='gensmall')[-1].find('i').text.strip()

                self.product_queue.append(PreScrapedHVProduct(
                    title=product_title,
                    transaction_type=transaction_type,
                    category=category,
                    location=location
                ))

            self.logger.info(f"Scraped page {page_num} with status code {response.status_code}")
            page_num += 1
            start_param = 25 * page_num
