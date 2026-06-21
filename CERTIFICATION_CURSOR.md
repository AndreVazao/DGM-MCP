# CERTIFICATION: CURSOR (v0.2.0)

## Status: CERTIFIED

## Configuration Used
- **Type**: STDIO
- **Command**: `python -m dgm_mcp.main run-stdio`
- **Env**: `PYTHONPATH=src`

## Checklist Results

### Transport
- [x] STDIO connection - **PASS**

### Features
- [x] Tool discovery - **PASS**
- [x] Successful tool execution - **PASS**
- [x] Resource access - **PASS**

## Observations
- Cursor correctly identifies all 5 primary tools.
- Non-interactive shell execution is stable.
- Resource reading (`dgm://runtime`) provides context for the AI.
