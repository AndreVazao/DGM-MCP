# DGM-MCP CONTEXT

## Visão Geral
DGM-MCP é o sucessor evoluído do DGM-HUB. É um servidor MCP (Model Control Protocol) local, focado em dar capacidades reais de engenharia de software a LLMs de forma segura e controlada.

## Filosofia
- Segurança em primeiro lugar
- Controle humano final (approvals)
- Transparência total (logs e explicações)
- Foco em qualidade e boas práticas de engenharia
- Separação clara entre reasoning e execução

## Fluxo Principal
1. LLM envia pedido via MCP
2. TaskManager recebe e prioriza
3. CognitiveAgent analisa e cria plano
4. Worker executa o plano passo a passo usando Tools
5. Quando necessário, pede aprovação humana
6. Executa alterações apenas após aprovação

## Componentes Chave

### Core
- ConfigManager
- Runtime (orquestrador central)
- Registry (tools e agents)

### Security
- PathGuard (restrição de pastas permitidas)
- Permission System

### Control
- TaskManager
- Worker
- CognitiveAgent (reasoning + planning)

### Tools
- FilesystemTool
- GitTool
- ShellTool (cmd/powershell)
- TestRunnerTool
- PatchTool

## Status Atual
- Fase inicial de fundação (MVP)
- Foco atual: Base sólida + MCP Server funcional

## Próximos Milestones
1. MCP Server básico funcional
2. Sistema de aprovação humana
3. CognitiveAgent v1 (bom reasoning)
4. Integração com Claude Desktop
5. Memory / Long-term state

## Status Atual (Fase 8)
- Estrutura modular sólida
- Security Layer (PathGuard)
- Tools: Filesystem, Git, Shell, Patch
- Sistema de aprovação humana
- Worker + CognitiveAgent funcionais (com loop de processamento)
- MCP Server com FastAPI
- CLI funcional (dgm-mcp start, tools, status, test)
- Sistema de Memória persistente

## Como Ligar com Ferramentas Externas (Claude Desktop / Cursor / Windsurf)

### Opção Recomendada: MCP Server
1. Inicia o servidor: `dgm-mcp start`
2. No Claude Desktop / Cursor, configura o MCP para:
   - URL: `http://127.0.0.1:8000/mcp/task`
   - Método: POST
   - Envia JSON com `"description": "tua tarefa aqui"`

### Exemplo de prompt para Claude:
```
Usa o DGM-MCP para:
1. Analisar a pasta atual
2. Criar um novo ficheiro chamado example.py
3. Fazer commit das alterações
Aprova todas as ações importantes.
```

## Próximos Passos (Fase 9+)
- Sistema completo de Patches + Diff
- Suporte a múltiplos LLMs
- Interface Web simples
- Logging avançado + observabilidade

## Fase 11 Status
- LLM integration completa (ChatGPT, Claude, Grok, Gemini, Ollama)
- Advanced Patch + Preview System
- Centralized Logging
- Plan Execution Engine

## Integração com LLMs Externos (Recomendado)

### Claude Desktop / Cursor / Windsurf
- URL: `http://127.0.0.1:8000/mcp/task`
- Método: `POST`
- Body JSON: `{"description": "tua tarefa", "session_id": "opcional"}`

### VS Code + Continue.dev ou Aider
Podes configurar o MCP como tool customizada.

### Ollama Local
Funciona sem API key.

## Integração com LLMs Externos (Recomendado)

### Claude Desktop / Cursor / Windsurf
- URL: `http://127.0.0.1:8000/mcp/task`
- Método: `POST`
- Body JSON: `{"description": "tua tarefa", "session_id": "opcional"}`

### VS Code + Continue.dev ou Aider
Podes configurar o MCP como tool customizada.

### Ollama Local
Funciona sem API key.

## Fase 18 — Status Atual (v0.1.5)

- Multi-LLM completo (ChatGPT, Claude, Grok, Gemini, Ollama)
- Sistema de aprovação rico com preview
- Worker em thread
- Observability / Dashboard
- Sessões de contexto
- Patch system avançado

**Pronto para integração real com Claude Desktop, Cursor, VS Code, etc.**

## Checklist de Produção (v0.1.4)

- [x] Dynamic LLM Detection (Fase 18)
- [x] PathGuard + Security
- [x] Sistema de aprovação humana
- [x] Worker em thread
- [x] Patch Tool com preview
- [x] Logging rico
- [x] CLI completa (start, test, tools, dashboard)
- [x] Testes básicos
- [ ] Integração real com Claude Desktop (testar)
- [ ] Melhor error recovery
- [ ] Logging para ficheiro

## Checklist de Produção (v0.1.5)

- [x] Dynamic LLM Detection (Fase 18)
- [x] PathGuard + Security
- [x] Sistema de aprovação humana
- [x] Worker em thread
- [x] Patch Tool com preview
- [x] Logging rico
- [x] CLI completa (start, test, tools, dashboard)
- [x] Testes básicos
- [ ] Integração real com Claude Desktop (testar)
- [ ] Melhor error recovery
- [ ] Logging para ficheiro

## Fase 18 — Status Atual (Production Ready)
- Dynamic LLM Detection e Auto-Registration.
- Comando `status` completo para diagnóstico.
- Documentação de uso real com Claude Desktop, Cursor, etc.
