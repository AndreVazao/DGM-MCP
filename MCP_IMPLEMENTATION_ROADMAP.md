# MCP_IMPLEMENTATION_ROADMAP.md

This roadmap outlines the transition from a custom REST API to a standard Model Context Protocol (MCP) server.

## Implementation Phases

### Phase 1: JSON-RPC Core
**Goal**: Implement the foundational JSON-RPC 2.0 protocol layer.
- **Components**: Request/Response parsing, Error handling, Id management.
- **Files**: `src/dgm_mcp/mcp/jsonrpc.py`, `src/dgm_mcp/mcp/messages.py`.

### Phase 2: Tool Discovery
**Goal**: Implement the tool registration and discovery mechanism.
- **Components**: `ToolRegistry`, `ListTools` handler.
- **Files**: `src/dgm_mcp/mcp/tool_registry.py`, `src/dgm_mcp/mcp/handlers/tools.py`.

### Phase 3: Tool Invocation
**Goal**: Connect MCP tool calls to the underlying Tool implementations.
- **Components**: `ToolAdapter`, `CallTool` handler.
- **Security**: Ensures `PathGuard` and `AuditLogger` are still enforced.

### Phase 4: STDIO Transport
**Goal**: Enable local communication via Standard Input/Output.
- **Target**: Claude Desktop, Cursor, and other local IDEs.
- **Files**: `src/dgm_mcp/mcp/transports/stdio.py`.

### Phase 5: Resources
**Goal**: Implement the MCP Resources specification.
- **Components**: `ListResources`, `ReadResource`.
- **Use Cases**: Exposing logs, configurations, and file contents as resources.

### Phase 6: Prompts
**Goal**: Implement the MCP Prompts specification.
- **Components**: `ListPrompts`, `GetPrompt`.
- **Use Cases**: Exposing system prompt templates and specialized coding prompts.

### Phase 7: SSE Transport
**Goal**: Enable remote communication via Server-Sent Events.
- **Target**: Web-based clients and remote integrations.
- **Files**: `src/dgm_mcp/mcp/transports/sse.py`.

### Phase 8: Claude Desktop Validation
**Goal**: Final end-to-end verification.
- **Action**: Use the official MCP Inspector and Claude Desktop to validate all features.

---

## PR Sequence (Iterative Delivery)

### PR1: JSON-RPC Core
- Core protocol logic.
- Basic message types.
- Unit tests for protocol compliance.

### PR2: Tool Discovery & Schemas
- `ToolRegistry` implementation.
- Detailed JSON Schemas for all existing tools.
- `tools/list` endpoint functionality.

### PR3: STDIO Transport
- Stdio transport layer.
- CLI command (`dgm-mcp run-stdio`) to start the server in stdio mode.

### PR4: Claude Desktop Validation
- Documentation and configuration for Claude Desktop.
- End-to-end tests for Tool Discovery and Invocation.

---

## Architectural Constraints
1. **Decoupling**: The `Runtime` and `Tools` must NOT know about MCP or JSON-RPC.
2. **Adapter Pattern**: Use a `ToolAdapter` to bridge the gap between MCP messages and the existing `BaseTool` interface.
3. **Immutability**: Core business logic remains unchanged; MCP is purely a communication layer.

