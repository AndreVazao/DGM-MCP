# DGM-MCP v0.2.0 Release Blockers

## CRITICAL
- **Version Mismatch**: `pyproject.toml` (0.1.5) and `__init__.py` (0.1.0) do not match the announced version in `README.md` (0.2.0).
- **Legal/Compliance**: Missing `LICENSE` file. This is mandatory for any public release.

## HIGH
- **Documentation**: Missing `CHANGELOG.md`, `SECURITY.md`, and `CONTRIBUTING.md`.
- **Quality**: 24 linting errors (unused imports, bare excepts) which indicate code hygiene issues.

## MEDIUM
- **Test Coverage**: 16 modules lack dedicated unit tests.
- **Git Hygiene**: No Git tags found (`v0.2.0` should be tagged).

## LOW
- **Inconsistency**: `filesystem_tool` and `git_tool` logic in `adapter.py` schema vs actual implementation should be cross-verified for parameter alignment.
