# DGM-MCP ChatGPT bridge security recovery — 2026-11-03

**Branch:** `feat/chatgpt-bridge-rbac-2026-11-03`

**Base:** latest fetched `origin/main` at `bc6feae`

## Recovered local work

The previously uncommitted local bridge work is preserved on this branch:
- configurable ChatGPT-facing YAML profile;
- HTTP/SSE bearer authentication;
- constant-time key comparison;
- role-based tool and action authorization;
- optional role-header support, disabled in the profile;
- resource secret sanitization;
- maximum file-write size;
- filesystem write limit propagation;
- access-policy tests and operator documentation.

No API key or credential value is stored in the tracked profile. The MCP key must be supplied through the environment.

## Additional hardening

The original local draft allowed the developer role to execute shell commands and included `python` and `pip` in the shell allowlist. That was too permissive: Python can execute arbitrary code and pip can execute package installation hooks.

The branch now:
- removes shell execution from the default developer role;
- reserves shell execution for admin;
- treats shell execution as high-risk and requires explicit `mcp_high_risk_enabled`;
- removes `python` and `pip` from the shell allowlist;
- retains the narrow command allowlist for explicitly enabled admin operations;
- tests HTTP and SSE authentication, secret redaction, role-header non-escalation, file path boundaries, write limits and shell gates.

## Validation

- Full DGM-MCP pytest suite: **59 passed**.
- No API key was added to the repository.
- The bridge profile keeps role-header elevation disabled and high-risk operations disabled by default.

## Scope

DGM-MCP remains an independent MCP project. This branch does not merge it into DGM-MAT or grant it authority over DGM-HUB. Any connected client must still explicitly configure the profile and provide a local secret.
