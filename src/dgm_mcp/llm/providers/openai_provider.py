import os
from typing import Optional
from ..base_provider import BaseLLMProvider, LLMResponse
from ...config.config_manager import MCPConfig

class OpenAIProvider(BaseLLMProvider):
    name = "ChatGPT"
    model = "gpt-4o"

    def __init__(self, config: Optional[MCPConfig] = None):
        self.config = config
        try:
            from openai import OpenAI
            api_key = (config.openai_key if config else None) or os.getenv("OPENAI_API_KEY")
            self.client = OpenAI(api_key=api_key) if api_key else None
        except ImportError:
            self.client = None

    def is_available(self) -> bool:
        api_key = (self.config.openai_key if self.config else None) or os.getenv("OPENAI_API_KEY")
        try:
            import openai
            return bool(api_key)
        except ImportError:
            return False

    def generate(self, prompt: str, system_prompt: str = None, **kwargs):
        if not self.client:
            return LLMResponse("OpenAI library not installed or API key not set", self.model, False)
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
