# Contributing to DGM-MCP

Thank you for your interest in contributing to DGM-MCP!

## Development Setup

1. Clone the repository.
2. Install dependencies: `pip install -e .`
3. Run tests: `pytest`
4. Run linting: `ruff check .`

## Code Style

- We use `ruff` for linting and formatting.
- Ensure all tests pass before submitting a PR.
- Follow the existing architectural patterns (PathGuard, AuditLogger, etc.).

## PR Process

1. Create a new branch for your feature or bugfix.
2. Commit your changes with descriptive messages.
3. Submit a PR against the `main` branch.
4. Ensure all CI checks pass.
