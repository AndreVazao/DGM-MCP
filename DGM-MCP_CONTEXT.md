# STATUS: ARCHITECTURAL REFACTOR (v0.2.0-alpha)

# DGM-MCP CONTEXT

## Visão Geral
DGM-MCP é um ecossistema para engenharia de software assistida por IA, evoluindo para se tornar um Servidor MCP (Model Context Protocol) nativo e de alta performance.

## Filosofia
- **Segurança**: PathGuard e Auditoria em tempo real.
- **Protocolo**: Aderência total ao padrão MCP v1.0.
- **Desacoplamento**: O Runtime e as Ferramentas são agnósticos em relação ao protocolo de transporte.
- **Soberania**: Decisões críticas exigem aprovação humana.

## Nova Estrutura MCP (v0.2.0)
Estamos a migrar de uma API REST customizada para uma arquitetura de 8 fases:
1. **JSON-RPC Core**: Protocolo base.
2. **Tool Registry**: Descoberta dinâmica de ferramentas.
3. **Tool Invocation**: Execução via adapters.
4. **STDIO Transport**: Conectividade nativa para Claude Desktop/Cursor.
5. **Resources**: Acesso a dados (logs, configs).
6. **Prompts**: Templates reutilizáveis.
7. **SSE Transport**: Conectividade remota.
8. **Validation**: Testes oficiais com Claude Desktop.

## Componentes Chave

### Protocol Layer (mcp/)
- `jsonrpc.py`: Motor de mensagens.
- `tool_registry.py`: Catálogo de capacidades.
- `adapter.py`: Ponte entre o protocolo e a execução.

### Core (core/ & tools/)
- `Runtime`: Orquestrador de estado e segurança.
- `Tools`: Implementações atómicas (Git, FS, Shell, Patch).

### Security
- `PathGuard`: Sandbox de sistema de ficheiros.
- `AuditLogger`: Rastreabilidade total.

## Status Atual
- **Fase 1-2 em progresso**: Definição de schemas e core JSON-RPC.
- **Infraestrutura**: Multi-LLM (Claude, GPT, Gemini, etc) está operacional no Core.
- **Objetivo Imediato**: Fazer o Claude Desktop listar as ferramentas do DGM-MCP via STDIO.

## Como Contribuir / Usar
1. Seguir o `MCP_IMPLEMENTATION_ROADMAP.md`.
2. Garantir que as novas Tools definem o seu `inputSchema` no Registry.
3. Não introduzir lógica MCP dentro das classes de Tool.

---

## Histórico de Versões
- **v0.1.5**: Multi-LLM, Dashboard, Async Worker.
- **v0.2.0 (Alpha)**: Início da transição para MCP Nativo (Standard).
