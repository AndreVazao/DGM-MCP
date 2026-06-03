import os
try:
    import google.generativeai as genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

from ..base_provider import BaseLLMProvider, LLMResponse

class GeminiProvider(BaseLLMProvider):
    name = "Gemini"
    model = "gemini-1.5-pro"

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key and HAS_GENAI:
            genai.configure(api_key=api_key)
            self.model_instance = genai.GenerativeModel(self.model)
        else:
            self.model_instance = None

    def is_available(self) -> bool:
        return HAS_GENAI and bool(os.getenv("GEMINI_API_KEY"))

    def generate(self, prompt: str, system_prompt: str = None, **kwargs):
        if not self.model_instance:
            return LLMResponse("Gemini API key not set or library not installed", self.model, False)
        try:
            full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
            response = self.model_instance.generate_content(full_prompt)
            return LLMResponse(
                content=response.text,
                model=self.model
            )
        except Exception as e:
            return LLMResponse(str(e), self.model, False)
