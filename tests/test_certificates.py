"""
Testes unitários para o CertificateService.
"""
from pathlib import Path
import pytest
from src.services.track_service import TrackService
from src.services.certificate_service import CertificateService


@pytest.fixture
def cert_service():
    return CertificateService(TrackService())


def test_emitir_certificado_sucesso(cert_service):
    cert = cert_service.emitir_certificado("Maria Aluna", "ibm-bob")
    
    assert cert.aluno_nome == "Maria Aluna"
    assert "IBM Bob" in cert.trilha_nome
    assert cert.carga_horaria_horas == 45
    assert cert.codigo_validacao.startswith("GEO-BOB-")
    assert len(cert.hash_seguranca) == 64  # SHA-256 tem 64 caracteres hexadecimais

    # Verifica se os arquivos físicos foram criados
    assert Path(cert.caminho_txt).exists()
    assert Path(cert.caminho_html).exists()

    # Confere o conteúdo do arquivo TXT
    with open(cert.caminho_txt, "r", encoding="utf-8") as f:
        txt_content = f.read()
        assert "Maria Aluna" in txt_content
        assert cert.codigo_validacao in txt_content


def test_validar_certificado_existente(cert_service):
    cert = cert_service.emitir_certificado("Lucas Teste", "python")
    
    # Validação pelo código
    val_cod = cert_service.validar_certificado(cert.codigo_validacao)
    assert val_cod.valido is True
    assert val_cod.certificado is not None
    assert val_cod.certificado.aluno_nome == "Lucas Teste"

    # Validação pelo hash
    val_hash = cert_service.validar_certificado(cert.hash_seguranca)
    assert val_hash.valido is True


def test_validar_certificado_inexistente(cert_service):
    val = cert_service.validar_certificado("GEO-INEXISTENTE-9999")
    assert val.valido is False
    assert "Nenhum certificado registrado" in val.mensagem


def test_emitir_certificado_aluno_vazio(cert_service):
    with pytest.raises(ValueError, match="nome do aluno é obrigatório"):
        cert_service.emitir_certificado("", "ibm-bob")


def test_emitir_certificado_tecnologia_invalida(cert_service):
    with pytest.raises(ValueError, match="não encontrada"):
        cert_service.emitir_certificado("Carlos Dev", "tecnologia-fake")
