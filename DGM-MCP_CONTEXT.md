# STATUS: CERTIFIED (v0.2.0)

# DGM-MCP CONTEXT

## Visão Geral
DGM-MCP completou a transição para um servidor MCP nativo certificado (Fase 2.5). O sistema está congelado para novas funcionalidades e focado em estabilidade.

## Estado Atual (v0.2.0)
- **Certificação**: Interoperabilidade validada com os principais clientes MCP.
- **Protocolo**: Handshake, lifecycle e tratamentos de erro JSON-RPC 2.0 endurecidos.
- **Transports**: STDIO, SSE e HTTP operacionais.
- **Camada de Dados**: Tools, Resources e Prompts totalmente expostos.
- **Higiene**: Repositório limpo, logs ignorados pelo git, estrutura de certificação estabelecida.

## Arquitetura
- O core continua agnóstico (`src/dgm_mcp/core/`).
- O adaptador MCP (`src/dgm_mcp/mcp/adapter.py`) é o ponto único de integração.
- A segurança (`PathGuard`) é aplicada em tempo de execução no core.

## Roadmap
- v0.2.0: Lançamento oficial (MCP Nativo).
- v0.3.0: Remoção completa do bridge legado e expansão de resources.

## Notas Operacionais
- Usar `dgm-mcp run-stdio` para integração com IDEs e Desktop apps.
- Consultar `certification/` para templates de validação.
