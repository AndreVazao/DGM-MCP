import unittest
from unittest.mock import MagicMock
from dgm_mcp.control.cognitive_agent import CognitiveAgent

class TestCognitiveAgent(unittest.TestCase):
    def setUp(self):
        self.runtime = MagicMock()
        self.task_manager = MagicMock()
        self.agent = CognitiveAgent(self.runtime, self.task_manager)

    def test_session_creation(self):
        session_id = self.agent.create_session()
        self.assertIn(session_id, self.agent.sessions)
        session = self.agent.get_session(session_id)
        self.assertEqual(session.id, session_id)

if __name__ == '__main__':
    unittest.main()
