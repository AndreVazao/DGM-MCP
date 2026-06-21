# MCP INSPECTOR CERTIFICATION CHECKLIST

## Transports
- [ ] STDIO (mcp-inspector -- python -m dgm_mcp.main run-stdio)
- [ ] SSE (mcp-inspector http://127.0.0.1:8002/mcp/sse)
- [ ] HTTP (mcp-inspector http://127.0.0.1:8003/mcp)

## Validation
- [ ] Schema validation for all tools
- [ ] Error handling (Method not found, Invalid params)
- [ ] Pagination support (if implemented)
