from typing import Dict, Optional
from rich.console import Console
import os
import subprocess

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
        self.current_provider: Optional[BaseLLMProvider] = None
        self._auto_detect_and_register()

    def _auto_detect_and_register(self):
        """Detecta automaticamente quais LLMs estão disponíveis"""
        candidates = [
            OpenAIProvider(),      # ChatGPT + Codex
            AnthropicProvider(),   # Claude
            GeminiProvider(),
            GrokProvider(),
            OllamaProvider(),
        ]

        for provider in candidates:
            if provider.is_available():
                self.providers[provider.name.lower()] = provider
                console.print(f"   ✅ LLM detectado: [green]{provider.name} ({provider.model})[/green]")

        if self.providers:
            # Usa Claude por default se disponível, senão o primeiro
            preferred = "claude" if "claude" in self.providers else list(self.providers.keys())[0]
            self.set_provider(preferred)
        else:
            console.print("[yellow]⚠️ Nenhum LLM encontrado. Configure API keys no .env[/yellow]")

    def set_provider(self, name: str) -> bool:
        key = name.lower()
        if key in self.providers:
            self.current_provider = self.providers[key]
            console.print(f"[bold green]🤖 LLM Ativo: {self.current_provider.name}[/bold green]")
            return True
        return False

    def generate(self, prompt: str, system_prompt: str = None, **kwargs):
        if not self.current_provider:
            return LLMResponse("Nenhum LLM disponível", "none", False)
        return self.current_provider.generate(prompt, system_prompt, **kwargs)

    def list_available(self):
        return list(self.providers.keys())
