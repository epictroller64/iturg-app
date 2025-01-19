
from pydantic import BaseModel


class OpenAIResponse(BaseModel):
    features: list[str]
