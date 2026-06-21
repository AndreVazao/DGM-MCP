import subprocess
from typing import Optional
from ..base_provider import BaseLLMProvider, LLMResponse
from ...config.config_manager import MCPConfig

class OllamaProvider(BaseLLMProvider):
    name = "Ollama"
    model = "llama3.2"

    def __init__(self, config: Optional[MCPConfig] = None):
        self.config = config
        if config and config.ollama_model:
            self.model = config.ollama_model

    def is_available(self) -> bool:
        try:
            result = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=3)
            return result.returncode == 0
        except Exception:
            return False

    def generate(self, prompt: str, system_prompt: str = None, **kwargs):
        try:
            import ollama
            # If ollama library supports setting base_url via env or config, it should be done here.
            # Usually it uses OLLAMA_HOST env var.
            response = ollama.chat(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            return LLMResponse(
                content=response['message']['content'],
                model=self.model
            )
        except Exception as e:
            return LLMResponse(str(e), self.model, False)
