from typing import List
from models.ScraperConfig import ScraperConfig
from bs4 import Tag
from models.PreScrapedSoovProduct import PreScrapedSoovProduct
from models.SoovProduct import SoovProduct
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


    def __init__(self, config: ScraperConfig):
        self.session = requests.Session()
        self.product_queue = []
        self.config = config
        self.logger = LoggerFactory.get_logger("soov")
    

    def update_product_details(self, product: SoovProduct):
        # fetch product page and detect whether listing is still active
        url = product.product_url
        response = self.session.get(url, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        headings = soup.find('h1')
        for heading in headings:
            if "Kuulutust ei leitud..." in heading.text.strip() or "Kuulutus eemaldatud" in heading.text.strip():
                product.active = False
        return product


    def scrape_product_details(self, product: PreScrapedSoovProduct) -> SoovProduct:

        url = product.href
        response = self.session.get(url, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        active = True
        # check if product is still active
        headings = soup.find('h1')
        for heading in headings:
            if "Kuulutust ei leitud..." in heading.text.strip() or "Kuulutus eemaldatud" in heading.text.strip():
                active = False
                break

        description = str(soup.find('p', attrs={'itemprop': 'description'}))

        key_feature_container = soup.find('div', class_='key-features row')
        key_features = key_feature_container.find_all('div', class_='media')
        if key_features and len(key_features) > 0:

            city_element = key_features[1].find('span', class_='media-heading')
            city = city_element.get_text(strip=True) if city_element else None

        # Get categories from breadcrumb
        categories = []
        breadcrumb = soup.find('ol', class_='breadcrumb')
        if breadcrumb:
            for li in breadcrumb.find_all('li'):
                span = li.find('span', itemprop='title')
                if span:
                    category_text = span.text.strip()
                    if 'SOOV' not in category_text and 'Kõik kuulutused' not in category_text:
                        categories.append(category_text)

        # Get product images
        image_container = soup.find('div', id='insideLightgallery2')
        images = []
        if image_container:
            for a in image_container.find_all('a'):
                if 'href' in a.attrs:
                    img_url = a['href']
                    images.append(img_url)


        user_ads_container = soup.find('div', class_='user-ads-action')
        seller_url = ""
        if user_ads_container:
            for a in user_ads_container.find_all('a'):
                if 'href' in a.attrs:
                    seller_url = a['href']
                    break

        time = soup.find('span', class_='date').text.strip()

        return SoovProduct(
            product_id=product.id,
            name=product.name,
            price=product.price,
            description=description,
            category=categories,
            images=images,
            brand="NA",
            seller_url=seller_url,
            product_url=product.href,
            location=city if city else '',
            time=time,
            active=active
        )



    def scrape_by_keyword(self, keyword: str) -> List[PreScrapedSoovProduct]:
        if self.config.max_pages == -1:
            self.config.max_pages = 1000000
        encoded_keyword = requests.utils.quote(keyword)
        
        for i in range(1, self.config.max_pages + 1):
            self.logger.info(f"Scraping page {i} with keyword {keyword}")
            url = f"https://soov.ee/keyword-{encoded_keyword}/tuup-müüa/{i}/listings.html"
            response = None
            
            # Retry logic
            for retry in range(self.config.retry_count + 1):
                try:
                    response = self.session.get(url, headers=self.headers)
                    if response.status_code == 200:
                        break
                    if retry < self.config.retry_count:
                        self.logger.warning(f"Failed to scrape page {i} (Status {response.status_code}), retrying...")
                        time.sleep(self.config.retry_delay)
                except Exception as e:
                    if retry < self.config.retry_count:
                        self.logger.warning(f"Error scraping page {i}: {str(e)}, retrying...")
                        time.sleep(self.config.retry_delay)
            
            if not response or response.status_code != 200:
                self.logger.error(f"Failed to scrape page {i} after {self.config.retry_count} retries")
                break
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Check for end of results
            end_element = soup.find('div', class_='item-list not-enough-items')
            if end_element:
                self.logger.info(f"No more results found on page {i}")
                break
            
            products = soup.find_all('div', class_='category-view')
            if not products:
                self.logger.info(f"No products found on page {i}")
                break
            
            successful_scrapes = 0
            for product in products:
                try:
                    title_element = product.find('h5', class_='add-title')
                    price_element = product.find('h2', class_='item-price')
                    price_text = price_element.text.strip() if price_element else None
                    price = float(price_text.replace('€', '')) if price_text else 0.0
                    link_element = title_element.find('a') if title_element else None
                    
                    if link_element:
                        product_name = link_element.text.strip()
                        product_href = link_element['href']
                        product_id = product_href.split('-')[0].split('/')[-1]
                        self.product_queue.append(PreScrapedSoovProduct(product_id, product_name, product_href, price))
                        successful_scrapes += 1
                except Exception as e:
                    self.logger.error(f"Failed to scrape product: {str(e)}")
                    continue
                
            self.logger.info(f"Successfully scraped {successful_scrapes}/{len(products)} products from page {i}")
            
            if i < self.config.max_pages:
                time.sleep(self.config.time_between_pages)

        return self.product_queue
