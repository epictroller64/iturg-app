from pydantic import BaseModel
from typing import List

class PreScrapedHVProduct(BaseModel):
    title: str
    transaction_type: str
    category: List[str]
    location: str
    link: str