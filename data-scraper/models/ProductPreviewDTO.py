from pydantic import BaseModel


class ProductPreviewDTO(BaseModel):
    product_table_id: int
    name: str
    price: float
    imageUrl: str
    platform: str


