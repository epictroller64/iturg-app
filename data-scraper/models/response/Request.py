from pydantic import BaseModel
from typing import List
from models.dto.ProductPreviewDTO import ProductPreviewDTO


class ProductPreviewResponse(BaseModel):
    page: int
    page_size: int
    max_pages: int
    data: List[ProductPreviewDTO]