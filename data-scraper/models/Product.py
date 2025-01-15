from pydantic import BaseModel
from datetime import datetime

class Product(BaseModel):
    id: str
    platform: str #okidoki, soov, etc
    name: str
    description: str
    category: str
    brand: str
    seller_url: str
    product_url: str
    location: str
    created_at: datetime | None = None
    updated_at: datetime | None = None
    images: str # JSON array of image urls

    def __init__(self, id, platform, name, description, category, brand, seller_url, product_url, location, created_at, updated_at, images):
        self.id = id
        self.platform = platform
        self.name = name
        self.description = description
        self.category = category
        self.brand = brand
        self.seller_url = seller_url
        self.product_url = product_url
        self.location = location
        self.created_at = created_at
        self.updated_at = updated_at
        self.images = images