from pydantic import BaseModel

class ScrapedSoovProduct(BaseModel):
    product_id: str
    name: str
    price: float
    description: str
    categories: list[str]
    images: list[str]
    brand: str
    seller_url: str
    product_url: str
    location: str
    time: str
    active: bool = True
