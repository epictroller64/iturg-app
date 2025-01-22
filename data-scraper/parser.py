import json
from typing import List
from openai import AsyncOpenAI
from repository.product import get_all_products
from models.Product import Product
import os
from group_pipeline import GroupPipeline
from models.OpenAIResponse import OpenAIResponse
class Parser:
    """Help parse titles into more understandable structures"""
    def __init__(self):
        self.group_pipeline = GroupPipeline()
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is not set in the environment variables")
        """Initialize parser with OpenAI API key"""
        
        self.openai = AsyncOpenAI(api_key=self.api_key)

    async def parse_all_products(self):
        """Parse products in batches of 10"""
        products = get_all_products()
        for i in range(0, len(products), 10):
            batch = products[i:i+10]
            for product in batch:
                await self.parse_product(product)

    async def ask_openai(self, product: Product) -> OpenAIResponse:
        """Parse product title using OpenAI to extract key features and group products"""

        response = await self.openai.beta.chat.completions.parse(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a product classifier that extracts product technical features from product titles. Return them as an JSON array of strings. Titles are in Estonian. Extract only main features. Most are Apple products."},
                {"role": "user", "content": product.name}
            ],
            response_format=OpenAIResponse
        )

        return response.choices[0].message.parsed
    
    async def parse_product(self, product: Product):
        """Parse product title using OpenAI to extract key features and group products"""
        try:
            openai_response = await self.ask_openai(product)
            features = openai_response.features
            # Create group junctions for the product
            await self.group_pipeline.process_groups(features, product.id)
        except Exception as e:
            self.logger.error(f"Error parsing product: {e}")
            raise e
    
    def test_parse(self):
        products = get_all_products()
        for index, product in enumerate(products):
            parsed_product = self.parse_product(product)
            json_obj = json.loads(parsed_product)
            print(f"Parsed product {index + 1}: {json_obj.features}")
