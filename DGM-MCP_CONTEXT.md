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
