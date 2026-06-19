# MCP_TOOL_SCHEMAS.md

This document defines the JSON Schemas for all DGM-MCP tools to ensure compatibility with the `tools/list` and `tools/call` methods.

## 1. Filesystem Tool (`filesystem`)

```json
{
  "name": "filesystem",
  "description": "Read, write and manipulate files and folders",
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
  }
}
```

---

## 2. Git Tool (`git`)

```json
{
  "name": "git",
  "description": "Execute Git commands safely",
  "inputSchema": {
    "type": "object",
    "properties": {
      "action": {
        "type": "string",
        "enum": ["status", "commit"],
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
  }
}
```

---

## 3. Shell Tool (`shell`)

```json
{
  "name": "shell",
  "description": "Execute allowed system commands (python, pip, pytest, etc.)",
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
  }
}
```

---

## 4. Patch Tool (`patch`)

```json
{
  "name": "patch",
  "description": "Apply precision edits to files using SEARCH/REPLACE blocks",
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

```json
{
  "name": "repo",
  "description": "General repository management (init, clone)",
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
