from typing import List
import re
from openai_communication import OpenAICommunication
from models.response.OpenAIResponse import OpenAIHVPostResponse, OpenAIHVProduct
from bs4 import BeautifulSoup, Tag

class HVParser():
    def __init__(self):
        self.openai = OpenAICommunication()

    def parse_listing_type(self, listing_type: str) -> str:
        if 'M:' in listing_type:
            return 'M'
        elif 'O:' in listing_type:
            return 'O'
        elif 'M/V:' in listing_type:
            return 'M/V'
        else:
            return 'Unknown'
        

    def parse_listing_link_from_post(self, post: Tag) -> str:
        return post.attrs['href'] if post.has_attr('href') else ""
        
    def is_active_listing(self, soup: BeautifulSoup) -> bool:
        gen_span = soup.find('span', class_='gen')
        if not gen_span:
            return True
        if "teema puudub või on kustutatud" in gen_span.text.strip():
            return False
        return True


    def parse_seller_url_from_post(self, soup: BeautifulSoup) -> str:
        seller_url = ""
        for elem in soup.find_all('td a'):
            if elem.has_attr('href') and elem['href'].startswith("profile.php?mode=viewprofile"):
                seller_url = elem['href']
                break
        return seller_url
    

    def get_soup(self, text: str):
        return BeautifulSoup(text, 'html.parser')
    
    def get_first_post(self, soup: BeautifulSoup) -> Tag:
        first_post = soup.find('span', class_='postbody')
        return first_post
    
    def get_images_from_post(self, first_post: Tag ) -> List[str]:
        images = [
            image['src'].replace('thumb', 'image') 
            for image in first_post.find_all('img')
            if not image['src'].endswith('/images/exclamation.gif')
        ]
        return images

    def get_product_id_from_url(self, url: str) -> str:
        return  url.split("t=")[1].split("&")[0] if "t=" in url else ""

    async def parse_listings_from_post(self, post: str) -> List[OpenAIHVProduct]:
        openai_response = await self.openai.ask_openai(
            [
                {"role": "system", "content": "You extract products and their prices from forum posts I feed you one by one. Use OK price wherever available."},
                {"role": "user", "content": post}
            ],
            response_format=OpenAIHVPostResponse
        )
        if openai_response:
            return openai_response.products
        else:
            return []
    

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

    def parse_title_from_element(self, title_element) -> str:
        title_text = ''
        for content in title_element.contents:
            if isinstance(content, str):
                title_text = content.strip()
                break
        return title_text if title_text else 'Unknown Title'

    def parse_category_from_element(self, title_element) -> str:
        return title_element.find('span', class_='gensmall').find_next('span', class_='gensmall').find('i').text.strip().split(' : ')

    def parse_location_from_element(self, title_element) -> str:
        return title_element.find_all('span', class_='gensmall')[-1].find('i').text.strip()

    