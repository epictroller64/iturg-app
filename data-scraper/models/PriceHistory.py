from pydantic import BaseModel
from datetime import datetime


class PriceHistory(BaseModel):
    id: int
    product_table_id: int
    price: float
    found_at: datetime

    model_config = {
        "from_attributes": True
    }


