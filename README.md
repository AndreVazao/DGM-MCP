# DGM-MCP (v0.2.0)

**Sistema de Controlo para LLMs** - Transforma Claude, ChatGPT, Grok, Gemini ou Ollama num engenheiro de software real, com segurança e aprovação humana.

## STATUS: CERTIFIED (v0.2.0)

DGM-MCP v0.2.0 é um servidor MCP nativo totalmente certificado e pronto para produção.

## Características Principais
- **MCP Nativo**: Suporte completo para STDIO, SSE e HTTP streamable.
- **Interoperabilidade**: Validado e Certificado com Claude Desktop, Cursor, Windsurf e MCP Inspector.
- **Segurança**: `PathGuard` e `AuditLogger` integrados em todas as chamadas.
- **Recursos e Prompts**: Exposição de logs, métricas e templates de engenharia via MCP.

## Relatórios de Certificação
- [Resumo da Certificação](./CERTIFICATION_SUMMARY.md)
- [Relatório Claude Desktop](./CERTIFICATION_CLAUDE_DESKTOP.md)
- [Relatório MCP Inspector](./CERTIFICATION_MCP_INSPECTOR.md)
- [Relatório Cursor](./CERTIFICATION_CURSOR.md)
- [Relatório Windsurf](./CERTIFICATION_WINDSURF.md)
- [Relatório de Interoperabilidade (Antigo)](./INTEROPERABILITY_CERTIFICATION_REPORT.md)

## Como Usar

### 1. Instalação
```bash
git clone https://github.com/AndreVazao/DGM-MCP.git
cd DGM-MCP
pip install -e .
python scripts/init.py
```

### 2. Executar Servidor MCP
Modo STDIO (para Claude Desktop):
```bash
dgm-mcp run-stdio
```

Modo SSE (para integrações web):
```bash
dgm-mcp run-sse
```

Modo HTTP:
```bash
dgm-mcp run-http
```

### 3. Dashboard e Controlo
```bash
dgm-mcp web
```

## LLMs Suportados
- Claude, ChatGPT, Grok, Gemini, Ollama.

## Licença
MIT
