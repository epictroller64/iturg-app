from typing import Optional, List, Dict
from models.database.Product import Product


class CacheStore:
    """In memory cache store for products"""
    products: Dict[int, Product]
    grouped_products: Dict[str, Product]
    def __init__(self, products: List[Product] = []):
        self.products = {product.id: product for product in products}
        # Use tuple as the key
        self.grouped_products = {
            (product.product_id, product.platform): product for product in products
        }

    def get_product(self, id: int) -> Optional[Product]:
        return self.products.get(id)
    
    def get_product_by_product_id_and_platform(self, product_id: str, platform: str) -> Optional[Product]:
        return self.grouped_products.get((product_id, platform))
    
    def set_product_by_product_id_and_platform(self, product_id: str, platform: str, product: Product):
        self.grouped_products[(product_id, platform)] = product

    def set_product(self, id: int, product: Product):
        self.products[id] = product
