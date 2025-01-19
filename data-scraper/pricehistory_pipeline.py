from models.PriceHistory import PriceHistory
from repository.pricehistory import insert_price_history
from factory import LoggerFactory
from datetime import datetime
class PriceHistoryPipeline:

    def __init__(self):
        self.logger = LoggerFactory.get_logger("PriceHistoryPipeline")

    async def process_price_history(self, product_table_id: int, price_string: str, found_at: datetime):
        price = self.transform_price_history(price_string)
        if price:
            await insert_price_history(PriceHistory(id=0, product_table_id=product_table_id, price=price, found_at=found_at))
            self.logger.info(f"Processed price history for {product_table_id}")

    def transform_price_history(self, price_string: str):
        try:
            # Remove Euro sign and convert to float
            if price_string == "Hind määramata":
                price = 0
            elif price_string == "":
                price = 0
            else:
                price = float(str(price_string).replace("€", "").replace(" ", ""))
        except Exception as e:
            self.logger.error(f"Error transforming price history for {price_string}: {e}")
            return None
        return price
