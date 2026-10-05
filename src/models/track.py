"""
Modelos de dados para Trilhas de Aprendizagem e Módulos.
"""
from typing import List
from pydantic import BaseModel, Field


class Modulo(BaseModel):
    """Representa um módulo componente de uma trilha."""
    ordem: int
    titulo: str
    duracao_horas: int
    topicos: List[str] = Field(default_factory=list)


class Desafio(BaseModel):
    """Representa um desafio de código vinculado a uma trilha."""
    id: str
    nivel: str  # iniciante, intermediario, avancado
    titulo: str
    descricao: str
    criterios_aceite: List[str] = Field(default_factory=list)
    dica: str = ""


class Trilha(BaseModel):
    """Representa uma trilha de aprendizagem completa."""
    id: str
    slug: str
    nome: str
    categoria: str
    descricao: str
    carga_horaria_horas: int
    modulos: List[Modulo] = Field(default_factory=list)
    desafios: List[Desafio] = Field(default_factory=list)
