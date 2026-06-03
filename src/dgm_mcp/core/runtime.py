from ..config.config_manager import MCPConfig
from ..security.path_guard import PathGuard
from ..tools.filesystem_tool import FilesystemTool

class MCPRuntime:
    def __init__(self, config: MCPConfig):
        self.config = config
        self.running = False
        self.path_guard = PathGuard(config.allowed_paths)
        self.components = {}
        self.tools = {}

    def start(self):
        self.running = True
        print("🚀 MCP Runtime iniciado")

        # Registar tools
        fs_tool = FilesystemTool(self.path_guard)
        self.register_tool(fs_tool)

    def stop(self):
        self.running = False
        print("⛔ MCP Runtime parado")

    def register_tool(self, tool):
        self.tools[tool.name] = tool
        print(f"Tool registada: {tool.name}")
