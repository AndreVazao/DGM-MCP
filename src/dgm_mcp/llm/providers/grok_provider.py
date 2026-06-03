import os
from ..base_provider import BaseLLMProvider, LLMResponse

class GrokProvider(BaseLLMProvider):
    name = "Grok"
    model = "grok-beta"

    def __init__(self):
        try:
            from openai import OpenAI
            api_key = os.getenv("XAI_API_KEY")
            if api_key:
                self.client = OpenAI(
                    api_key=api_key,
                    base_url="https://api.x.ai/v1"
                )
            else:
                self.client = None
        except ImportError:
            self.client = None

    def is_available(self) -> bool:
        try:
            import openai
            return bool(os.getenv("XAI_API_KEY"))
        except ImportError:
            return False

    def generate(self, prompt: str, system_prompt: str = None, **kwargs):
        if not self.client:
            return LLMResponse("OpenAI library not installed or XAI API key not set", self.model, False)
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                **kwargs
            )
            return LLMResponse(
                content=response.choices[0].message.content,
                model=self.model
            )
        except Exception as e:
            return LLMResponse(str(e), self.model, False)
