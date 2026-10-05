"""
Serviço de geração e consulta de desafios práticos de código.
"""
import random
from typing import Optional, List
from src.services.track_service import TrackService
from src.models.challenge import DesafioInfo
from src.models.track import Desafio


class ChallengeService:
    """Gerencia a busca e calibração de desafios de código."""

    def __init__(self, track_service: Optional[TrackService] = None):
        self.track_service = track_service or TrackService()

    def gerar_desafio(self, tecnologia: str, nivel: Optional[str] = None) -> DesafioInfo:
        """
        Gera um desafio de código para a tecnologia especificada e nível de dificuldade.
        Níveis suportados: iniciante, intermediario, avancado.
        """
        trilha = self.track_service.obter_por_identificador(tecnologia)
        if not trilha:
            tecnologias_disponiveis = [t.slug for t in self.track_service.listar_todas()]
            raise ValueError(
                f"Tecnologia '{tecnologia}' não encontrada. "
                f"Opções disponíveis: {', '.join(tecnologias_disponiveis)}"
            )

        desafios_trilha: List[Desafio] = trilha.desafios
        if not desafios_trilha:
            raise ValueError(f"Nenhum desafio cadastrado para a trilha '{trilha.nome}'.")

        if nivel:
            nivel_normalizado = nivel.strip().lower()
            # Mapeamento de possíveis variações de digitação
            mapa_niveis = {
                "iniciante": "iniciante",
                "junior": "iniciante",
                "jr": "iniciante",
                "basico": "iniciante",
                "intermediario": "intermediario",
                "intermediário": "intermediario",
                "pleno": "intermediario",
                "medio": "intermediario",
                "avancado": "avancado",
                "avançado": "avancado",
                "senior": "avancado",
                "sr": "avancado"
            }
            nivel_alvo = mapa_niveis.get(nivel_normalizado, nivel_normalizado)

            desafios_filtrados = [d for d in desafios_trilha if d.nivel.lower() == nivel_alvo]
            if not desafios_filtrados:
                niveis_validos = list(set(d.nivel for d in desafios_trilha))
                raise ValueError(
                    f"Nenhum desafio encontrado para o nível '{nivel}'. "
                    f"Níveis disponíveis para esta trilha: {', '.join(niveis_validos)}"
                )
            desafio_escolhido = random.choice(desafios_filtrados)
        else:
            # Se nenhum nível for informado, escolhe um desafio aleatório da trilha
            desafio_escolhido = random.choice(desafios_trilha)

        return DesafioInfo(
            trilha_id=trilha.id,
            trilha_nome=trilha.nome,
            tecnologia=trilha.slug,
            nivel=desafio_escolhido.nivel,
            desafio=desafio_escolhido
        )
