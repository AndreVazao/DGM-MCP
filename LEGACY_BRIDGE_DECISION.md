# LEGACY BRIDGE RETIREMENT ANALYSIS

## Current State
The legacy bridge in `src/dgm_mcp/bridge/` provides a custom FastAPI-based interface for task creation and execution.

## Findings
- The new MCP native servers (STDIO, HTTP, SSE) now cover all functionality of the legacy bridge.
- The native MCP servers are more standard, secure (schema validation), and interoperable.
- `dgm-mcp start` still defaults to the legacy bridge.

## Decision
- **Status**: DEPRECATED
- **Plan**:
  - In v0.2.0, keep the bridge for backward compatibility but mark as deprecated in logs.
  - In v0.3.0, remove the bridge entirely.
  - Update `dgm-mcp start` to encourage using `run-stdio` or `run-http`.

## Recommendation
Transition all users to MCP Native transports immediately.
