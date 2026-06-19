# MCP_IMPLEMENTATION_ROADMAP.md

This roadmap outlines the transition from a custom REST API to an MCP-compatible server.

## Phase 1: Foundation & JSON-RPC Layer
**Goal**: Implement the core MCP protocol logic without changing the Runtime.

- **New Files**:
  - `src/dgm_mcp/mcp/jsonrpc.py`: Base classes for JSON-RPC 2.0 (Request, Response, Error).
  - `src/dgm_mcp/mcp/messages.py`: MCP specific message types (Initialize, ListTools, CallTool).
  - `src/dgm_mcp/mcp/server.py`: Core `MCPServer` class that handles the protocol state machine.
- **Estimated LOC**: ~400
- **Migration**: Purely additive. No impact on existing code.
- **Verification**: Unit tests for JSON-RPC serialization/deserialization.

---

## Phase 2: Tool Discovery & Schemas
**Goal**: Enable MCP clients to "see" and "describe" DGM-MCP tools.

- **New Files**:
  - `src/dgm_mcp/mcp/tools.py`: Logic to convert `BaseTool` instances into MCP Tool Definitions.
- **Modified Files**:
  - `src/dgm_mcp/tools/base_tool.py`: Add `get_schema()` abstract method.
  - `src/dgm_mcp/tools/*.py`: Implement `get_schema()` for all existing tools.
- **Estimated LOC**: ~300
- **Migration**: Updates to `BaseTool` interface.
- **Compatibility**: Old `execute` method remains untouched.
- **Rollback**: Schema methods are metadata-only; removing them doesn't break logic.

---

## Phase 3: Transport Layer (Stdio & SSE)
**Goal**: Allow external clients (Claude Desktop, Cursor) to connect.

- **New Files**:
  - `src/dgm_mcp/transports/base.py`: Interface for transports.
  - `src/dgm_mcp/transports/stdio.py`: Standard Input/Output transport.
  - `src/dgm_mcp/transports/sse.py`: Server-Sent Events transport (FastAPI compatible).
- **Modified Files**:
  - `src/dgm_mcp/bridge/mcp_server.py`: Refactor to use `sse.py`.
  - `src/dgm_mcp/main.py`: Add `dgm-mcp run-stdio` command.
- **Estimated LOC**: ~500
- **Migration**: Refactors the "Bridge" layer.
- **Compatibility**: FastAPI continues to run, but uses the standard protocol under the hood.
- **Rollback**: Keep a `LegacyMCPServer` class to switch back via config.

---

## Phase 4: Full Integration & Agent Bridging
**Goal**: Connect standard MCP tool calls to the `CognitiveAgent` and `Worker`.

- **Modified Files**:
  - `src/dgm_mcp/core/runtime.py`: Glue logic between `mcp.server` and `CognitiveAgent`.
  - `src/dgm_mcp/control/cognitive_agent.py`: Support for immediate (synchronous) tool execution vs. asynchronous planning.
- **Estimated LOC**: ~300
- **Migration**: Deep integration.
- **Rollback**: Revert `runtime.py` to previous version.

---

## Summary Table

| Phase | Duration | LOC (est) | Risk | Primary Files |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 3-4 days | 400 | Low | `mcp/jsonrpc.py`, `mcp/messages.py` |
| 2 | 2-3 days | 300 | Medium | `mcp/tools.py`, `tools/base_tool.py` |
| 3 | 5-7 days | 500 | High | `transports/stdio.py`, `transports/sse.py` |
| 4 | 4-5 days | 300 | Medium | `core/runtime.py`, `control/cognitive_agent.py` |

**Total Estimated Effort**: 14-19 working days (~3-4 weeks).
