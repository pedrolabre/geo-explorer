"""
Testes de integração das ferramentas, recursos e prompts do Servidor MCP.
"""
import json
import pytest
from src.mcp.server import (
    consultar_trilha,
    gerar_desafio,
    gerar_certificado,
    validar_certificado,
    listar_tecnologias,
    mentoria_estudo,
    avaliar_codigo_desafio,
    get_todas_trilhas,
    get_catalogo_resumido
)


def test_mcp_tool_consultar_trilha():
    resp_str = consultar_trilha("ibm-bob")
    resp = json.loads(resp_str)
    assert resp["status"] == "sucesso"
    assert "trilha" in resp
    assert resp["trilha"]["slug"] == "ibm-bob"


def test_mcp_tool_consultar_trilha_invalida():
    resp_str = consultar_trilha("inexistente")
    resp = json.loads(resp_str)
    assert resp["status"] == "erro"
    assert "opcoes_disponiveis" in resp


def test_mcp_tool_gerar_desafio():
    resp_str = gerar_desafio("python", "iniciante")
    resp = json.loads(resp_str)
    assert resp["status"] == "sucesso"
    assert resp["dados"]["nivel"] == "iniciante"


def test_mcp_tool_gerar_certificado():
    resp_str = gerar_certificado("Aluno Teste MCP", "ibm-bob")
    resp = json.loads(resp_str)
    assert resp["status"] == "sucesso"
    cert = resp["certificado"]
    assert cert["aluno_nome"] == "Aluno Teste Mcp"
    assert "codigo_validacao" in cert

    # Valida usando a tool de validação
    val_str = validar_certificado(cert["codigo_validacao"])
    val = json.loads(val_str)
    assert val["status"] == "sucesso"
    assert val["valido"] is True


def test_mcp_tool_listar_tecnologias():
    resp_str = listar_tecnologias()
    resp = json.loads(resp_str)
    assert resp["status"] == "sucesso"
    assert resp["total"] >= 5


def test_mcp_resources():
    trilhas_json = get_todas_trilhas()
    trilhas = json.loads(trilhas_json)
    assert isinstance(trilhas, list)
    assert len(trilhas) >= 5

    catalogo_json = get_catalogo_resumido()
    catalogo = json.loads(catalogo_json)
    assert isinstance(catalogo, list)
    assert len(catalogo) >= 5


def test_mcp_prompts():
    prompt_mentoria = mentoria_estudo("ibm-bob", "aprender agentes corporativos")
    assert len(prompt_mentoria) == 1
    assert "Tech Lead" in prompt_mentoria[0]["content"]

    prompt_review = avaliar_codigo_desafio("python", "iniciante", "print('hello world')")
    assert len(prompt_review) == 1
    assert "revisor sênior" in prompt_review[0]["content"]
