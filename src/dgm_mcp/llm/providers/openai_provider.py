import os
from openai import OpenAI
from ..base_provider import BaseLLMProvider, LLMResponse

class OpenAIProvider(BaseLLMProvider):
    name = "ChatGPT"
    model = "gpt-4o"

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key) if api_key else None

    def is_available(self) -> bool:
        return bool(os.getenv("OPENAI_API_KEY"))

    def generate(self, prompt: str, system_prompt: str = None, **kwargs):
        if not self.client:
            return LLMResponse("OpenAI API key not set", self.model, False)
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                **kwargs
            )
            return LLMResponse(
                content=response.choices[0].message.content,
                model=self.model
            )
        except Exception as e:
            return LLMResponse(str(e), self.model, False)
