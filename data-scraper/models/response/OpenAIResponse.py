
from pydantic import BaseModel


class OpenAIResponse(BaseModel):
    features: list[str]

class OpenAIHVProduct(BaseModel):
    title: str
    price: float

class OpenAIHVPostResponse(BaseModel):
    products: list[OpenAIHVProduct]