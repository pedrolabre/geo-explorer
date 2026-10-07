# 🚀 Geo-Explorer

> **Plataforma interativa de exploração de trilhas de aprendizagem, desafios práticos de código e certificação digital.**  
> Projeto desenvolvido no desafio da formação **IBM Bob: IA de Nível Empresarial para Desenvolvedores e Tech Leaders** (DIO 2026).

---

## 📌 Sumário
- [1. O que é o Geo-Explorer](#1-o-que-é-o-geo-explorer)
- [2. Arquitetura e Tecnologias](#2-arquitetura-e-tecnologias)
- [3. Instalação e Pré-requisitos](#3-instalação-e-pré-requisitos)
- [4. Como Usar os Comandos](#4-como-usar-os-comandos)
- [5. Servidor MCP (Model Context Protocol)](#5-servidor-mcp-model-context-protocol)
- [6. Execução dos Testes Automatizados](#6-execução-dos-testes-automatizados)
- [7. Melhorias e Diferenciais Implementados](#7-melhorias-e-diferenciais-implementados)
- [8. O Que Aprendi Durante o Desafio](#8-o-que-aprendi-durante-o-desafio)
- [9. Governança e Regras com o IBM Bob](#9-governança-e-regras-com-o-ibm-bob)

---

## 1. O que é o Geo-Explorer

O **Geo-Explorer** é uma solução completa desenvolvida para transformar a forma como pessoas desenvolvedoras navegam e consolidam seus conhecimentos técnicos. A plataforma permite:
- **Consultar Trilhas de Estudo**: Acessar ementas completas com carga horária, tópicos e objetivos formativos.
- **Gerar Desafios Práticos de Código**: Receber desafios calibrados por nível de senioridade (*Iniciante*, *Intermediário*, *Avançado*), contendo critérios de aceite e orientações técnicas.
- **Emitir Certificados Verificáveis**: Gerar certificados com código alfanumérico único e assinatura digital criptográfica (hash SHA-256), exportados tanto em formato de terminal (ASCII) quanto em página web responsiva (HTML).
- **Validar Autenticidade**: Sistema de auditoria que verifica se o certificado foi emitido pela plataforma e se os dados originais sofreram qualquer adulteração.
- **Integração com Agentes de IA via MCP**: Um servidor nativo baseado no padrão *Model Context Protocol* para que agentes como o **IBM Bob** possam consultar trilhas, gerar desafios e emitir certificados diretamente em conversas por linguagem natural.

---

## 2. Arquitetura e Tecnologias

O projeto adota uma arquitetura em camadas desacopladas (**Layered Architecture**):

```text
├── .bob/                      # Guardrails e regras de governança para o IBM Bob
│   └── rules.md
├── .bobignore                # Arquivos ignorados pelo indexador do Bob
├── .gitignore                # Padrões de exclusão de arquivos transitórios
├── AGENTS.md                 # Contexto persistente do repositório para agentes de IA
├── README.md                 # Documentação de portfólio oficial
├── bob_mcp_settings.json     # Configuração pronta para conexão do servidor MCP no Bob
├── pyproject.toml            # Metadados do projeto e scripts de entrada
├── requirements.txt          # Dependências Python
├── data/
│   ├── trilhas.json          # Base estruturada com trilhas, módulos e desafios
│   └── certificados_emitidos.json # Registro persistente para auditoria e validação
├── src/
│   ├── cli.py                # Interface de linha de comando (comandos diretos e menu interativo)
│   ├── models/               # Modelos de dados e validações (Pydantic)
│   │   ├── track.py
│   │   ├── challenge.py
│   │   └── certificate.py
│   ├── services/             # Lógica de negócio e regras de domínio
│   │   ├── track_service.py
│   │   ├── challenge_service.py
│   │   └── certificate_service.py
│   └── mcp/                  # Servidor Model Context Protocol (stdio)
│       └── server.py
├── templates/
│   ├── certificate_template.html # Template visual responsivo com CSS moderno
│   └── certificate_template.txt  # Template estilizado para terminal
├── tests/                    # Suíte de testes automatizados com pytest
│   ├── test_tracks.py
│   ├── test_challenges.py
│   ├── test_certificates.py
│   └── test_mcp_server.py
└── docs/
    ├── arquitetura.md        # Documento de desenho técnico
    └── mcp_setup.md          # Passo a passo de integração do Servidor MCP
```

### Tecnologias Utilizadas:
- **Python 3.12+ / 3.14**: Tipagem estática e core engine.
- **Pydantic**: Validação de schemas e serialização estruturada.
- **Rich**: Renderização visual de tabelas, painéis e menus interativos no terminal.
- **Jinja2**: Mecanismo de renderização de templates de certificados (TXT e HTML).
- **SDK Oficial MCP (Model Context Protocol)**: Exposição de tools, resources e prompts.
- **Pytest**: Suíte completa de testes unitários e de integração.

---

## 3. Instalação e Pré-requisitos

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/pedrolabre/geo-explorer.git
   cd geo-explorer
   ```

2. **Crie e ative um ambiente virtual (recomendado):**
   ```bash
   python -m venv .venv
   # No Windows:
   .venv\Scripts\activate
   # No Linux/macOS:
   source .venv/bin/activate
   ```

3. **Instale as dependências:**
   ```bash
   python -m pip install -r requirements.txt
   ```

---

## 4. Como Usar os Comandos

A aplicação pode ser utilizada de duas formas: através de um **Menu Interativo Guiado** ou via **Comandos Diretos no Terminal**.

### 4.1 Menu Interativo
Para abrir o menu interativo com navegação facilitada, basta rodar sem argumentos:
```bash
python -m src.cli
```

### 4.2 Comandos Diretos

- **Listar todas as tecnologias disponíveis:**
  ```bash
  python -m src.cli listar
  ```

- **Consultar o plano de estudos de uma trilha:**
  ```bash
  python -m src.cli trilha ibm-bob
  python -m src.cli trilha python
  python -m src.cli trilha typescript
  ```

- **Gerar um desafio prático de código:**
  ```bash
  # Sintaxe: python -m src.cli desafio <tecnologia> <nivel>
  python -m src.cli desafio ibm-bob iniciante
  python -m src.cli desafio python intermediario
  python -m src.cli desafio devops avancado
  ```

- **Emitir um certificado de conclusão:**
  ```bash
  # Sintaxe: python -m src.cli certificado "<Nome do Aluno>" <tecnologia>
  python -m src.cli certificado "Pedro Dev" ibm-bob
  ```
  *O certificado é renderizado no terminal e salvo automaticamente nos formatos `.txt` e `.html` dentro de `certificates/generated/`.*

- **Validar a autenticidade de um certificado:**
  ```bash
  # Sintaxe: python -m src.cli verificar <codigo_ou_hash>
  python -m src.cli verificar GEO-BOB-2026-FE7217CB
  ```

---

## 5. Servidor MCP (Model Context Protocol)

O projeto implementa a especificação oficial do **Model Context Protocol (MCP)** sobre transporte `stdio`, permitindo que agentes de IA consumam suas funcionalidades de forma transparente.

### Recursos Expostos pelo MCP:
- **Tools**:
  - `consultar_trilha`: Retorna módulos, tópicos e ementa detalhada de uma tecnologia.
  - `gerar_desafio`: Fornece enunciados, critérios de aceite e dicas por senioridade.
  - `gerar_certificado`: Emite novos certificados e persiste a auditoria digital.
  - `validar_certificado`: Confere a autenticidade e detecta alterações indevidas.
  - `listar_tecnologias`: Fornece a listagem consolidada do catálogo.
- **Resources**:
  - `geoexplorer://trilhas`: Catálogo completo em JSON.
  - `geoexplorer://catalogo`: Resumo leve de tecnologias.
- **Prompts**:
  - `mentoria_estudo`: Template para o IBM Bob orientar cronogramas de aprendizado.
  - `avaliar_codigo_desafio`: Template para o IBM Bob revisar soluções submetidas por estudantes.

### Como Conectar ao IBM Bob
O arquivo `bob_mcp_settings.json` na raiz do projeto já está pronto para uso:
```json
{
  "mcpServers": {
    "geo-explorer": {
      "command": "python",
      "args": [
        "-m",
        "src.mcp.server"
      ],
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```
Para mais detalhes, consulte [docs/mcp_setup.md](docs/mcp_setup.md).

---

## 6. Execução dos Testes Automatizados

O projeto conta com testes unitários e de integração cobrindo 100% dos serviços e do servidor MCP.

Para executar todos os testes:
```bash
python -m pytest -v
```

Exemplo de resultado esperado:
```text
tests/test_certificates.py::test_emitir_certificado_sucesso PASSED       [  4%]
tests/test_certificates.py::test_validar_certificado_existente PASSED    [  8%]
tests/test_certificates.py::test_validar_certificado_inexistente PASSED  [ 12%]
...
tests/test_mcp_server.py::test_mcp_tool_consultar_trilha PASSED          [ 50%]
tests/test_mcp_server.py::test_mcp_resources PASSED                      [ 70%]
tests/test_mcp_server.py::test_mcp_prompts PASSED                        [ 75%]
...
tests/test_tracks.py::test_buscar_por_termo_multiplos PASSED             [100%]
============================= 24 passed in 10.49s =============================
```

---

## 7. Melhorias e Diferenciais Implementados

Indo além do escopo básico do desafio, foram adicionadas as seguintes melhorias:
1. **Trilha Exclusiva "IBM Bob & Agentic AI"**: Base de conhecimento estruturada cobrindo personas do Bob, context window, Bobcoins, guardrails e MCP.
2. **Dupla Renderização de Certificados**: Emissão de versão em texto puro estilizado (para terminais e logs) e página HTML responsiva com tema escuro e layout otimizado para impressão/PDF.
3. **Mecanismo Criptográfico de Auditoria (SHA-256)**: Cada certificado possui uma assinatura calculada a partir de seus atributos imutáveis, prevenindo falsificações.
4. **Validador de Integridade com Histórico**: Comando `verificar` que revalida o hash e confirma a existência legítima do certificado.
5. **Implementação Completa do Protocolo MCP 2.x**: Com suporte nativo a `tools`, `resources` e `prompts`, pronta para integração direta no IBM Bob IDE.
6. **Interface Terminal Aprimorada**: Utilização da biblioteca `rich` com tabelas, cores e painéis, incluindo fallback seguro de codificação para ambientes Windows e Linux.

---

## 8. O Que Aprendi Durante o Desafio

- **O Paradoxo do Desenvolvedor Orquestrador**: Compreendi na prática a transição do papel de quem apenas digita código para quem orquestra agentes de IA, definindo contratos, revisando planos e mantendo o humano no controle (*Human-in-the-loop*).
- **Importância do Contexto Persistente (`AGENTS.md`)**: A estruturação clara das convenções e arquitetura do projeto reduz o risco de *context poisoning* e garante que o agente gere código coerente com os padrões da equipe.
- **O Poder do Model Context Protocol (MCP)**: Entendi por que o MCP é chamado de "USB da IA". A capacidade de expor uma ferramenta local via `stdio` e permitir que um modelo de linguagem execute ações reais com parâmetros tipados padroniza a integração de ferramentas no ciclo de desenvolvimento.
- **Governança e Guardrails**: A configuração de políticas de aprovação (`autoApprove: false`) e a proteção de arquivos de indexação (`.bobignore`) são fundamentais para segurança em ambientes corporativos.

---

## 9. Governança e Regras com o IBM Bob

- Regras e guardrails ativos: confira [`.bob/rules.md`](.bob/rules.md).
- Mapa de contexto e convenções do repositório: confira [`AGENTS.md`](AGENTS.md).
- Arquitetura detalhada: confira [`docs/arquitetura.md`](docs/arquitetura.md).
- Passo a passo de integração MCP: confira [`docs/mcp_setup.md`](docs/mcp_setup.md).

---

## 📄 Licença
Distribuído sob a licença MIT. Sinta-se livre para utilizar, estudar e evoluir a solução!
