import unittest
import os
from dgm_mcp.llm.llm_manager import LLMManager
from dgm_mcp.llm.base_provider import LLMResponse

class TestLLMManager(unittest.TestCase):
    def test_manager_init(self):
        manager = LLMManager()
        # Should initialize even with no providers available
        self.assertIsInstance(manager.providers, dict)

    def test_set_invalid_provider(self):
        manager = LLMManager()
        result = manager.set_provider("NonExistent")
        self.assertFalse(result)

    def test_generate_no_provider(self):
        manager = LLMManager()
        # If no providers are available, it should return a failure response
        if not manager.providers:
            response = manager.generate("Hello")
            self.assertFalse(response.success)
            self.assertEqual(response.content, "Nenhum LLM disponível")

if __name__ == '__main__':
    unittest.main()
