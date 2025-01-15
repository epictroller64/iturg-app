from pydantic import BaseModel


class ProductPreviewDTO(BaseModel):
    id: str
    name: str
    price: float
    imageUrl: str
    platform: str

    def __init__(self, id: str, name: str, price: float, imageUrl: str, platform: str):
        self.id = id
        self.name = name
        self.price = price
        self.imageUrl = imageUrl
        self.platform = platform

    def __iter__(self):
        yield 'id', self.id
        yield 'name', self.name 
        yield 'price', self.price
        yield 'imageUrl', self.imageUrl
        yield 'platform', self.platform

