# ARCHITECTURE_MAP.md

## Current Architecture Overview (Transitioning)

```mermaid
graph TD
    CLI[CLI: main.py] --> Runtime[Core: Runtime]
    Runtime --> Agent[Control: CognitiveAgent]
    Runtime --> Worker[Control: Worker - Thread]
    Runtime --> TM[Control: TaskManager]
    Runtime --> LLM[LLM: LLMManager]
    Runtime --> Tools[Tools: Git, Shell, FS, etc.]

    Worker --> TM
    Worker --> Agent
    Agent --> TM
    Agent --> LLM
    Agent --> Tools
    Tools --> Security[Security: PathGuard / Audit]
```

## Target Architecture (MCP-Native)

The architecture is designed to support multiple clients via standardized transports, while keeping the core logic isolated.

```mermaid
graph TD
    subgraph "Clients"
        Claude[Claude Desktop]
        Cursor[Cursor / Windsurf]
        Custom[Custom Apps]
    end

    subgraph "Transport Layer"
        Stdio[STDIO Transport]
        SSE[SSE Transport / FastAPI]
    end

    subgraph "MCP Protocol Layer"
        JSONRPC[JSON-RPC 2.0 Engine]
        Registry[Tool/Resource/Prompt Registry]
        Adapter[Tool Adapter]
    end

    subgraph "Core DGM-MCP (Protocol Agnostic)"
        Runtime[Runtime Orchestrator]
        Tools[Internal Tools]
        Security[PathGuard / Audit]
        Agent[Cognitive Agent]
    end

    Claude -- stdio --> Stdio
    Cursor -- sse --> SSE
    Stdio --> JSONRPC
    SSE --> JSONRPC
    JSONRPC --> Registry
    Registry --> Adapter
    Adapter --> Runtime
    Runtime --> Tools
    Tools --> Security
```

### Key Architectural Principles:

1.  **Isolation**: The `Core` (Runtime, Tools, Security) has zero knowledge of MCP. It only knows how to execute tasks and enforce security.
2.  **Standardization**: All communication follows the Model Context Protocol v1.0.
3.  **Flexibility**: New tools added to `Core` are automatically exposed via the `Registry` and `Adapter`.
4.  **Transport Independence**: The same protocol logic handles both local (Stdio) and remote (SSE) clients.

## Component Roles in MCP Context:

- **Registry**: The single source of truth for tool schemas. It scans the existing toolset and generates MCP-compatible metadata.
- **Adapter**: Maps the flattened MCP `call_tool` parameters to the specific keyword arguments required by our internal `execute` methods.
- **Runtime**: Continues to be the orchestrator for session state, logging, and security context.

## Migration Status:
- **Core Logic**: 100% Stable.
- **REST Bridge**: Deprecated (replaced by SSE).
- **MCP Layer**: Under implementation (Phase 1-2).
- **Transports**: Pending (Phase 4 & 7).
