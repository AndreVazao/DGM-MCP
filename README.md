# DGM-MCP

**Motor de Controlo para LLMs** — Permite que Claude, ChatGPT, Grok, Gemini ou Ollama façam engenharia de software real no teu computador de forma **segura**.

## Funcionalidades
- Suporte multi-LLM (Claude, GPT-4o, Grok, Gemini, Ollama local)
- PathGuard + aprovação humana obrigatória
- Worker em background
- Patch preview com diff
- MCP Server para integração com Claude Desktop / Cursor

## Como começar

```bash
git clone https://github.com/AndreVazao/DGM-MCP.git
cd DGM-MCP
python scripts/init.py
dgm-mcp dashboard
dgm-mcp start
```

## LLMs Suportados
- **Claude** (melhor qualidade atual)
- **ChatGPT / Codex**
- **Grok**
- **Gemini**
- **Ollama** (local)

## Próximos Passos
- Interface Web
- Suporte a streaming em tempo real
- Mais ferramentas (Docker, Database, etc.)
- Modo agente autónomo
