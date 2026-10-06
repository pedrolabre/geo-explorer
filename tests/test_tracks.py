"""
Testes unitários para o TrackService e modelos de trilhas.
"""
import pytest
from src.services.track_service import TrackService


@pytest.fixture
def track_service():
    return TrackService()


def test_listar_todas_trilhas(track_service):
    trilhas = track_service.listar_todas()
    assert len(trilhas) >= 5
    slugs = [t.slug for t in trilhas]
    assert "ibm-bob" in slugs
    assert "python" in slugs
    assert "typescript" in slugs
    assert "devops" in slugs
    assert "java" in slugs


def test_obter_por_identificador_exato(track_service):
    trilha = track_service.obter_por_identificador("ibm-bob")
    assert trilha is not None
    assert "IBM Bob" in trilha.nome
    assert trilha.carga_horaria_horas == 45
    assert len(trilha.modulos) == 4
    assert len(trilha.desafios) == 3


def test_obter_por_termo_parcial(track_service):
    trilha = track_service.obter_por_identificador("agentic")
    assert trilha is not None
    assert trilha.slug == "ibm-bob"


def test_obter_inexistente_retorna_none(track_service):
    trilha = track_service.obter_por_identificador("tecnologia-alienigena-123")
    assert trilha is None


def test_listar_resumo_tecnologias(track_service):
    resumo = track_service.listar_resumo_tecnologias()
    assert len(resumo) >= 5
    for item in resumo:
        assert "id" in item
        assert "slug" in item
        assert "nome" in item
        assert "categoria" in item
        assert "carga_horaria_horas" in item
        assert "total_modulos" in item
        assert "total_desafios" in item


def test_buscar_por_termo_multiplos(track_service):
    resultados = track_service.buscar_por_termo("IA")
    assert len(resultados) >= 2  # Pelo menos Bob e Python IA
