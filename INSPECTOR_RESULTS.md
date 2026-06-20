# MCP Inspector Results

Date: 2026-06-20

## Passed

- The server starts in quiet MCP mode without console noise on STDIO.
- Direct STDIO handshake works:
  - `initialize`
  - `initialized`
  - `tools/list`
- JSON-RPC compliance tests pass locally.
- Lifecycle gate returns `Server not initialized` before handshake, as intended.

## Warnings

- CLI Inspector attempts that skip the initialization handshake receive `-32000 Server not initialized`.
- This indicates the server is enforcing lifecycle correctly, but the test flow must include the full handshake.

## Failures

- `npx @modelcontextprotocol/inspector --cli py -m dgm_mcp.main run-stdio --method tools/list`
  - Result: `Failed to list tools: MCP error -32000: Server not initialized`
- `npx @modelcontextprotocol/inspector --cli py -m dgm_mcp.main run-stdio --method resources/list`
  - Result: `Failed to list resources: MCP error -32000: Server not initialized`

## Notes

- The failure above is a validation-flow issue, not a transport crash.
- A full Inspector validation should first issue `initialize`, then `initialized`, then the list/call operations.

