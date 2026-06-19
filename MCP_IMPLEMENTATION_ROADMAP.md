# MCP_IMPLEMENTATION_ROADMAP.md

This roadmap tracks the transition from the custom bridge to a standard MCP server.

## Implemented So Far
- JSON-RPC request/response primitives.
- Tool registry and MCP adapter.
- STDIO transport with `initialize`, `tools/list`, and `tools/call`.
- Resources and prompts with `resources/list`, `resources/read`, `prompts/list`, and `prompts/get`.
- Constrained tool schemas with enums and `additionalProperties: false`.
- SSE transport with `/mcp/sse` and `/mcp/message`.
- Lifecycle support for `shutdown` and JSON-RPC notifications.
- Streamable HTTP transport with `/mcp`.
- CLI command: `dgm-mcp run-stdio`.
- CLI command: `dgm-mcp run-sse`.
- CLI command: `dgm-mcp run-http`.

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
1. Validate with a real MCP client.
2. Add richer resources and prompt templates.
3. Decide when the legacy bridge can be deprecated safely.

## Architectural Constraints
1. The Runtime and Tools stay protocol-agnostic.
2. MCP logic lives only in `src/dgm_mcp/mcp/`.
3. The adapter remains the only bridge between protocol and tool execution.
