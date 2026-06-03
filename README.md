# DGM-MCP

**DGM-MCP** (Model Control Protocol Server) é um runtime local seguro que permite a Large Language Models (como Claude, GPT-4o, etc.) executar engenharia de software no teu computador com controlo humano explícito.

## Objetivo
Permitir que um LLM trabalhe como um engenheiro de software real: analisa, planeia, escreve código, faz git, testes, etc., sempre com aprovação humana antes de alterações críticas.

## Principais Funcionalidades
- MCP Server (compatível com Claude Desktop / Cursor / Windsurf)
- Runtime seguro com PathGuard
- Sistema de tarefas + aprovação humana
- Ferramentas avançadas (Filesystem, Git, Shell, Testing, etc.)
- Arquitetura modular e extensível

## Como Usar

```bash
pip install -e .
dgm-mcp start
```

## Estrutura
- `src/dgm_mcp/` → Código principal
- `DGM-MCP_CONTEXT.md` → Contexto completo do projeto
