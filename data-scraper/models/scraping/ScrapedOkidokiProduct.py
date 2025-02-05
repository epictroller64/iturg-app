from pydantic import BaseModel

# Store data after scraping it from Okidoki
class ScrapedOkidokiProduct(BaseModel):
    product_id: str #Okidoki Product ID
    name: str
    price: float
    description: str
    images: list[str]
    categories: list[str]
    brand: str
    seller_url: str
    product_url: str
    location: str
    time: str




    
