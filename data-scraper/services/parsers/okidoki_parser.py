from bs4 import BeautifulSoup
from typing import List, Tuple
import json
import re
from models.scraping.PreScrapedOkidokiProduct import PreScrapedOkidokiProduct
from models.scraping.ScrapedOkidokiProduct import ScrapedOkidokiProduct
from factory import LoggerFactory
from logger import Logger

class OkidokiParser:
    """
    Parser for Okidoki.ee
    """
    logger: Logger

    def __init__(self):
        self.logger = LoggerFactory.get_logger("okidoki")

    def get_soup(self, html_content: str) -> BeautifulSoup:
        return BeautifulSoup(html_content, 'html.parser')
    
    def is_active_listing(self, soup: BeautifulSoup) -> bool:
        status_elem = soup.find("p", class_="item-status")
        if not status_elem:
            return False  # If we can't find the status element, assume listing is not active
        return "Kuulutus ei ole aktiivne" not in status_elem.text.strip()
    
    def get_product_price(self, soup: BeautifulSoup) -> float:
        price_elem = soup.find('p', class_='price')
        if not price_elem:
            return 0.0
        price_text = price_elem.text.strip()
        price_text = price_text.replace('€', '').replace(' ', '').replace(',', '.')
        try:
            return float(price_text)
        except ValueError:
            return 0.0
    
    def get_product_images(self, soup: BeautifulSoup) -> List[str]:
        script_tag = soup.find('script', string=lambda text: text and 'photosList' in text)
        if not script_tag:
            return []
        
        match = re.search(r'var photosList = (\[.*?\]),', script_tag.string)
        if not match:
            return []
            
        try:
            photos_list = json.loads(match.group(1))
            return [photo['photoFullsize']['src'] for photo in photos_list]
        except (json.JSONDecodeError, KeyError):
            return []
    
    def get_product_seller_url(self, soup: BeautifulSoup) -> str:
        seller_elem = soup.find('div', class_='user-block__popup-footer')
        if not seller_elem:
            return ""
        link = seller_elem.find('a')
        return link.get('href', "") if link else ""

    def get_product_location(self, soup: BeautifulSoup) -> str:
        location_elem = soup.find('span', attrs={'itemprop': 'address'})
        return location_elem.text.strip() if location_elem else ""
    
    def get_product_time(self, soup: BeautifulSoup) -> str:
        stats_views = soup.find('div', class_='stats-views')
        if not stats_views:
            return ""
        time_container = stats_views.find_all('div', class_='stats-views__item')[1]
        if not time_container:
            return ""
        time_elem = time_container.find('span')
        return time_elem.text.strip() if time_elem else ""
    
    def get_product_category(self, soup: BeautifulSoup) -> List[str]:
        breadcrumbs = soup.find('ul', class_='breadcrumbs')
        if not breadcrumbs:
            return []
        return [
            span.text.strip()
            for li in breadcrumbs.find_all('li', attrs={'itemprop': 'itemListElement'})
            if (span := li.find('span', itemprop='name'))
        ]
    
    def get_product_description(self, soup: BeautifulSoup) -> str:
        desc_elem = soup.find('div', id='description')
        return str(desc_elem) if desc_elem else ""

    def parse_product_list(self, html_content: str) -> Tuple[List[PreScrapedOkidokiProduct], bool]:
        """Parse product list page and return list of pre-scraped products and has_next_page flag"""
        soup = self.get_soup(html_content)
        products = []
        
        for item in soup.find_all('li', class_='classifieds__item'):
            try:
                name_elem = item.find('h3')
                link = item.find('a')
                if not (name_elem and link):
                    continue
                    
                href = link.get('href', '')
                product_id = href.split('/')[-2]
                products.append(PreScrapedOkidokiProduct(
                    product_id,
                    name_elem.text.strip(),
                    href
                ))
            except Exception as e:
                self.logger.error(f"Error parsing product list item: {str(e)}")
                continue

        return products, bool(soup.find('a', class_='pager__next'))

    def parse_product_details(self, html_content: str, product: PreScrapedOkidokiProduct) -> ScrapedOkidokiProduct:
        """Parse product detail page and return scraped product"""
        soup = self.get_soup(html_content)
        
        return ScrapedOkidokiProduct(
            product_id=product.id,
            name=product.name,
            price=self.get_product_price(soup),
            description=self.get_product_description(soup),
            images=self.get_product_images(soup),
            categories=self.get_product_category(soup),
            brand="NA",
            seller_url=self.get_product_seller_url(soup),
            product_url=product.href,
            location=self.get_product_location(soup),
            time=self.get_product_time(soup)
        )