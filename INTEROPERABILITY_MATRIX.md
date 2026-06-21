# Interoperability Matrix - DGM-MCP

Date: 2026-06-21
Status: CERTIFIED (v0.2.0)

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
| SSE transport | PASS | PASS | PASS | PASS |
| HTTP transport | PASS | PASS | PASS | PASS |
| Lifecycle | PASS | PASS | PASS | PASS |
| Schema validation | PASS | PASS | PASS | PASS |

## Validation Methodology
Tests were conducted using real MCP clients and the automated certification suite (`certification/certify_*.py`). All clients are now officially **CERTIFIED** for DGM-MCP v0.2.0.
