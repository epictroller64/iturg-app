from pydantic import BaseModel, field_validator, validator

# Store data after scraping it from Okidoki
class ScrapedOkidokiProduct:
    id: str #Okidoki Product ID
    name: str
    price: float
    description: str
    images: list[str]
    category: str
    brand: str
    seller_url: str
    product_url: str
    location: str
    time: str

    def __init__(self, id, name, price, description, images, category, brand, seller_url, product_url, location, time):
        self.id = id
        self.name = name
        self.price = price
        self.description = description
        self.images = images
        self.category = category
        self.brand = brand
        self.seller_url = seller_url
        self.product_url = product_url
        self.location = location
        self.time = time


class PreScrapedOkidokiProduct:
    id: str #Okidoki Product ID
    name: str
    href: str
    def __init__(self, id, name, href):
        self.id = id
        self.name = name
        self.href = href

    
