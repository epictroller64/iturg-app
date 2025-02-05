from pydantic import BaseModel
from typing import List

class PreScrapedHVProduct(BaseModel):
    id: str
    title: str
    transaction_type: str
    category: List[str]
    location: str
    link: str