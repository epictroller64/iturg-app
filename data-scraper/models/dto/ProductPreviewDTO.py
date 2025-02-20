from pydantic import BaseModel


class ProductPreviewDTO(BaseModel):
    id: int
    platform_product_id: str
    name: str
    price: float
    imageUrl: str
    platform: str
    device: str
    chip: str
    ram: str
    screen_size: str
    generation: str
    storage: str
    color: str
    status: str
    year: str
    watch_mm: str
    days_since_added: int


