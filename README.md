# STATUS: PRODUCTION BETA

# DGM-MCP

**Sistema de Controlo para LLMs** — Transforma Claude, ChatGPT, Grok, Gemini ou Ollama num engenheiro de software real, com segurança e aprovação humana.

## Como Usar com Diferentes Ferramentas

### 1. Claude Desktop / Cursor / Windsurf
Inicia o servidor:
```bash
dgm-mcp start
```
Configura o MCP com URL: `http://127.0.0.1:8000/mcp/task`

### 2. VS Code + Continue.dev
Configura o `config.json` do Continue para usar o endpoint do DGM-MCP.

### 3. Aider ou outras ferramentas
Usa o MCP Server como backend.

### 4. Modo CLI direto
```bash
dgm-mcp status
dgm-mcp test
dgm-mcp web
```

O sistema **detecta automaticamente** quais LLMs tens configurados.

## Utilizar com Grok (xAI)

1. Obtém a tua API key em https://console.x.ai
2. Adiciona no `.env`:
   ```env
   XAI_API_KEY=xai-...
   ```
3. O DGM-MCP vai detetar automaticamente o Grok e colocá-lo como prioridade.

Podes forçar o uso do Grok com:
```bash
dgm-mcp start --llm Grok
```

## Instalação Rápida

```bash
git clone https://github.com/AndreVazao/DGM-MCP.git
cd DGM-MCP
python scripts/init.py
dgm-mcp dashboard
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
