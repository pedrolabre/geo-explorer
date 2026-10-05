"""
Serviço de emissão, persistência e validação de certificados digitais.
"""
import hashlib
import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any
from jinja2 import Template

from src.services.track_service import TrackService
from src.models.certificate import Certificado, ValidacaoCertificado


class CertificateService:
    """Gerencia a emissão e validação criptográfica de certificados de conclusão."""

    def __init__(
        self,
        track_service: Optional[TrackService] = None,
        base_dir: Optional[Path] = None
    ):
        self.base_dir = base_dir or Path(__file__).resolve().parent.parent.parent
        self.track_service = track_service or TrackService(self.base_dir / "data" / "trilhas.json")
        self.templates_dir = self.base_dir / "templates"
        self.output_dir = self.base_dir / "certificates" / "generated"
        self.db_certificados_path = self.base_dir / "data" / "certificados_emitidos.json"

        self.output_dir.mkdir(parents=True, exist_ok=True)
        self._inicializar_base_certificados()

    def _inicializar_base_certificados(self) -> None:
        """Garante a existência do arquivo de armazenamento de certificados."""
        if not self.db_certificados_path.exists():
            with open(self.db_certificados_path, "w", encoding="utf-8") as f:
                json.dump([], f, indent=2, ensure_ascii=False)

    def _salvar_certificado_db(self, certificado: Certificado) -> None:
        """Persiste o registro do certificado emitido na base JSON."""
        certificados = self.listar_certificados()
        certificados.append(certificado)
        with open(self.db_certificados_path, "w", encoding="utf-8") as f:
            json.dump(
                [c.model_dump() for c in certificados],
                f,
                indent=2,
                ensure_ascii=False
            )

    def listar_certificados(self) -> List[Certificado]:
        """Recupera todos os certificados emitidos."""
        try:
            with open(self.db_certificados_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [Certificado(**item) for item in data]
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _calcular_hash(
        self,
        aluno: str,
        trilha_id: str,
        carga: int,
        codigo: str,
        data_str: str
    ) -> str:
        """Gera um hash SHA-256 único e determinístico para garantir autenticidade."""
        payload = f"{aluno.strip().lower()}:{trilha_id}:{carga}:{codigo}:{data_str}"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def emitir_certificado(
        self,
        aluno_nome: str,
        tecnologia: str
    ) -> Certificado:
        """
        Emite um certificado para o aluno especificado e tecnologia concluída.
        Gera versões em texto formatado (.txt) e página estilizada (.html).
        """
        if not aluno_nome or not aluno_nome.strip():
            raise ValueError("O nome do aluno é obrigatório para emissão do certificado.")

        trilha = self.track_service.obter_por_identificador(tecnologia)
        if not trilha:
            tecnologias_disponiveis = [t.slug for t in self.track_service.listar_todas()]
            raise ValueError(
                f"Tecnologia '{tecnologia}' não encontrada. "
                f"Opções disponíveis: {', '.join(tecnologias_disponiveis)}"
            )

        nome_formatado = aluno_nome.strip().title()
        agora = datetime.now()
        data_emissao_str = agora.strftime("%d/%m/%Y às %H:%M")
        
        # Gera código único alfanumérico amigável
        codigo_sufixo = uuid.uuid4().hex[:8].upper()
        codigo_validacao = f"GEO-BOB-{agora.year}-{codigo_sufixo}"

        hash_seguranca = self._calcular_hash(
            aluno=nome_formatado,
            trilha_id=trilha.id,
            carga=trilha.carga_horaria_horas,
            codigo=codigo_validacao,
            data_str=data_emissao_str
        )

        contexto = {
            "aluno_nome": nome_formatado,
            "trilha_id": trilha.id,
            "trilha_nome": trilha.nome,
            "carga_horaria_horas": trilha.carga_horaria_horas,
            "data_emissao": data_emissao_str,
            "codigo_validacao": codigo_validacao,
            "hash_seguranca": hash_seguranca
        }

        # 1. Renderiza template TXT
        txt_template_path = self.templates_dir / "certificate_template.txt"
        with open(txt_template_path, "r", encoding="utf-8") as f:
            tmpl_txt = Template(f.read())
        conteudo_txt = tmpl_txt.render(**contexto)

        arquivo_txt = self.output_dir / f"certificado_{codigo_validacao}.txt"
        with open(arquivo_txt, "w", encoding="utf-8") as f:
            f.write(conteudo_txt)

        # 2. Renderiza template HTML
        html_template_path = self.templates_dir / "certificate_template.html"
        with open(html_template_path, "r", encoding="utf-8") as f:
            tmpl_html = Template(f.read())
        conteudo_html = tmpl_html.render(**contexto)

        arquivo_html = self.output_dir / f"certificado_{codigo_validacao}.html"
        with open(arquivo_html, "w", encoding="utf-8") as f:
            f.write(conteudo_html)

        certificado = Certificado(
            codigo_validacao=codigo_validacao,
            aluno_nome=nome_formatado,
            trilha_id=trilha.id,
            trilha_nome=trilha.nome,
            carga_horaria_horas=trilha.carga_horaria_horas,
            data_emissao=data_emissao_str,
            hash_seguranca=hash_seguranca,
            caminho_html=str(arquivo_html),
            caminho_txt=str(arquivo_txt)
        )

        self._salvar_certificado_db(certificado)
        return certificado

    def validar_certificado(self, codigo_ou_hash: str) -> ValidacaoCertificado:
        """
        Valida a autenticidade de um certificado a partir de seu código ou hash de segurança.
        """
        if not codigo_ou_hash:
            return ValidacaoCertificado(
                valido=False,
                mensagem="Código ou hash não informado."
            )

        termo = codigo_ou_hash.strip().upper()
        certificados = self.listar_certificados()

        encontrado: Optional[Certificado] = None
        for cert in certificados:
            if cert.codigo_validacao.upper() == termo or cert.hash_seguranca.upper() == termo:
                encontrado = cert
                break

        if not encontrado:
            return ValidacaoCertificado(
                valido=False,
                mensagem=f"Nenhum certificado registrado com o código/hash '{codigo_ou_hash}'."
            )

        # Recalcula o hash para conferir se não houve adulteração
        hash_esperado = self._calcular_hash(
            aluno=encontrado.aluno_nome,
            trilha_id=encontrado.trilha_id,
            carga=encontrado.carga_horaria_horas,
            codigo=encontrado.codigo_validacao,
            data_str=encontrado.data_emissao
        )

        if hash_esperado != encontrado.hash_seguranca:
            return ValidacaoCertificado(
                valido=False,
                mensagem="Alerta de integridade: os dados do certificado foram adulterados!",
                certificado=encontrado
            )

        return ValidacaoCertificado(
            valido=True,
            mensagem="Certificado autêntico e verificado com sucesso!",
            certificado=encontrado
        )
