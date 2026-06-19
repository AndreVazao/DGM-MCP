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
- **MCP fase 1-8 parcialmente concluída**: JSON-RPC, tools, resources, prompts, SSE e HTTP streamable já expostos.
- **STDIO, SSE e HTTP**: comandos `dgm-mcp run-stdio`, `dgm-mcp run-sse` e `dgm-mcp run-http` disponíveis para teste local.
- **Testes locais**: suíte principal verde no ambiente atual.

## MCP Implementado
### `src/dgm_mcp/mcp/`
- `jsonrpc.py`: requests, responses e erros JSON-RPC.
- `tool_registry.py`: catálogo de ferramentas exposto ao protocolo.
- `adapter.py`: ponte entre tool runtime e chamadas MCP.
- `resources.py`: resources e prompts expostos pelo servidor MCP.
- `stdio.py`: servidor MCP via STDIO com `initialize`, `tools/list`, `tools/call`, `resources/list`, `resources/read`, `prompts/list` e `prompts/get`.
- `sse.py`: transporte SSE com endpoint de stream e endpoint de mensagens MCP.
- `http.py`: transporte HTTP streamable com endpoint MCP oficial.
- Schemas de tools já estão mais restritos, com enums e `additionalProperties: false`.
- O lifecycle já trata `shutdown` e ignora notificações sem `id`.

## Próximos Passos
1. Adicionar validação oficial com MCP Inspector / Claude Desktop.
2. Expandir resources e prompts com dados mais ricos.
3. Validar o transport e o lifecycle com um cliente MCP real.
4. Planear substituição gradual do bridge antigo quando o caminho MCP estiver estável.

## Notas Operacionais
- O `pytest.ini` foi adicionado para incluir `src/` automaticamente nos testes.
- O `ShellTool` foi ajustado para funcionar no Windows nos testes locais.
- O `tools/call` usa o adapter e preserva a execução via Runtime.
- `resources` e `prompts` agora devolvem config, logs e templates úteis para inspeção.
