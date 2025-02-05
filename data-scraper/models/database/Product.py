from pydantic import BaseModel
from datetime import datetime
from models.database.PriceHistory import PriceHistory

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
    price_history: list[PriceHistory]
    device: str | None = None
    chip: str | None = None
    ram: str | None = None
    screen_size: str | None = None
    generation: str | None = None
    storage: str | None = None
    color: str | None = None
    status: str | None = None
    year: str | None = None
    watch_mm: str | None = None

    model_config = {
        "from_attributes": True  # This replaces the old orm_mode=True
    }
