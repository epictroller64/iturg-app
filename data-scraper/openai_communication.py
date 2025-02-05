from typing import List, TypeVar, Type
from openai import OpenAI
import os
from factory import LoggerFactory
from openai import AsyncOpenAI
from pydantic import BaseModel

T = TypeVar('T')

class OpenAICommunication():

    def __init__(self, version: str = "gpt-4o"):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is not set in the environment variables")
        """Initialize parser with OpenAI API key"""
        self.logger = LoggerFactory.get_logger("OpenAI")
        self.openai = AsyncOpenAI(api_key=self.api_key)
        self.version = version

    async def ask_openai(self, messages: List[dict], response_format: Type[T] = None) -> T | None:
        """Parse product title using OpenAI to extract key features and group products"""
        try:
            response = await self.openai.beta.chat.completions.parse(
                model=self.version,
                messages=messages,
                response_format=response_format
            )

            return response.choices[0].message.parsed
        except Exception as e:
            self.logger.error(f"Error retrieving OpenAI response: {str(e)}")
            return None
