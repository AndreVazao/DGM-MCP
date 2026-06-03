import subprocess
from ..base_provider import BaseLLMProvider, LLMResponse

class OllamaProvider(BaseLLMProvider):
    name = "Ollama"
    model = "llama3.2"   # pode ser alterado

    def is_available(self) -> bool:
        try:
            result = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=3)
            return result.returncode == 0
        except:
            return False

    def generate(self, prompt: str, system_prompt: str = None, **kwargs):
        try:
            import ollama
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
