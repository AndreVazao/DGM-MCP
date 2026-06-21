# Security Policy

## Supported Versions

We currently provide security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 0.2.x   | :white_check_mark: |
| < 0.2.0 | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability, please report it via the project's issue tracker or contact the maintainers directly.

We take security seriously and will investigate all reports promptly. Please provide a detailed description of the vulnerability, including steps to reproduce it if possible.

### Security Features

- **PathGuard**: Restricts filesystem access to allowed directories.
- **Audit Logging**: All tool executions are logged with detailed metadata.
- **Human Approval**: Critical actions require explicit human confirmation.
