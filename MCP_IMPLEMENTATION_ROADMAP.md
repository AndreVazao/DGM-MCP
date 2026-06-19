# MCP_IMPLEMENTATION_ROADMAP.md

This roadmap tracks the transition from the custom bridge to a standard MCP server.

## Implemented So Far
- JSON-RPC request/response primitives.
- Tool registry and MCP adapter.
- STDIO transport with `initialize`, `tools/list`, and `tools/call`.
- Resources and prompts with `resources/list`, `resources/read`, `prompts/list`, and `prompts/get`.
- CLI command: `dgm-mcp run-stdio`.

## Next Phases
### Phase 5: Resources
Goal: expose logs, configs, and file contents as MCP resources.

### Phase 6: Prompts
Goal: expose reusable prompt templates through MCP.

### Phase 7: SSE Transport
Goal: add remote communication for web clients and integrations.

### Phase 8: Validation
Goal: validate the MCP flow end-to-end with Claude Desktop / MCP Inspector.

## Current Priorities
1. Improve tool schemas per tool instead of generic ones.
2. Add SSE transport for remote clients.
3. Harden stdio lifecycle and error handling.
4. Decide when the legacy bridge can be deprecated safely.

## Architectural Constraints
1. The Runtime and Tools stay protocol-agnostic.
2. MCP logic lives only in `src/dgm_mcp/mcp/`.
3. The adapter remains the only bridge between protocol and tool execution.
