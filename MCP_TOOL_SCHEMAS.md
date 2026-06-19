# MCP_TOOL_SCHEMAS.md

This document defines the enriched JSON Schemas for DGM-MCP tools, following the latest MCP standards.

## 1. Filesystem Tool (`filesystem`)
**Title**: Filesystem Operations
**Description**: Securely read, write and manipulate files and folders within allowed paths.

```json
{
  "name": "filesystem",
  "title": "Filesystem Operations",
  "description": "Read and write files within the sandbox.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "action": {
        "type": "string",
        "enum": ["read", "write"],
        "description": "The action to perform"
      },
      "path": {
        "type": "string",
        "description": "The target file or directory path"
      },
      "content": {
        "type": "string",
        "description": "Content for the write action"
      }
    },
    "required": ["action", "path"]
  },
  "outputSchema": {
    "type": "object",
    "properties": {
      "success": { "type": "boolean" },
      "message": { "type": "string" },
      "data": { "type": "object" }
    }
  }
}
```

---

## 2. Git Tool (`git`)
**Title**: Git Repository Operations
**Description**: Execute Git commands safely to manage version control.

```json
{
  "name": "git",
  "title": "Git Operations",
  "description": "Safe git operations (status, commit, log).",
  "inputSchema": {
    "type": "object",
    "properties": {
      "action": {
        "type": "string",
        "enum": ["status", "commit", "log"],
        "description": "Git action"
      },
      "repo_path": {
        "type": "string",
        "default": ".",
        "description": "Path to the repository"
      },
      "message": {
        "type": "string",
        "description": "Commit message"
      }
    },
    "required": ["action"]
  },
  "outputSchema": {
    "type": "object"
  }
}
```

---

## 3. Shell Tool (`shell`)
**Title**: System Shell Execution
**Description**: Execute whitelisted system commands (python, pip, pytest).

```json
{
  "name": "shell",
  "title": "Shell Execution",
  "description": "Execute allowed commands in a secure shell environment.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "command": {
        "type": "string",
        "description": "The command string to execute"
      },
      "cwd": {
        "type": "string",
        "default": ".",
        "description": "Working directory"
      },
      "timeout": {
        "type": "integer",
        "default": 30,
        "description": "Execution timeout in seconds"
      }
    },
    "required": ["command"]
  },
  "outputSchema": {
    "type": "object"
  }
}
```

---

## 4. Patch Tool (`patch`)
**Title**: Precision File Patching
**Description**: Apply surgical edits using SEARCH/REPLACE blocks.

```json
{
  "name": "patch",
  "title": "File Patching",
  "description": "Apply SEARCH/REPLACE patches to files.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "path": {
        "type": "string",
        "description": "File path to patch"
      },
      "patch_data": {
        "type": "string",
        "description": "The patch content with SEARCH/REPLACE markers"
      }
    },
    "required": ["path", "patch_data"]
  }
}
```

---

## 5. Repo Tool (`repo`)
**Title**: Repository Management
**Description**: High-level repository lifecycle operations (init, clone).

```json
{
  "name": "repo",
  "title": "Repo Management",
  "description": "Initialize or clone repositories.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "action": {
        "type": "string",
        "enum": ["init", "clone"],
        "description": "Repo action"
      },
      "path": {
        "type": "string",
        "description": "Target path"
      },
      "url": {
        "type": "string",
        "description": "Repository URL for clone action"
      }
    },
    "required": ["action", "path"]
  }
}
```
