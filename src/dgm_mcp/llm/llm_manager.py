from typing import Dict, Optional
from rich.console import Console

from .base_provider import BaseLLMProvider, LLMResponse
from .providers.openai_provider import OpenAIProvider
from .providers.anthropic_provider import AnthropicProvider
from .providers.gemini_provider import GeminiProvider
from .providers.grok_provider import GrokProvider
from .providers.ollama_provider import OllamaProvider
from ..config.config_manager import MCPConfig

console = Console()


class LLMManager:
    def __init__(self, config: Optional[MCPConfig] = None, quiet: bool = False):
        self.config = config
        self.quiet = quiet
        self.providers: Dict[str, BaseLLMProvider] = {}
        self.current_provider: Optional[BaseLLMProvider] = None
        self._auto_detect_and_register()

    def _auto_detect_and_register(self):
        """Detecta automaticamente quais LLMs estao disponiveis"""
        candidates = [
            OpenAIProvider(self.config),
            AnthropicProvider(self.config),
            GeminiProvider(self.config),
            GrokProvider(self.config),
            OllamaProvider(self.config),
        ]

        for provider in candidates:
            if provider.is_available():
                self.providers[provider.name.lower()] = provider
                if not self.quiet:
                    console.print(f"LLM detectado: {provider.name} ({provider.model})")

        if self.providers:
            preferred_order = ["grok", "claude", "chatgpt", "ollama"]
            if self.config and self.config.default_llm.lower() in self.providers:
                self.set_provider(self.config.default_llm)
            else:
                for pref in preferred_order:
                    if pref in self.providers:
                        self.set_provider(pref)
                        break
                else:
                    self.set_provider(list(self.providers.keys())[0])
        else:
            if not self.quiet:
                console.print("Nenhum LLM encontrado. Configure API keys no .env")

    def set_provider(self, name: str) -> bool:
        key = name.lower()
        if key in self.providers:
            self.current_provider = self.providers[key]
            if not self.quiet:
                console.print(f"LLM ativo: {self.current_provider.name}")
            return True
        return False

    def generate(self, prompt: str, system_prompt: str = None, **kwargs):
        if not self.current_provider:
            return LLMResponse("Nenhum LLM disponível", "none", False)
        return self.current_provider.generate(prompt, system_prompt, **kwargs)

    def list_available(self):
        return list(self.providers.keys())
