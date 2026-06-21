# Changelog

All notable changes to this project will be documented in this file.

## [0.2.0] - 2026-06-21

### Added
- Native Model Context Protocol (MCP) support (2025-06-18 specification).
- Transports: STDIO, SSE, and Streamable HTTP.
- Official certification for Claude Desktop, Cursor, Windsurf, and MCP Inspector.
- `PathGuard` for secure filesystem access.
- `AuditLogger` for JSON-based activity logging.
- Integrated Human-in-the-Loop approval system.
- Resources (dgm://) and Prompts support.
- Native metrics and health endpoints.
- Robust session management.

### Changed
- Refactored core runtime for production readiness.
- Improved P99 latency to < 110ms.
- Deprecated legacy bridge (scheduled for removal in v0.3.0).

### Fixed
- Protocol handshake inconsistencies.
- JSON-RPC error handling.
- Unused imports and linting issues.

## [0.1.5] - 2025-06-14
- Pre-release with initial audit logging and security hardening.

## [0.1.0] - 2025-06-01
- Initial release.
