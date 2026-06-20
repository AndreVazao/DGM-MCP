# Validation Guide

This guide records the local validation flow for Claude Desktop, MCP Inspector, and direct transport checks.

## Claude Desktop

Use this configuration:

```json
{
  "mcpServers": {
    "dgm-mcp": {
      "command": "py",
      "args": [
        "-m",
        "dgm_mcp.main",
        "run-stdio"
      ]
    }
  }
}
```

Recommended startup checks:

1. `initialize`
2. `initialized`
3. `tools/list`
4. `tools/call`
5. `resources/list`
6. `resources/read`
7. `prompts/list`
8. `prompts/get`
9. `shutdown`

## MCP Inspector

Observed usage:

```bash
npx @modelcontextprotocol/inspector --cli py -m dgm_mcp.main run-stdio --method tools/list
```

Local outcome:
- The server responded with `Server not initialized` when the Inspector attempted `tools/list` without a prior `initialize` + `initialized` handshake.
- This is expected with the current lifecycle hardening.

## Direct Local Check

STDIO handshake validated locally with:

1. `initialize`
2. `initialized`
3. `tools/list`

Result:
- The server returns JSON-RPC responses correctly.
- No non-protocol console noise is emitted in quiet MCP mode.
- Local full-suite test status: `33 passed`.
