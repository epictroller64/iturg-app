from models.PriceHistory import PriceHistory
from repository.pricehistory import insert_price_history
from factory import LoggerFactory

class PriceHistoryPipeline:

    def __init__(self):
        self.logger = LoggerFactory.get_logger("PriceHistoryPipeline")

    def process_price_history(self, price_history: PriceHistory):
        transformed_price_history = self.transform_price_history(price_history)
        if transformed_price_history:
            insert_price_history(transformed_price_history)
            self.logger.info(f"Processed price history for {price_history.product_id}")

    def transform_price_history(self, price_history: PriceHistory):
        try:
            # Remove Euro sign and convert to float
            if price_history.price == "Hind määramata":
                price_history.price = 0
            elif price_history.price == "":
                price_history.price = 0
            else:
                price_history.price = float(str(price_history.price).replace("€", "").replace(" ", ""))
        except Exception as e:
            self.logger.error(f"Error transforming price history for {price_history.product_id}: {e}")
            return None
        return price_history
