# IBM Bob — Diretrizes e Guardrails do Projeto Geo-Explorer

## Governança e Modos de Operação
- **autoApprove**: false
- **Persona Padrão**: Code (para implementação) e Plan (para novas features)
- **Human-in-the-Loop**: Sempre solicitar confirmação antes de alterações destrutivas em arquivos de dados ou exclusão de módulos.

## Guardrails de Segurança
1. **Segredos e Credenciais**: Nunca expor tokens, chaves de API ou dados sensíveis em arquivos do repositório.
2. **Context Poisoning**: Não injetar arquivos de teste binários ou logs volumosos na janela de contexto; utilizar referências pontuais.
3. **Escopo de Alteração**: Ao implementar comandos ou rotas, manter separação estrita entre models, services e interfaces (CLI/MCP).

## Padrões de Código
- **Linguagem**: Python 3.12+ com type hints estritos (`typing`, `dataclasses`, `pydantic`).
- **Arquitetura**: Camadas desacopladas (`models`, `services`, `mcp`, `cli`).
- **Testes**: Cobrir todos os serviços e comandos com `pytest`.
- **Mensagens de Commit**: Conventional Commits (`feat:`, `fix:`, `docs:`, `test:`, `refactor:`).
