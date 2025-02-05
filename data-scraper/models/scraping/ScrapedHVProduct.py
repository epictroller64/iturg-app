from pydantic import BaseModel

class ScrapedHVProduct(BaseModel):
    product_id: str
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