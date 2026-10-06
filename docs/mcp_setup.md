# Guia de Configuração do Servidor MCP (IBM Bob & Clientes MCP)

Este guia orienta como integrar o **Geo-Explorer** como um Servidor MCP (**Model Context Protocol**) no **IBM Bob** e em outros clientes compatíveis.

---

## 1. O que o Servidor MCP Disponibiliza?

Ao plugar o Geo-Explorer no IBM Bob, o agente ganha capacidades nativas de:
- **Consultar Trilhas**: `consultar_trilha(tecnologia="...")`
- **Gerar Desafios Técnicos**: `gerar_desafio(tecnologia="...", nivel="...")`
- **Emitir Certificados**: `gerar_certificado(aluno_nome="...", tecnologia="...")`
- **Validar Autenticidade**: `validar_certificado(codigo_ou_hash="...")`
- **Listar Catálogo**: `listar_tecnologias()`
- **Recursos Diretos (Resources)**: Acesso a `geoexplorer://trilhas` e `geoexplorer://catalogo`.
- **Prompts Estruturados**: Modelos pré-configurados para mentoria técnica e revisão de código.

---

## 2. Configurando no IBM Bob IDE

No IBM Bob IDE, os servidores MCP locais utilizam transporte `stdio`.

1. Localize ou crie o arquivo de configuração MCP do Bob (ou adicione no arquivo global de MCPs):
   - **Local do projeto**: `bob_mcp_settings.json` (já presente na raiz deste repositório)
   - **Global do Bob IDE**: `%USERPROFILE%/.config/Code/User/globalStorage/ibm.bob/mcp.json`

2. Insira a configuração abaixo:

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

3. Abra o chat agêntico do IBM Bob e teste em linguagem natural:
   > *"Liste as tecnologias disponíveis no Geo-Explorer"*  
   > *"Gere um desafio iniciante de Python para mim"*  
   > *"Emita um certificado para Maria Silva na trilha IBM Bob"*

O Bob identificará os tools automaticamente e executará as ações no sistema.

---

## 3. Testando o Servidor MCP Manualmente

Você pode verificar a saúde do servidor MCP executando diretamente pelo Python:

```bash
python -m src.mcp.server
```

Como o transporte padrão é `stdio`, o processo aguardará requisições JSON-RPC 2.0 pelo stdin.
Para rodar a suíte de testes do MCP:

```bash
python -m pytest tests/test_mcp_server.py -v
```
