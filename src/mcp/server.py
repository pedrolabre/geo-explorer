"""
Servidor Model Context Protocol (MCP) do Geo-Explorer.
Exposição de ferramentas (tools), recursos (resources) e templates de prompts.
"""
import json
from typing import Optional
from mcp.server.mcpserver import MCPServer

from src.services.track_service import TrackService
from src.services.challenge_service import ChallengeService
from src.services.certificate_service import CertificateService

# Inicialização do servidor MCP
mcp_server = MCPServer("geo-explorer")

# Instanciação dos serviços de domínio
track_service = TrackService()
challenge_service = ChallengeService(track_service)
certificate_service = CertificateService(track_service)


# ==============================================================================
# TOOLS (Funções executáveis invocadas por agentes e clientes MCP)
# ==============================================================================

@mcp_server.tool(
    name="consultar_trilha",
    description="Consulta o plano de estudos detalhado de uma tecnologia (ex: ibm-bob, python, typescript, devops, java). Retorna nome, carga horária, módulos e tópicos."
)
def consultar_trilha(tecnologia: str) -> str:
    """Busca o plano de estudos para a tecnologia indicada."""
    trilha = track_service.obter_por_identificador(tecnologia)
    if not trilha:
        opcoes = [t.slug for t in track_service.listar_todas()]
        return json.dumps({
            "status": "erro",
            "mensagem": f"Tecnologia '{tecnologia}' não encontrada.",
            "opcoes_disponiveis": opcoes
        }, indent=2, ensure_ascii=False)

    return json.dumps({
        "status": "sucesso",
        "trilha": trilha.model_dump()
    }, indent=2, ensure_ascii=False)


@mcp_server.tool(
    name="gerar_desafio",
    description="Gera um desafio prático de código conforme a tecnologia e nível informado (iniciante, intermediario, avancado)."
)
def gerar_desafio(tecnologia: str, nivel: str = "iniciante") -> str:
    """Gera um desafio de código para prática."""
    try:
        resultado = challenge_service.gerar_desafio(tecnologia, nivel)
        return json.dumps({
            "status": "sucesso",
            "dados": resultado.model_dump()
        }, indent=2, ensure_ascii=False)
    except ValueError as e:
        return json.dumps({
            "status": "erro",
            "mensagem": str(e)
        }, indent=2, ensure_ascii=False)


@mcp_server.tool(
    name="gerar_certificado",
    description="Emite um certificado oficial de conclusão de trilha para o aluno com código de validação único e hash SHA-256."
)
def gerar_certificado(aluno_nome: str, tecnologia: str) -> str:
    """Emite o certificado nos formatos texto e HTML estilizado."""
    try:
        cert = certificate_service.emitir_certificado(aluno_nome, tecnologia)
        return json.dumps({
            "status": "sucesso",
            "certificado": cert.model_dump()
        }, indent=2, ensure_ascii=False)
    except ValueError as e:
        return json.dumps({
            "status": "erro",
            "mensagem": str(e)
        }, indent=2, ensure_ascii=False)


@mcp_server.tool(
    name="validar_certificado",
    description="Verifica a autenticidade e integridade de um certificado emitido pelo Geo-Explorer a partir do seu código ou hash SHA-256."
)
def validar_certificado(codigo_ou_hash: str) -> str:
    """Valida se o certificado foi emitido legitimamente pelo Geo-Explorer."""
    validacao = certificate_service.validar_certificado(codigo_ou_hash)
    return json.dumps({
        "status": "sucesso",
        "valido": validacao.valido,
        "mensagem": validacao.mensagem,
        "dados": validacao.certificado.model_dump() if validacao.certificado else None
    }, indent=2, ensure_ascii=False)


@mcp_server.tool(
    name="listar_tecnologias",
    description="Lista o catálogo com todas as tecnologias, categorias e cargas horárias disponíveis no Geo-Explorer."
)
def listar_tecnologias() -> str:
    """Retorna o resumo de todas as trilhas cadastradas."""
    resumo = track_service.listar_resumo_tecnologias()
    return json.dumps({
        "status": "sucesso",
        "total": len(resumo),
        "tecnologias": resumo
    }, indent=2, ensure_ascii=False)


# ==============================================================================
# RESOURCES (Fontes de dados estáticas/dinâmicas expostas via URI)
# ==============================================================================

@mcp_server.resource("geoexplorer://trilhas", mime_type="application/json")
def get_todas_trilhas() -> str:
    """Recurso com o catálogo integral de trilhas cadastradas."""
    trilhas = [t.model_dump() for t in track_service.listar_todas()]
    return json.dumps(trilhas, indent=2, ensure_ascii=False)


@mcp_server.resource("geoexplorer://catalogo", mime_type="application/json")
def get_catalogo_resumido() -> str:
    """Recurso com a listagem resumida de tecnologias disponíveis."""
    resumo = track_service.listar_resumo_tecnologias()
    return json.dumps(resumo, indent=2, ensure_ascii=False)


# ==============================================================================
# PROMPTS (Templates pré-formatados de instrução para agentes de IA)
# ==============================================================================

@mcp_server.prompt(
    name="mentoria_estudo",
    description="Template de mentoria técnica para o modelo orientar o estudante através de uma trilha de aprendizagem."
)
def mentoria_estudo(tecnologia: str, objetivo_profissional: str = "transição de carreira") -> list[dict]:
    """Cria prompt estruturado de mentoria guiada."""
    trilha = track_service.obter_por_identificador(tecnologia)
    nome_trilha = trilha.nome if trilha else tecnologia

    return [
        {
            "role": "user",
            "content": (
                f"Você é um Tech Lead e mentor especialista no ecossistema de software empresarial. "
                f"O aluno está cursando a trilha '{nome_trilha}' com o objetivo de: '{objetivo_profissional}'.\n\n"
                f"Com base na estrutura de módulos da trilha, elabore um plano de ação semanal dividido em etapas, "
                f"incluindo sugestões de exercícios práticos, tópicos para atenção especial e dicas de mercado."
            )
        }
    ]


@mcp_server.prompt(
    name="avaliar_codigo_desafio",
    description="Template para o agente atuar como revisor técnico sênior avaliando a submissão de um desafio de código."
)
def avaliar_codigo_desafio(tecnologia: str, nivel: str, codigo_submetido: str) -> list[dict]:
    """Cria prompt estruturado de code review para o desafio do aluno."""
    return [
        {
            "role": "user",
            "content": (
                f"Você é o revisor sênior de código do Geo-Explorer. "
                f"O aluno submeteu a seguinte solução para o desafio da trilha '{tecnologia}' no nível '{nivel}':\n\n"
                f"```\n{codigo_submetido}\n```\n\n"
                f"Analise o código considerando:\n"
                f"1. Aderência aos requisitos e boas práticas da linguagem;\n"
                f"2. Complexidade e clareza;\n"
                f"3. Tratamento de exceções e possíveis vulnerabilidades de segurança;\n"
                f"4. Sugestão construtiva e didática de melhoria."
            )
        }
    ]


def main() -> None:
    """Inicia o servidor MCP utilizando o transporte padrão stdio."""
    mcp_server.run(transport="stdio")


if __name__ == "__main__":
    main()
