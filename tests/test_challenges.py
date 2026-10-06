"""
Testes unitários para o ChallengeService.
"""
import pytest
from src.services.track_service import TrackService
from src.services.challenge_service import ChallengeService


@pytest.fixture
def challenge_service():
    return ChallengeService(TrackService())


def test_gerar_desafio_iniciante(challenge_service):
    resultado = challenge_service.gerar_desafio("ibm-bob", "iniciante")
    assert resultado.trilha_id == "ibm-bob-agentic-ai"
    assert resultado.nivel == "iniciante"
    assert resultado.desafio.titulo is not None
    assert len(resultado.desafio.criterios_aceite) > 0


def test_gerar_desafio_intermediario(challenge_service):
    resultado = challenge_service.gerar_desafio("python", "intermediario")
    assert resultado.nivel == "intermediario"
    assert resultado.desafio.titulo is not None


def test_gerar_desafio_avancado(challenge_service):
    resultado = challenge_service.gerar_desafio("devops", "avancado")
    assert resultado.nivel == "avancado"


def test_gerar_desafio_alias_junior(challenge_service):
    resultado = challenge_service.gerar_desafio("typescript", "junior")
    assert resultado.nivel == "iniciante"


def test_gerar_desafio_tecnologia_invalida(challenge_service):
    with pytest.raises(ValueError, match="Tecnologia 'inexistente' não encontrada"):
        challenge_service.gerar_desafio("inexistente", "iniciante")


def test_gerar_desafio_nivel_invalido(challenge_service):
    with pytest.raises(ValueError, match="Nenhum desafio encontrado para o nível 'mestre'"):
        challenge_service.gerar_desafio("ibm-bob", "mestre")
