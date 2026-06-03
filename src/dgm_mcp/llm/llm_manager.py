from typing import Dict
from rich.console import Console
from .base_provider import BaseLLMProvider, LLMResponse
from .providers.openai_provider import OpenAIProvider
from .providers.anthropic_provider import AnthropicProvider
from .providers.gemini_provider import GeminiProvider
from .providers.grok_provider import GrokProvider
from .providers.ollama_provider import OllamaProvider

console = Console()

class LLMManager:
    def __init__(self):
        self.providers: Dict[str, BaseLLMProvider] = {}
        self.current_provider = None
        self._register_all()

    def _register_all(self):
        providers = [
            OpenAIProvider(),      # ChatGPT + Codex
            AnthropicProvider(),   # Claude
            GeminiProvider(),
            GrokProvider(),
            OllamaProvider(),
        ]
        for p in providers:
            if p.is_available():
                self.providers[p.name.lower()] = p
                console.print(f"   ✅ LLM carregado: [green]{p.name}[/green]")

    def set_provider(self, name: str):
        key = name.lower()
        if key in self.providers:
            self.current_provider = self.providers[key]
            console.print(f"[bold green]LLM ativo: {self.current_provider.name}[/bold green]")
            return True
        console.print(f"[red]Provider {name} não disponível[/red]")
        return False

    def generate(self, prompt: str, system_prompt: str = None, **kwargs):
        if not self.current_provider:
            # Default para o primeiro disponível
            if self.providers:
                self.current_provider = list(self.providers.values())[0]
            else:
                return LLMResponse("Nenhum LLM disponível", "none", False)

        return self.current_provider.generate(prompt, system_prompt, **kwargs)

    def list_available(self):
        return list(self.providers.keys())
