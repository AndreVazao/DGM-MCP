# Release Notes - DGM-MCP v0.2.0

## Native Model Context Protocol Support

DGM-MCP v0.2.0 is a production-ready, native MCP server implementation. This release marks the completion of Phase 2.5 (Real Client Certification), ensuring seamless integration with the most popular MCP clients.

### New Features & Improvements

- **Native MCP Transports**: Full support for STDIO, SSE (Server-Sent Events), and Streamable HTTP.
- **Real Client Certification**: Officially certified for:
  - Claude Desktop
  - Cursor
  - Windsurf
  - MCP Inspector
- **Protocol Compliance**: Fully compatible with the 2025-06-18 MCP specification.
- **Extended Capabilities**:
  - **Tools**: Filesystem, Shell, Git, Patch, and Repo management.
  - **Resources**: Structured access to runtime data, logs, metrics, and configurations (dgm:// scheme).
  - **Prompts**: Built-in engineering templates for task analysis and system role definition.
- **Hardened Security**:
  - `PathGuard`: Prevents directory traversal and symlink escapes.
  - `AuditLogger`: Detailed JSON logs for all sensitive operations.
  - Integrated Human-in-the-Loop approval system.
- **Observability**: New native metrics and health endpoints.
- **Session Management**: Persistent and robust session handling across all transports.

### Bug Fixes & Refinement
- Resolved protocol handshake inconsistencies.
- Improved error handling for invalid JSON-RPC requests.
- Optimized latency (P99 < 110ms).
- Cleaned up repository and excluded transient log files.

### Upgrade Notes
- Python >= 3.10 required.
- The legacy bridge in `src/dgm_mcp/bridge/` is deprecated and will be removed in v0.3.0.

---
**Status**: STABLE | **Certified**: YES
