from repository.product import get_all_products
from group_pipeline import GroupPipeline
from factory import LoggerFactory
from openai_communication import OpenAICommunication
from models.database.Product import Product
from models.response.OpenAIResponse import OpenAIResponse



class Parser:
    """Help parse titles into more understandable structures"""
    def __init__(self):
        self.group_pipeline = GroupPipeline()
        self.logger = LoggerFactory.get_logger("Parser")
        self.openai = OpenAICommunication()

    async def parse_all_products(self):
        """Parse products in batches of 10"""
        products = get_all_products()
        for i in range(0, len(products), 10):
            batch = products[i:i+10]
            for product in batch:
                await self.parse_product(product)

    
    async def parse_product(self, product: Product) -> OpenAIResponse:
        """Parse product title using OpenAI to extract key features and group products"""
        try:
            openai_response = await self.openai.ask_openai([
                    {"role": "system", "content": "You are a product classifier that extracts product technical features from product titles. Return them as an JSON array of strings. Titles are in Estonian. Extract only main features. Most are Apple products."},
                    {"role": "user", "content": product.name}
                ], OpenAIResponse)
            if openai_response:
                features = openai_response.features
                # Create group junctions for the product
                await self.group_pipeline.process_groups(features, product.id)
            # if there was no response from openai, continue and fix the issues later
        except Exception as e:
            self.logger.error(f"Error parsing product: {e}")
            raise e
    