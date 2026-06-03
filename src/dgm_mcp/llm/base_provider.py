from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class LLMResponse:
    def __init__(self, content: str, model: str, success: bool = True):
        self.content = content
        self.model = model
        self.success = success

class BaseLLMProvider(ABC):
    name: str
    model: str

    @abstractmethod
    def generate(self, prompt: str, system_prompt: str = None, **kwargs) -> LLMResponse:
        pass

    @abstractmethod
    def is_available(self) -> bool:
        pass
