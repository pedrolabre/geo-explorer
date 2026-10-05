"""
Modelos de dados para Desafios de Código.
"""
from typing import List
from pydantic import BaseModel, Field
from src.models.track import Desafio


class DesafioInfo(BaseModel):
    """Informações completas de um desafio gerado."""
    trilha_id: str
    trilha_nome: str
    tecnologia: str
    nivel: str
    desafio: Desafio
