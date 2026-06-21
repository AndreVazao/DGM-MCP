import json
import os
import unittest
from dgm_mcp.security.audit_logger import AuditLogger

class TestAuditLogger(unittest.TestCase):
    def setUp(self):
        self.test_log = "test_audit.log"
        self.logger = AuditLogger(self.test_log)

    def tearDown(self):
        if os.path.exists(self.test_log):
            os.remove(self.test_log)

    def test_log_creation(self):
        self.logger.log("test_tool", "test_action", True, 0.1234)
        self.assertTrue(os.path.exists(self.test_log))

        with open(self.test_log, "r") as f:
            entry = json.loads(f.readline())
            self.assertEqual(entry["tool"], "test_tool")
            self.assertEqual(entry["action"], "test_action")
            self.assertTrue(entry["success"])
            self.assertEqual(entry["duration_seconds"], 0.1234)

    def test_log_with_error_and_details(self):
        self.logger.log(
            "error_tool",
            "error_action",
            False,
            0.5,
            error="Something went wrong",
            details={"key": "value"}
        )

        with open(self.test_log, "r") as f:
            entry = json.loads(f.readline())
            self.assertEqual(entry["error"], "Something went wrong")
            self.assertEqual(entry["details"], {"key": "value"})

    def test_invalid_path_fallback(self):
        # This shouldn't crash, just print to console
        logger = AuditLogger("/invalid/path/to/log.log")
        logger.log("fail_tool", "fail_action", True, 0.1)
