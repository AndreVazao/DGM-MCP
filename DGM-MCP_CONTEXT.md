# STATUS: MCP TRANSITION IN PROGRESS

# DGM-MCP CONTEXT

## Visão Geral
DGM-MCP está a evoluir de um sistema de controlo para LLMs com bridge customizado para um servidor MCP nativo, mantendo o core agnóstico do protocolo.

## Filosofia
- **Segurança**: PathGuard e AuditLogger continuam no core.
- **Protocolo**: A camada MCP fica isolada do Runtime e das Tools.
- **Desacoplamento**: O core não conhece JSON-RPC nem transport.
- **Soberania**: A execução continua sujeita a validações e limites do runtime.

## Estado Atual
- **Core legado funcional**: Runtime, tools, web e control continuam operacionais.
- **MCP fase 1-2 implementada**: JSON-RPC básico, registry de tools e adapter.
- **STDIO em curso**: comando `dgm-mcp run-stdio` disponível para teste local.
- **Testes locais**: suíte principal verde no ambiente atual.

## MCP Implementado
### `src/dgm_mcp/mcp/`
- `jsonrpc.py`: requests, responses e erros JSON-RPC.
- `tool_registry.py`: catálogo de ferramentas exposto ao protocolo.
- `adapter.py`: ponte entre tool runtime e chamadas MCP.
- `stdio.py`: servidor MCP via STDIO com `initialize`, `tools/list` e `tools/call`.

## Próximos Passos
1. Expandir o suporte a `resources` e `prompts`.
2. Melhorar schemas de input para cada tool.
3. Adicionar validação oficial com MCP Inspector / Claude Desktop.
4. Planear substituição gradual do bridge antigo quando o caminho MCP estiver estável.

## Notas Operacionais
- O `pytest.ini` foi adicionado para incluir `src/` automaticamente nos testes.
- O `ShellTool` foi ajustado para funcionar no Windows nos testes locais.
- O `tools/call` usa o adapter e preserva a execução via Runtime.

