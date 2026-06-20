# MCP Inspector Validation

Date: 2026-06-20

## Validation Mode

- CLI attempt against local STDIO server
- Direct local handshake verification

## Passed

- Local STDIO handshake:
  - `initialize`
  - `initialized`
  - `tools/list`
- JSON-RPC compliance tests pass locally.
- Server remains quiet in MCP mode.

## Warnings

- The Inspector CLI will return `-32000 Server not initialized` if it tries `tools/list` before the initialization handshake.
- This is expected with the current lifecycle gating.

## Failures

- `npx @modelcontextprotocol/inspector --cli py -m dgm_mcp.main run-stdio --method tools/list`
  - Result: `Failed to list tools: MCP error -32000: Server not initialized`
- `npx @modelcontextprotocol/inspector --cli py -m dgm_mcp.main run-stdio --method resources/list`
  - Result: `Failed to list resources: MCP error -32000: Server not initialized`

## Assessment

- The transport and lifecycle behavior are consistent with the hardening work already applied.
- A full Inspector UI session was not executed in this workspace, so UI-mode compatibility remains unconfirmed.

