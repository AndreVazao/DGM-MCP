from ..config.config_manager import MCPConfig
from ..security.path_guard import PathGuard
from ..security.audit_logger import AuditLogger
from ..tools.filesystem_tool import FilesystemTool
from ..tools.git_tool import GitTool
from ..tools.shell_tool import ShellTool
from ..tools.patch_tool import PatchTool
from ..tools.repo_tool import RepoTool
from ..control.task_manager import TaskManager
from ..control.worker import Worker
from ..control.cognitive_agent import CognitiveAgent
from ..llm.llm_manager import LLMManager
from .logger import DGMLogger
from .observability import Observability

class MCPRuntime:
    def __init__(self, config: MCPConfig):
        self.config = config
        self.running = False
        self.path_guard = PathGuard(config.allowed_paths)
        self.audit = AuditLogger()
        self.tools = {}
        self.task_manager = TaskManager()
        self.logger = DGMLogger()
        self.observability = Observability()
        self.llm_manager = LLMManager(config)
        self.agent = None
        self.worker = None

    def start(self):
        self.running = True
        self.logger.info("🚀 MCP Runtime iniciado")

        self._register_tools()

        self.agent = CognitiveAgent(self, self.task_manager)
        for tool in self.tools.values():
            self.agent.register_tool(tool)

        self.worker = Worker(self, self.task_manager)
        self.worker.start()

        # LLMManager already sets the default provider based on config during init
        # but we can force it again if needed.
        if self.config.default_llm:
            self.llm_manager.set_provider(self.config.default_llm)

    def _register_tools(self):
        tools = [
            FilesystemTool(self.path_guard, self.audit),
            GitTool(self.path_guard, self.audit),
            ShellTool(self.path_guard, self.audit, self.config.max_tool_execution_seconds),
            PatchTool(self.path_guard, self.audit),
            RepoTool(self.path_guard, self.audit),
        ]
        for tool in tools:
            self.tools[tool.name] = tool
            self.logger.success(f"Tool carregada: {tool.name}")

    def stop(self):
        self.running = False
        if self.worker:
            self.worker.stop()
        self.logger.info("⛔ Runtime parado")
