"""
Serviço de gerenciamento e consulta de trilhas de aprendizagem.
"""
import json
from pathlib import Path
from typing import List, Optional, Dict, Any
from src.models.track import Trilha


class TrackService:
    """Gerencia a consulta e listagem de trilhas de aprendizagem."""

    def __init__(self, data_path: Optional[Path] = None):
        if data_path is None:
            # Caminho padrão data/trilhas.json a partir da raiz do projeto
            base_dir = Path(__file__).resolve().parent.parent.parent
            self.data_path = base_dir / "data" / "trilhas.json"
        else:
            self.data_path = Path(data_path)
        self._trilhas: List[Trilha] = []
        self._carregar_dados()

    def _carregar_dados(self) -> None:
        """Carrega e valida os dados de trilhas a partir do arquivo JSON."""
        if not self.data_path.exists():
            raise FileNotFoundError(f"Base de dados não encontrada em: {self.data_path}")

        with open(self.data_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

        trilhas_raw = raw_data.get("trilhas", [])
        self._trilhas = [Trilha(**item) for item in trilhas_raw]

    def listar_todas(self) -> List[Trilha]:
        """Retorna todas as trilhas cadastradas."""
        return self._trilhas

    def listar_resumo_tecnologias(self) -> List[Dict[str, Any]]:
        """Retorna um resumo leve com id, slug, nome e carga horária de cada trilha."""
        return [
            {
                "id": t.id,
                "slug": t.slug,
                "nome": t.nome,
                "categoria": t.categoria,
                "carga_horaria_horas": t.carga_horaria_horas,
                "total_modulos": len(t.modulos),
                "total_desafios": len(t.desafios)
            }
            for t in self._trilhas
        ]

    def obter_por_identificador(self, termo: str) -> Optional[Trilha]:
        """
        Busca uma trilha por ID exato, slug exato ou aproximação no nome/slug.
        Exemplos de busca: 'ibm-bob', 'python', 'java', 'devops', 'typescript', 'agentic'.
        """
        if not termo:
            return None

        termo_clean = termo.strip().lower()

        # 1. Correspondência exata por id ou slug
        for t in self._trilhas:
            if t.id.lower() == termo_clean or t.slug.lower() == termo_clean:
                return t

        # 2. Correspondência parcial no slug ou id
        for t in self._trilhas:
            if termo_clean in t.slug.lower() or termo_clean in t.id.lower():
                return t

        # 3. Correspondência parcial no nome ou categoria
        for t in self._trilhas:
            if termo_clean in t.nome.lower() or termo_clean in t.categoria.lower():
                return t

        return None

    def buscar_por_termo(self, termo: str) -> List[Trilha]:
        """Retorna todas as trilhas que contêm o termo informado no nome ou descrição."""
        if not termo:
            return self._trilhas

        termo_clean = termo.strip().lower()
        return [
            t for t in self._trilhas
            if termo_clean in t.nome.lower()
            or termo_clean in t.slug.lower()
            or termo_clean in t.descricao.lower()
            or termo_clean in t.categoria.lower()
        ]
