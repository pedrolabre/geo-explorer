# Arquitetura do Geo-Explorer

Este documento detalha o desenho arquitetural, os princípios de design e o fluxo de dados do projeto **Geo-Explorer**.

---

## 1. Visão Geral do Sistema

O Geo-Explorer adota uma arquitetura em camadas (**Layered Architecture**), desacoplando a camada de dados, regras de negócio e interfaces de comunicação (CLI e protocolo MCP).

```text
┌─────────────────────────────────────────────────────────────┐
│                   Interfaces de Consumo                     │
│  ┌─────────────────────────────┐  ┌──────────────────────┐  │
│  │     CLI Interativa / Rich   │  │  Servidor MCP (stdio)│  │
│  │       (src/cli.py)          │  │ (src/mcp/server.py)  │  │
│  └──────────────┬──────────────┘  └──────────┬───────────┘  │
└─────────────────┼────────────────────────────┼──────────────┘
                  │                            │
┌─────────────────▼────────────────────────────▼──────────────┐
│                    Camada de Serviços                       │
│  ┌──────────────────┐  ┌──────────────────┐  ┌───────────┐  │
│  │   TrackService   │  │ ChallengeService │  │CertService│  │
│  └────────┬─────────┘  └────────┬─────────┘  └─────┬─────┘  │
└───────────┼─────────────────────┼──────────────────┼────────┘
            │                     │                  │
┌───────────▼─────────────────────▼──────────────────▼────────┐
│               Modelos e Armazenamento de Dados              │
│  ┌──────────────────┐  ┌──────────────────┐  ┌───────────┐  │
│  │   Trilha / Modulo│  │   Desafio / Info │  │Certificado│  │
│  │ (data/trilhas.json)│ │ (Templates TXT/HTML)│ (SHA-256) │  │
│  └──────────────────┘  └──────────────────┘  └───────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Componentes Principais

### 2.1 Camada de Domínio e Modelos (`src/models/`)
- **`track.py`**: Modelos Pydantic para `Trilha`, `Modulo` e `Desafio`.
- **`challenge.py`**: Modelo para `DesafioInfo`, encapsulando dados de saída e contextualização técnica.
- **`certificate.py`**: Modelo para emissão (`Certificado`) e auditoria de integridade (`ValidacaoCertificado`).

### 2.2 Camada de Serviços (`src/services/`)
- **`TrackService`**: Leitura, busca textual por similaridade/slug e listagem de tecnologias.
- **`ChallengeService`**: Sorteio e calibração de desafios técnicos por senioridade (Iniciante, Intermediário, Avançado).
- **`CertificateService`**: Cálculo de hash determinístico SHA-256, renderização via Jinja2 (versões terminal e web responsiva) e persistência de registros em `data/certificados_emitidos.json`.

### 2.3 Camada de Interfaces
- **CLI (`src/cli.py`)**: Interface de terminal com suporte a flags de comando direto ou menu interativo guiado pela biblioteca `rich`.
- **MCP Server (`src/mcp/server.py`)**: Exposição padronizada via Model Context Protocol (stdio) de:
  - **Tools**: `consultar_trilha`, `gerar_desafio`, `gerar_certificado`, `validar_certificado`, `listar_tecnologias`.
  - **Resources**: `geoexplorer://trilhas` e `geoexplorer://catalogo`.
  - **Prompts**: `mentoria_estudo` e `avaliar_codigo_desafio`.

---

## 3. Segurança e Integridade

1. **Assinatura Digital de Certificados**: Cada certificado recebe um hash SHA-256 gerado a partir de seus dados imutáveis (`aluno`, `trilha_id`, `carga_horaria`, `codigo`, `data`). Na validação, o hash é recalculado; caso haja qualquer adulteração nos arquivos ou registros, o sistema detecta imediatamente.
2. **Isolamento de Processos**: A comunicação MCP via `stdio` garante que nenhuma porta de rede aberta seja necessária no ambiente local, mantendo o processo estritamente sob permissões do usuário.
