# AGENTS.md — Instruções e Contexto do Projeto Geo-Explorer

> Este arquivo fornece contexto persistente para o **IBM Bob** e outros agentes de IA no desenvolvimento e manutenção do projeto **Geo-Explorer**. Gerado e mantido no padrão oficial da formação IBM Bob / DIO 2026.

---

## 1. Visão Geral do Projeto
O **Geo-Explorer** é uma plataforma interativa de exploração de trilhas de aprendizagem em tecnologia. A aplicação oferece:
1. **Consulta de Trilhas**: Apresentação de planos de estudos detalhados por tecnologia e objetivos formativos.
2. **Geração de Desafios Práticos**: Emissão de desafios de código customizados por senioridade (Iniciante, Intermediário, Avançado).
3. **Emissão e Verificação de Certificados**: Criação de certificados com hash criptográfico SHA-256 e código de autenticidade (renderizados em ASCII e HTML).
4. **Servidor MCP (Model Context Protocol)**: Exposição de ferramentas (`tools`), fontes de dados (`resources`) e templates de prompt (`prompts`) para consumo direto por agentes de IA como o IBM Bob.

---

## 2. Estrutura do Diretório e Arquivos-Chave

```text
├── .bob/
│   └── rules.md                  # Guardrails e regras de governança para o Bob
├── .bobignore                    # Arquivos ignorados pelo indexador do Bob
├── .gitignore                    # Exclusões para versionamento Git
├── AGENTS.md                     # Contexto persistente para agentes (este arquivo)
├── README.md                     # Documentação de portfólio oficial
├── bob_mcp_settings.json         # Configuração de conexão do MCP Server para IBM Bob
├── pyproject.toml                # Metadados e configuração de build
├── requirements.txt              # Dependências do projeto
├── data/
│   └── trilhas.json              # Base de conhecimento com trilhas, módulos e desafios
├── src/
│   ├── cli.py                    # Interface de linha de comando (comandos interativos e diretos)
│   ├── models/                   # Dataclasses e schemas de validação
│   │   ├── track.py              # Modelos de Trilha, Módulo e Tópico
│   │   ├── challenge.py          # Modelo de Desafio de Código
│   │   └── certificate.py        # Modelo de Certificado e Registro de Emissão
│   ├── services/                 # Lógica de negócio e regras de domínio
│   │   ├── track_service.py      # Busca e filtragem de trilhas
│   │   ├── challenge_service.py  # Geração e calibração de desafios
│   │   └── certificate_service.py # Emissão, persistência e validação de certificados
│   └── mcp/                      # Servidor Model Context Protocol
│       └── server.py             # Implementação oficial do MCP (stdio)
├── templates/
│   ├── certificate_template.html # Template visual responsivo com CSS moderno
│   └── certificate_template.txt  # Template ASCII para saída estilizada no terminal
├── tests/
│   ├── test_tracks.py            # Testes de consulta de trilhas
│   ├── test_challenges.py        # Testes de geração de desafios
│   ├── test_certificates.py      # Testes de certificados e hash de segurança
│   └── test_mcp_server.py        # Testes de integração do servidor MCP
└── docs/
    ├── arquitetura.md            # Decisões de design e diagramas
    └── mcp_setup.md              # Passo a passo de integração com o IBM Bob
```

---

## 3. Comandos Comuns de Desenvolvimento

- **Executar a CLI Interativa:**
  ```bash
  python -m src.cli
  ```
- **Consultar uma Trilha:**
  ```bash
  python -m src.cli trilha "IBM Bob & Agentic AI"
  ```
- **Gerar um Desafio de Código:**
  ```bash
  python -m src.cli desafio "Python para IA" iniciante
  ```
- **Emitir Certificado:**
  ```bash
  python -m src.cli certificado "Pedro Dev" "DevOps & Cloud"
  ```
- **Validar Autenticidade de um Certificado:**
  ```bash
  python -m src.cli verificar GEO-xxxx-xxxx
  ```
- **Executar o Servidor MCP (stdio):**
  ```bash
  python -m src.mcp.server
  ```
- **Rodar a Suíte de Testes:**
  ```bash
  pytest -v
  ```

---

## 4. Modos de Trabalho e Papéis do Bob

O fluxo de trabalho com o IBM Bob respeita o ciclo **SDLC na Era dos Agentes**:
- **Modo Ask**: Usado para entender regras de negócio, explorar a base de trilhas e tirar dúvidas sobre contratos.
- **Modo Plan**: Usado para rascunhar o plano de implementação antes de alterações no código.
- **Modo Code**: Usado para implementar funções, testes e templates conforme o plano aprovado.
- **Modo Orchestrator**: Usado para coordenar migrações estruturais ou fluxos de integração contínua.

---

## 5. Diretrizes para Agentes de IA

1. **Idempotência e Segurança**: Não delete arquivos na pasta `data/` sem backup; use salvamento estruturado.
2. **Formatação de Saída**: Utilize a biblioteca `rich` para mensagens visuais elegantes no terminal, mantendo fallback amigável.
3. **Manutenção do AGENTS.md**: Sempre que novos comandos, módulos ou tabelas forem criados, atualize esta documentação e execute `/init` no chat do Bob para renovar o mapa de contexto.
