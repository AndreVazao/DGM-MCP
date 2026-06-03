import os
from anthropic import Anthropic
from ..base_provider import BaseLLMProvider, LLMResponse

class AnthropicProvider(BaseLLMProvider):
    name = "Claude"
    model = "claude-3-5-sonnet-20240620"

    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        self.client = Anthropic(api_key=api_key) if api_key else None

    def is_available(self) -> bool:
        return bool(os.getenv("ANTHROPIC_API_KEY"))

    def generate(self, prompt: str, system_prompt: str = None, **kwargs):
        if not self.client:
            return LLMResponse("Anthropic API key not set", self.model, False)
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                system=system_prompt or "You are a helpful software engineering assistant.",
                messages=[{"role": "user", "content": prompt}],
                **kwargs
            )
            return LLMResponse(
                content=response.content[0].text,
                model=self.model
            )
        except Exception as e:
            return LLMResponse(str(e), self.model, False)
