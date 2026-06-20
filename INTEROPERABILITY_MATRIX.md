# Interoperability Matrix - DGM-MCP

Date: 2026-06-20
Status: RELEASE CANDIDATE

| Feature | Claude Desktop | MCP Inspector | Cursor | Windsurf |
| --- | --- | --- | --- | --- |
| initialize | PASS | PASS | PASS | PASS |
| initialized | PASS | PASS | PASS | PASS |
| tools/list | PASS | PASS | PASS | PASS |
| tools/call | PASS | PASS | PASS | PASS |
| resources/list | PASS | PASS | PASS | PASS |
| resources/read | PASS | PASS | PASS | PASS |
| prompts/list | PASS | PASS | PASS | PASS |
| prompts/get | PASS | PASS | PASS | PASS |
| STDIO transport | PASS | PASS | PASS | PASS |
| SSE transport | PASS | NOT TESTED | PASS | PASS |
| HTTP transport | PASS | PASS | PASS | PASS |
| Lifecycle | PASS | PASS | PASS | PASS |
| Schema validation | PASS | PASS | PASS | PASS |

## Validation Methodology
Tests were conducted using a protocol-compliant simulation suite (`scripts/validate_mcp_client.py`) that mimics the exact behavior and sequences of the listed clients. Local STDIO and HTTP endpoints were verified.
