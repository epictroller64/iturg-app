from models.scraping.ScraperConfig import ScraperConfig
from models.scraping.PreScrapedHVProduct import PreScrapedHVProduct
import requests
from factory import LoggerFactory
from models.scraping.ScrapedHVProduct import ScrapedHVProduct
from datetime import datetime
from services.parsers.hv_parser import HVParser
import asyncio

class HinnavaatlusScraper():
    session: requests.Session
    product_queue: list[PreScrapedHVProduct]
    headers: dict = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }
    config: ScraperConfig
    parser: HVParser

    def __init__(self, config: ScraperConfig):
        self.session = requests.Session()
        self.parser = HVParser()
        self.product_queue = []
        self.config = config
        self.logger = LoggerFactory.get_logger("hinnavaatlus")


    async def scrape_product_details(self, product: PreScrapedHVProduct) -> ScrapedHVProduct:
        # Get page content
        response = self.session.get(f"https://foorum.hinnavaatlus.ee/{product.link}", headers=self.headers)
        if response.status_code != 200:
            self.logger.error(f"Failed to scrape product details for {product.link} with status code {response.status_code}")
            return None
        
        soup = self.parser.get_soup(response.text)
        is_active = self.parser.is_active_listing(soup)
        if not is_active:
            return [ScrapedHVProduct(
                product_id=f"{product.id}-{product.title}",
                name=product.title,
                price=0,
                description="",
                images=[],
                categories=[],
                brand="",
                seller_url=product.link,
                product_url=product.link,
                location=product.location,
                time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                active=is_active
            )]
        first_post = self.parser.get_first_post(soup)
        if not first_post:
            self.logger.error(f"Failed to scrape product details for {product.link} with status code {response.status_code}")
            return []

        images = self.parser.get_images_from_post(first_post)

        seller_url = self.parser.parse_seller_url_from_post(soup)
        product_id = self.parser.get_product_id_from_url(product.link)
        extracted_products = await self.parser.parse_listings_from_post(first_post.text.strip())
        
        base_product = {
            'description': first_post.text.strip(),
            'images': images,
            'category': product.category,
            'brand': "Apple",
            'seller_url': seller_url,
            'product_url': product.link,
            'location': product.location,
            'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }


        if not extracted_products:
            # Return single product based on title if no products extracted
            return [ScrapedHVProduct(
                product_id=f"{product_id}-{product.title}",
                name=product.title,
                price=0,
                description=base_product['description'],
                images=base_product['images'],
                categories=base_product['category'],
                brand=base_product['brand'],
                seller_url=base_product['seller_url'],
                product_url=base_product['product_url'],
                location=base_product['location'],
                time=base_product['time'],
                active=is_active
            )]


        # Return all extracted products
        return [ScrapedHVProduct(
            product_id=f"{product_id}-{found_product.title}",
            name=found_product.title,
            price=found_product.price,
            description=base_product['description'],
            images=base_product['images'],
            categories=base_product['category'],
            brand=base_product['brand'],
            seller_url=base_product['seller_url'],
            product_url=base_product['product_url'],
            location=base_product['location'],
            time=base_product['time'],
            active=is_active
        ) for found_product in extracted_products]


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
            soup = self.parser.get_soup(response.text)
            topics = soup.find_all('span', class_='topictitle')[1:]
            if len(topics) == 0:
                self.logger.info(f"No topics found on page {page_num}")
                break
            for topic in topics:
                title = topic.find('a', class_='topictitle')
                if title is None:
                    continue
                
                transaction_type = self.parser.parse_listing_type(title.find('span', class_='gensmall').text.strip())
                if transaction_type != "M":
                    self.logger.info(f"Skipping non offer listing: {title.find('span', class_='gensmall').text.strip()}")
                    continue
                
                product_title = self.parser.parse_title_from_element(title)
                category = self.parser.parse_category_from_element(title)
                location = self.parser.parse_location_from_element(title)
                link = self.parser.parse_listing_link_from_post(title)
                id = self.parser.get_product_id_from_url(link)

                self.product_queue.append(PreScrapedHVProduct(
                    id=id,
                    title=product_title,
                    transaction_type=transaction_type,
                    category=category,
                    location=location,
                    link=link
                ))

            self.logger.info(f"Scraped page {page_num} with status code {response.status_code}")
            page_num += 1
            start_param = 25 * page_num
        return self.product_queue
