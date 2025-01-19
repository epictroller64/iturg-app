from pydantic import BaseModel
from datetime import datetime

class Product(BaseModel):
    id: int # Primary key in the database
    product_id: str # Unique identifier for the product based on the platform its found from
    platform: str #okidoki, soov, etc
    name: str
    description: str
    category: list[str]
    brand: str
    seller_url: str
    product_url: str
    location: str
    created_at: datetime | None = None
    updated_at: datetime | None = None
    images: list[str] # JSON array of image urls

    model_config = {
        "from_attributes": True  # This replaces the old orm_mode=True
    }
