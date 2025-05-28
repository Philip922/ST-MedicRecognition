from typing import List, Optional, TypeVar, Type

from google import genai
from google.genai import types
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class GeminiClient:
    """
    A client for interacting with Google's Gemini API for content generation.
    This class provides functionality for generating plain text and structured JSON content
    using the Gemini large language model API.
    """

    def __init__(self, api_key: str, model: str = "gemini-2.0-flash"):
        """
        Initialize the GeminiClient.
        Args: api_key (str): API key for authenticating with Gemini API.
              model (str, optional): Model version to use. Defaults to "gemini-2.0-flash".
        """
        self.api_key = api_key
        self.model = model
        self.client = genai.Client(api_key=self.api_key)

    def generate_content(
            self,
            messages: List[str],
            system_instruction: Optional[str] = None,
            max_output_tokens: int = 512,
            temperature: float = 0.7
    ) -> Optional[str]:
        """
        Generate plain text content based on a list of prompts.
        Args:
            messages (List[str]): List of user prompts.
            system_instruction (Optional[str]): Optional system instruction to guide the model.
            max_output_tokens (int): Maximum number of tokens to return.
            temperature (float): Sampling temperature for generation diversity.
        Returns:
            Optional[str]: The generated response as a string, or None if an error occurs.
        """
        try:
            config = types.GenerateContentConfig(
                system_instruction=system_instruction,
                max_output_tokens=max_output_tokens,
                temperature=temperature
            )
            response = self.client.models.generate_content(
                model=self.model,
                contents=messages,
                config=config
            )
            return response.text
        except Exception as e:
            print(f"Error during Gemini API request: {e}")
            return None

    def generate_json_content(self, prompt: str, schema: Type[T]):
        """
        Generate structured JSON content from a prompt using a specified Pydantic schema.
        Args: prompt (str): The prompt to send to the Gemini API.
              schema (Type[T]): A Pydantic model class defining the expected schema of the response.
        Returns: Optional[List[T]]: A list of parsed Pydantic model instances, or None if an error occurs.
        """
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_schema": schema,
                },
            )
            return response.parsed
        except Exception as e:
            print(f"Error during Gemini JSON request: {e}")
            return None