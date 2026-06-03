from ..config.config_manager import MCPConfig
from ..security.path_guard import PathGuard
from ..tools.filesystem_tool import FilesystemTool
from ..tools.git_tool import GitTool
from ..tools.shell_tool import ShellTool
from ..tools.patch_tool import PatchTool
from ..control.task_manager import TaskManager
from ..control.worker import Worker
from ..control.cognitive_agent import CognitiveAgent
from ..llm.llm_manager import LLMManager
from .memory import Memory
from .logger import DGMLogger
from .observability import Observability
from rich.console import Console

console = Console()

class MCPRuntime:
    def __init__(self, config: MCPConfig):
        self.config = config
        self.running = False
        self.path_guard = PathGuard(config.allowed_paths)
        self.tools = {}
        self.task_manager = TaskManager()
        self.agent = None
        self.worker = None
        self.console = console
        self.memory = None
        self.llm_manager = LLMManager()
        self.logger = DGMLogger()
        self.observability = Observability()

    def start(self):
        self.running = True
        self.logger.success("MCP Runtime iniciado")

        # Registar todas as tools
        self._register_tools()

        # LLM Manager
        config_llm = getattr(self.config, 'default_llm', 'Claude')
        self.llm_manager.set_provider(config_llm)
        self.logger.info(f"LLM padrão configurado: {config_llm}")

        # Inicializar Agent e Worker
        self.agent = CognitiveAgent(self, self.task_manager)
        self.worker = Worker(self, self.task_manager)

        # Registar tools no Agent
        for tool in self.tools.values():
            self.agent.register_tool(tool)

        # Inicializar Memory
        self.memory = Memory(self)
        self.logger.success("Memory system carregado")

        self.worker.start()

    def _register_tools(self):
        tools = [
            FilesystemTool(self.path_guard),
            GitTool(self.path_guard),
            ShellTool(self.path_guard),
            PatchTool(self.path_guard),
        ]
        for tool in tools:
            self.tools[tool.name] = tool
            self.logger.success(f"Tool carregada: {tool.name}")

    def stop(self):
        self.running = False
        self.logger.warning("Runtime parado")
