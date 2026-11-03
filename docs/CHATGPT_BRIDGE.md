# DGM-MCP ChatGPT Bridge

This profile prepares DGM-MCP for an authenticated MCP bridge without changing the existing Claude Desktop or VS Code MCP entries.

## Local profile

Use `config/chatgpt-bridge.yaml` for the ChatGPT-facing profile. It enables:

- explicit allowed project directories;
- MCP authentication on HTTP/SSE transports;
- developer role with file read/write, patch write and Git status; no shell execution by default;
- high-risk Git/repo actions disabled by default;
- sanitized config and log resources;
- low worker count for older hardware.

The MCP API key must come from the environment. Do not write it to Git-tracked config files.

```powershell
$env:DGM_CONFIG_PATH = "config/chatgpt-bridge.yaml"
$env:DGM_MCP_API_KEY = "<set-a-local-secret>"
py -m dgm_mcp.main run-http
```

The HTTP MCP endpoint is:

```text
http://127.0.0.1:8003/mcp
```

Authenticate with either:

```text
Authorization: Bearer <set-a-local-secret>
```

or:

```text
X-DGM-Key: <set-a-local-secret>
```

## ChatGPT activation

For ChatGPT, use the official custom MCP server/plugin flow when it is available on the account. For a private local server, use OpenAI Secure MCP Tunnel and point the tunnel client at the local MCP server. Do not expose this endpoint directly to the public Internet.

## Permissions

The default `developer` role can:

- read and write files inside allowed paths;
- apply patch writes inside allowed paths;
- run allowlisted development commands;
- run `git status`.

The default `developer` role cannot:

- commit;
- clone repositories;
- initialize repositories;
- access paths outside `allowed_paths`;
- use unauthenticated HTTP/SSE MCP calls.

To authorize another project, add its absolute path to `allowed_paths` and restart the server.

## Shell execution boundary

The default developer role cannot call the shell. Shell execution is reserved for
the admin role and is additionally blocked unless mcp_high_risk_enabled is
explicitly enabled. Python and pip are not shell allowlist entries because they
can execute arbitrary code or install package hooks. The remaining command
allowlist is intentionally narrow.
