# MCP Gap Analysis — DGM-MCP vs. Model Context Protocol (v1.0+)

## 1. Contexto Atual
O DGM-MCP atual funciona como um orquestrador de tarefas via FastAPI, mas não implementa a especificação oficial do Model Context Protocol (MCP) conforme definida pela Anthropic.

## 2. Análise de Conformidade

### 2.1 Tool Discovery
- **DGM-MCP**: Possui um endpoint customizado `/mcp/task` que recebe uma descrição de tarefa.
- **MCP Spec**: Requer o método `tools/list` para que o cliente possa descobrir as ferramentas disponíveis, seus esquemas de entrada (JSON Schema) e descrições.
- **Lacuna**: Falta implementação do endpoint de listagem de ferramentas seguindo o padrão JSON-RPC.

### 2.2 Resources
- **DGM-MCP**: Não possui conceito de "Resources".
- **MCP Spec**: Permite que servidores exponham dados (ficheiros, logs, bases de dados) através de URIs (ex: `file:///path/to/file`). Requer `resources/list`, `resources/read`, etc.
- **Lacuna**: Total. O sistema atual é puramente focado em ações (tools), não em dados estáticos/recursos.

### 2.3 Prompts
- **DGM-MCP**: Define prompts internamente em `src/dgm_mcp/llm/prompts.py`.
- **MCP Spec**: Permite que o servidor exponha templates de prompts reutilizáveis para o cliente via `prompts/list` e `prompts/get`.
- **Lacuna**: Total. Os prompts não são expostos via protocolo MCP.

### 2.4 JSON-RPC Transport
- **DGM-MCP**: Usa REST standard (POST com JSON arbitrário).
- **MCP Spec**: Toda a comunicação deve ser via JSON-RPC 2.0.
- **Lacuna**: Necessário migrar o formato das mensagens para pedidos/respostas JSON-RPC.

### 2.5 Transports
- **DGM-MCP**: Apenas HTTP (FastAPI).
- **MCP Spec**: Suporta:
  - **Stdio**: Para servidores locais (Claude Desktop usa isto).
  - **HTTP com SSE (Server-Sent Events)**: Para servidores remotos.
- **Lacuna**: Falta suporte para Stdio e SSE. O DGM-MCP atual é apenas um servidor web tradicional.

## 3. Requisitos para Conformidade Real

| Funcionalidade | Status Atual | Necessário para MCP Real |
| :--- | :--- | :--- |
| **Tool Discovery** | Customizado | Implementar `tools/list` (JSON Schema) |
| **Tool Call** | `/mcp/task` | Implementar `tools/call` (JSON-RPC) |
| **Resources** | Não existe | Implementar `resources/*` endpoints |
| **Prompts** | Internos | Implementar `prompts/*` endpoints |
| **Transport: Stdio** | Não | Implementar interface stdin/stdout |
| **Transport: HTTP/SSE** | Apenas REST | Implementar SSE para respostas asíncronas |
| **Protocolo** | REST | Implementar JSON-RPC 2.0 Layer |

## 4. Conclusão
O DGM-MCP é atualmente um **wrapper de agentes via API**, e não um **Servidor MCP**. Para se tornar um verdadeiro backend para o AndréOS e outras ferramentas que consomem MCP nativamente, é necessária uma refatoração profunda da camada de comunicação (Bridge) para adotar JSON-RPC e suportar múltiplos transportes (especialmente Stdio para uso local e SSE para web).
