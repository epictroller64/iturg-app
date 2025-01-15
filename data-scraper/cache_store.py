from models.Product import Product
from typing import Optional, List



class CacheStore:
    """In memory cache store for products"""
    def __init__(self, products: List[Product] = []):
        self.products = {product.id: product for product in products}

    def get_product(self, id: str) -> Optional[Product]:
        return self.products.get(id)

    def set_product(self, id: str, product: Product):
        self.products[id] = product
