import unittest
from dgm_mcp.core.runtime import MCPRuntime
from dgm_mcp.config.config_manager import MCPConfig

class TestBasicImport(unittest.TestCase):
    def test_import_runtime(self):
        config = MCPConfig()
        runtime = MCPRuntime(config)
        self.assertIsNotNone(runtime)
        self.assertEqual(runtime.config.max_workers, 4)

if __name__ == "__main__":
    unittest.main()
