import unittest
from dgm_mcp.config.config_manager import ConfigManager
from dgm_mcp.core.runtime import MCPRuntime

class TestBasic(unittest.TestCase):
    def test_config_loading(self):
        config = ConfigManager().load()
        self.assertIsNotNone(config)
        self.assertGreater(len(config.allowed_paths), 0)

    def test_runtime_initialization(self):
        config = ConfigManager().load()
        runtime = MCPRuntime(config)
        runtime.start()
        self.assertTrue(runtime.running)
        self.assertGreaterEqual(len(runtime.tools), 3)
        self.assertIsNotNone(runtime.llm_manager)
        self.assertIsNotNone(runtime.observability)

if __name__ == '__main__':
    unittest.main()
