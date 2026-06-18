import os
from typing import Optional
from ..base_provider import BaseLLMProvider, LLMResponse
from ...config.config_manager import MCPConfig

class GrokProvider(BaseLLMProvider):
    name = "Grok"
    model = "grok-3-beta"

    def __init__(self, config: Optional[MCPConfig] = None):
        self.config = config
        try:
            from openai import OpenAI
            api_key = (config.xai_key if config else None) or os.getenv("XAI_API_KEY")
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
        api_key = (self.config.xai_key if self.config else None) or os.getenv("XAI_API_KEY")
        return bool(api_key)

    def generate(self, prompt: str, system_prompt: str = None, **kwargs):
        if not self.client:
            return LLMResponse("Erro Grok: Cliente não inicializado (XAI_API_KEY em falta?)", self.model, False)
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.6,
                max_tokens=4096,
                **kwargs
            )
            return LLMResponse(
                content=response.choices[0].message.content.strip(),
                model=self.model,
                success=True
            )
        except Exception as e:
            return LLMResponse(f"Erro Grok: {str(e)}", self.model, False)
