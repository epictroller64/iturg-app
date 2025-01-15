from database import get_db_connection
import datetime


class PriceHistory:
    id: int
    product_id: str
    platform: str
    price: float
    found_at: datetime

    def __init__(self, product_id, platform, price, found_at, id=None):
        self.id = id
        self.product_id = product_id
        self.platform = platform
        self.price = price
        self.found_at = found_at


