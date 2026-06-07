import os
from openai import OpenAI
from ..base_provider import BaseLLMProvider, LLMResponse

class GrokProvider(BaseLLMProvider):
    name = "Grok"
    model = "grok-3-beta"          # ou grok-beta, conforme disponibilidade atual

    def __init__(self):
        self.api_key = os.getenv("XAI_API_KEY")
        if self.api_key:
            self.client = OpenAI(
                api_key=self.api_key,
                base_url="https://api.x.ai/v1"
            )
        else:
            self.client = None

    def is_available(self) -> bool:
        return bool(os.getenv("XAI_API_KEY"))

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
