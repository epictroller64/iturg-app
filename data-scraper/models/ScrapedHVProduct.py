from pydantic import BaseModel

class ScrapedHVProduct(BaseModel):
    id: str
    name: str
    price: float
    description: str
    images: list[str]
    category: list[str]
    brand: str
    seller_url: str
    product_url: str
    location: str
    time: str