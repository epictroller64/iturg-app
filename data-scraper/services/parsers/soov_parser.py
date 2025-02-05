from factory import LoggerFactory
from bs4 import BeautifulSoup
from typing import List, Optional

class SoovParser:
    def __init__(self):
        self.logger = LoggerFactory.get_logger("soov")

    def get_soup(self, html_content: str) -> BeautifulSoup:
        return BeautifulSoup(html_content, 'html.parser')
    
    def get_product_active_status(self, soup: BeautifulSoup) -> bool:
        try:
            headings = soup.find('h1')
            for heading in headings:
                if any(text in heading.text.strip() for text in ["Kuulutust ei leitud...", "Kuulutus eemaldatud"]):
                    return False
            return True
        except Exception:
            return False
    
    def get_product_location(self, soup: BeautifulSoup) -> Optional[str]:
        try:
            key_feature_container = soup.find('div', class_='key-features row')
            key_features = key_feature_container.find_all('div', class_='media')
            if key_features and len(key_features) > 1:
                city_element = key_features[1].find('span', class_='media-heading')
                return city_element.get_text(strip=True) if city_element else None
            return None
        except Exception:
            return None

    def get_product_description(self, soup: BeautifulSoup) -> Optional[str]:
        try:
            desc = soup.find('p', attrs={'itemprop': 'description'})
            return str(desc) if desc else None
        except Exception:
            return None
    
    def get_product_category(self, soup: BeautifulSoup) -> List[str]:
        categories = []
        try:
            breadcrumb = soup.find('ol', class_='breadcrumb')
            if breadcrumb:
                excluded = {'SOOV', 'Kõik kuulutused'}
                categories = [span.text.strip() for li in breadcrumb.find_all('li')
                            if (span := li.find('span', itemprop='title'))
                            and span.text.strip() not in excluded]
        except Exception:
            self.logger.error("Error parsing categories")
        return categories
    
    def get_product_images(self, soup: BeautifulSoup) -> List[str]:
        try:
            image_container = soup.find('div', id='insideLightgallery2')
            return [a['href'] for a in image_container.find_all('a') if 'href' in a.attrs] if image_container else []
        except Exception:
            return []

    def get_product_seller_url(self, soup: BeautifulSoup) -> str:
        try:
            user_ads_container = soup.find('div', class_='user-ads-action')
            if user_ads_container:
                seller_link = user_ads_container.find('a')
                return seller_link['href'] if seller_link and 'href' in seller_link.attrs else ""
            return ""
        except Exception:
            return ""
    
    def get_product_time(self, soup: BeautifulSoup) -> str:
        try:
            date_span = soup.find('span', class_='date')
            return date_span.text.strip() if date_span else ""
        except Exception:
            return ""

    def get_is_end_of_results(self, soup: BeautifulSoup) -> bool:
        return bool(soup.find('div', class_='item-list not-enough-items'))

    def get_products(self, soup: BeautifulSoup) -> List[BeautifulSoup]:
        return soup.find_all('div', class_='category-view')

    def get_product_price(self, soup: BeautifulSoup) -> float:
        """Get the price from search page not product page"""
        try:
            price_element = soup.find('h2', class_='item-price')
            if not price_element:
                return 0
            price_text = price_element.text.strip()
            price_text = price_text.replace('€', '').replace(',', '.').strip()
            return float(price_text) if price_text else 0
        except (ValueError, AttributeError):
            return 0

    def get_product_name(self, soup: BeautifulSoup) -> str:
        try:
            title_element = soup.find('h5', class_='add-title')
            link_element = title_element.find('a') if title_element else None
            return link_element.text.strip() if link_element else ""
        except Exception:
            return ""

    def get_product_link(self, soup: BeautifulSoup) -> str:
        try:
            title_element = soup.find('h5', class_='add-title')
            link_element = title_element.find('a') if title_element else None
            return link_element['href'] if link_element and 'href' in link_element.attrs else ""
        except Exception:
            return "" 
