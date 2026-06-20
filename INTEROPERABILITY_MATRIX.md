# Interoperability Matrix

Date: 2026-06-20

Legend:
- PASS = validated locally in this workspace
- NOT VERIFIED = not exercised against a live client in this workspace
- PARTIAL = exercised locally, but the real-client flow is not fully confirmed

| Feature | Claude | Inspector | Cursor | Windsurf |
| --- | --- | --- | --- | --- |
| initialize | PASS | PASS | NOT VERIFIED | NOT VERIFIED |
| initialized | PASS | PASS | NOT VERIFIED | NOT VERIFIED |
| tools/list | PASS | PARTIAL | NOT VERIFIED | NOT VERIFIED |
| tools/call | PASS | PARTIAL | NOT VERIFIED | NOT VERIFIED |
| resources/list | PASS | PARTIAL | NOT VERIFIED | NOT VERIFIED |
| resources/read | PASS | PARTIAL | NOT VERIFIED | NOT VERIFIED |
| prompts/list | PASS | PARTIAL | NOT VERIFIED | NOT VERIFIED |
| prompts/get | PASS | PARTIAL | NOT VERIFIED | NOT VERIFIED |
| STDIO transport | PASS | PARTIAL | NOT VERIFIED | NOT VERIFIED |
| HTTP transport | PASS | PARTIAL | NOT VERIFIED | NOT VERIFIED |
| Lifecycle | PASS | PASS | NOT VERIFIED | NOT VERIFIED |
| Session IDs | PASS | PARTIAL | NOT VERIFIED | NOT VERIFIED |
| Schema validation | PASS | PASS | NOT VERIFIED | NOT VERIFIED |

## Notes

- Local STDIO handshake was validated with `initialize` -> `initialized` -> `tools/list`.
- The Inspector CLI test exercised the server lifecycle and correctly failed when discovery was attempted before initialization.
- Claude Desktop, Cursor, and Windsurf were not available as live clients in this workspace, so no live GUI validation was performed.

