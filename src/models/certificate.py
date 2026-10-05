"""
Modelos de dados para Emissão e Validação de Certificados.
"""
from typing import Optional
from pydantic import BaseModel


class Certificado(BaseModel):
    """Representa um certificado de conclusão de trilha emitido pelo Geo-Explorer."""
    codigo_validacao: str
    aluno_nome: str
    trilha_id: str
    trilha_nome: str
    carga_horaria_horas: int
    data_emissao: str
    hash_seguranca: str
    caminho_html: Optional[str] = None
    caminho_txt: Optional[str] = None


class ValidacaoCertificado(BaseModel):
    """Resultado da checagem de autenticidade de um certificado."""
    valido: bool
    mensagem: str
    certificado: Optional[Certificado] = None
