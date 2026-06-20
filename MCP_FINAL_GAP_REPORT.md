# MCP Final Gap Report

Date: 2026-06-20

## CRITICAL

- Claude Desktop not validated in a live session.
- MCP Inspector UI mode not validated in a live session.
- Cursor not validated in a live session.
- Windsurf not validated in a live session.
- Repository main branch is synchronized with the compliance hardening commit history.

## HIGH

- Streamable HTTP has been hardened, but full client interoperability is still unconfirmed.
- HTTP session behavior was implemented, but only locally verified.
- Lifecycle gating is strict; clients must follow `initialize` -> `initialized` before discovery.

## MEDIUM

- No pagination on `tools/list`, `resources/list`, `prompts/list`.
- Resource metadata is minimal.
- Prompt argument schemas are still simple.

## LOW

- Log noise and deprecation warnings remain in the test environment.
- README and validation docs could be consolidated once live client validation is completed.

## Actions Needed

1. Run a real Claude Desktop session against STDIO and capture results.
2. Run MCP Inspector UI mode against both STDIO and HTTP and capture results.
3. Validate Cursor against the same local server configuration.
4. Validate Windsurf against the same local server configuration.
5. Only after those checks, decide whether to retire the legacy bridge.

