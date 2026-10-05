"""
Interface de Linha de Comando (CLI) do Geo-Explorer.
Navegação em trilhas de estudos, desafios práticos e emissão de certificados.
"""
import sys
import argparse
from typing import Optional

# Garante suporte a UTF-8 no terminal Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.prompt import Prompt

from src.services.track_service import TrackService
from src.services.challenge_service import ChallengeService
from src.services.certificate_service import CertificateService

console = Console(force_terminal=True, legacy_windows=False)


def render_banner() -> None:
    """Exibe o cabeçalho estilizado do Geo-Explorer."""
    banner_text = Text(
        "🚀 GEO-EXPLORER — Trilhas de Aprendizagem & Desafios Técnicos",
        style="bold cyan",
        justify="center"
    )
    console.print(Panel(banner_text, border_style="bright_blue"))


def cmd_listar(track_service: TrackService) -> None:
    """Lista todas as tecnologias e trilhas disponíveis."""
    trilhas = track_service.listar_todas()
    
    table = Table(
        title="📚 Catálogo de Trilhas Disponíveis",
        border_style="blue",
        header_style="bold magenta"
    )
    table.add_column("Slug (Comando)", style="cyan", no_wrap=True)
    table.add_column("Nome da Trilha", style="white")
    table.add_column("Categoria", style="yellow")
    table.add_column("Carga Horária", justify="center", style="green")
    table.add_column("Módulos", justify="center", style="dim")

    for t in trilhas:
        table.add_row(
            t.slug,
            t.nome,
            t.categoria,
            f"{t.carga_horaria_horas}h",
            str(len(t.modulos))
        )

    console.print(table)
    console.print(
        "\n[dim]Para ver o plano detalhado de uma trilha: "
        "[bold cyan]python -m src.cli trilha <slug>[/bold cyan][/dim]\n"
    )


def cmd_trilha(track_service: TrackService, tecnologia: Optional[str] = None) -> None:
    """Apresenta o plano de estudos detalhado de uma tecnologia."""
    if not tecnologia:
        cmd_listar(track_service)
        tecnologia = Prompt.ask("[bold yellow]Digite o nome ou slug da tecnologia desejada[/bold yellow]")

    trilha = track_service.obter_por_identificador(tecnologia)
    if not trilha:
        console.print(
            f"[bold red]❌ Trilha não encontrada para '{tecnologia}'.[/bold red]\n"
            f"[yellow]Use o comando [bold cyan]listar[/bold cyan] para ver as opções disponíveis.[/yellow]"
        )
        return

    # Cabeçalho da Trilha
    header = (
        f"[bold white]{trilha.nome}[/bold white]\n"
        f"[dim]{trilha.descricao}[/dim]\n\n"
        f"🏷️  [bold]Categoria:[/bold] {trilha.categoria}  |  "
        f"⏱️  [bold]Carga Horária:[/bold] {trilha.carga_horaria_horas}h  |  "
        f"🎯  [bold]Módulos:[/bold] {len(trilha.modulos)}"
    )
    console.print(Panel(header, title="📖 Plano de Estudos", border_style="cyan"))

    # Módulos
    for mod in trilha.modulos:
        mod_text = f"[bold green]Módulo {mod.ordem}: {mod.titulo}[/bold green] ({mod.duracao_horas}h)\n"
        for topico in mod.topicos:
            mod_text += f"  • {topico}\n"
        console.print(Panel(mod_text.strip(), border_style="dim blue"))

    # Desafios disponíveis
    if trilha.desafios:
        desafios_table = Table(
            title="⚡ Desafios Práticos desta Trilha",
            border_style="yellow",
            header_style="bold yellow"
        )
        desafios_table.add_column("Nível", style="bold", width=14)
        desafios_table.add_column("Título do Desafio", style="white")
        
        for d in trilha.desafios:
            cor_nivel = {
                "iniciante": "[green]Iniciante[/green]",
                "intermediario": "[yellow]Intermediário[/yellow]",
                "avancado": "[red]Avançado[/red]"
            }.get(d.nivel.lower(), d.nivel)
            desafios_table.add_row(cor_nivel, d.titulo)
        
        console.print(desafios_table)
        console.print(
            f"\n[dim]Para gerar um desafio prático: "
            f"[bold cyan]python -m src.cli desafio {trilha.slug} <iniciante|intermediario|avancado>[/bold cyan][/dim]\n"
        )


def cmd_desafio(
    challenge_service: ChallengeService,
    tecnologia: Optional[str] = None,
    nivel: Optional[str] = None
) -> None:
    """Gera um desafio de código conforme tecnologia e nível informados."""
    if not tecnologia:
        cmd_listar(challenge_service.track_service)
        tecnologia = Prompt.ask("[bold yellow]Escolha a tecnologia para o desafio[/bold yellow]")

    if not nivel:
        nivel = Prompt.ask(
            "[bold yellow]Escolha o nível de senioridade[/bold yellow]",
            choices=["iniciante", "intermediario", "avancado"],
            default="iniciante"
        )

    try:
        resultado = challenge_service.gerar_desafio(tecnologia, nivel)
        d = resultado.desafio

        cor_borda = {
            "iniciante": "green",
            "intermediario": "yellow",
            "avancado": "red"
        }.get(d.nivel.lower(), "blue")

        corpo = (
            f"[bold white]{d.titulo}[/bold white]\n\n"
            f"[bold cyan]Descrição da Demanda:[/bold cyan]\n{d.descricao}\n\n"
            f"[bold cyan]Critérios de Aceite:[/bold cyan]\n"
        )
        for c in d.criterios_aceite:
            corpo += f"  ☑ {c}\n"

        if d.dica:
            corpo += f"\n💡 [bold yellow]Dica Técnica:[/bold yellow] [dim]{d.dica}[/dim]"

        console.print(
            Panel(
                corpo,
                title=f"💻 Desafio de Código • {resultado.trilha_nome} [{d.nivel.upper()}]",
                border_style=cor_borda
            )
        )
        console.print(
            "\n[dim]Ao concluir, você pode emitir seu certificado com: "
            f"[bold cyan]python -m src.cli certificado \"Seu Nome\" {resultado.tecnologia}[/bold cyan][/dim]\n"
        )

    except ValueError as e:
        console.print(f"[bold red]❌ Erro ao gerar desafio:[/bold red] {e}")


def cmd_certificado(
    certificate_service: CertificateService,
    aluno: Optional[str] = None,
    tecnologia: Optional[str] = None
) -> None:
    """Emite um certificado fictício para a trilha concluída."""
    if not aluno:
        aluno = Prompt.ask("[bold yellow]Digite o nome completo do(a) estudante[/bold yellow]")

    if not tecnologia:
        cmd_listar(certificate_service.track_service)
        tecnologia = Prompt.ask("[bold yellow]Digite a tecnologia concluída[/bold yellow]")

    try:
        cert = certificate_service.emitir_certificado(aluno, tecnologia)

        corpo = (
            f"[bold green]✨ PARABÉNS! CERTIFICADO EMITIDO COM SUCESSO ✨[/bold green]\n\n"
            f"👤  [bold]Estudante:[/bold] {cert.aluno_nome}\n"
            f"🎓  [bold]Especialização:[/bold] {cert.trilha_nome}\n"
            f"⏱️   [bold]Carga Horária:[/bold] {cert.carga_horaria_horas} horas\n"
            f"📅  [bold]Data de Emissão:[/bold] {cert.data_emissao}\n"
            f"🔑  [bold]Código de Autenticidade:[/bold] [bold cyan]{cert.codigo_validacao}[/bold cyan]\n"
            f"🔒  [bold]Hash SHA-256:[/bold] [dim]{cert.hash_seguranca}[/dim]\n\n"
            f"📄  [bold]Arquivo TXT (Terminal):[/bold] [dim]{cert.caminho_txt}[/dim]\n"
            f"🌐  [bold]Arquivo HTML (Web/PDF):[/bold] [dim]{cert.caminho_html}[/dim]"
        )

        console.print(Panel(corpo, title="🏆 Certificado Oficial Geo-Explorer", border_style="gold1"))
        console.print(
            "\n[dim]Para validar a autenticidade deste certificado a qualquer momento:\n"
            f"[bold cyan]python -m src.cli verificar {cert.codigo_validacao}[/bold cyan][/dim]\n"
        )

    except ValueError as e:
        console.print(f"[bold red]❌ Erro ao emitir certificado:[/bold red] {e}")


def cmd_verificar(certificate_service: CertificateService, codigo: Optional[str] = None) -> None:
    """Valida a autenticidade de um certificado emitido."""
    if not codigo:
        codigo = Prompt.ask("[bold yellow]Informe o código de validação ou hash do certificado[/bold yellow]")

    validacao = certificate_service.validar_certificado(codigo)

    if validacao.valido and validacao.certificado:
        c = validacao.certificado
        corpo = (
            f"[bold green]✅ {validacao.mensagem}[/bold green]\n\n"
            f"👤  [bold]Estudante Titular:[/bold] {c.aluno_nome}\n"
            f"🎓  [bold]Trilha Concluída:[/bold] {c.trilha_nome}\n"
            f"⏱️   [bold]Carga Horária:[/bold] {c.carga_horaria_horas} horas\n"
            f"📅  [bold]Emitido em:[/bold] {c.data_emissao}\n"
            f"🔑  [bold]Código Registrado:[/bold] {c.codigo_validacao}\n"
            f"🔒  [bold]Hash Verificado:[/bold] [dim]{c.hash_seguranca}[/dim]"
        )
        console.print(Panel(corpo, title="🔍 Validação de Certificado", border_style="green"))
    else:
        corpo = f"[bold red]❌ FALHA NA VALIDAÇÃO[/bold red]\n\n{validacao.mensagem}"
        console.print(Panel(corpo, title="🔍 Validação de Certificado", border_style="red"))


def menu_interativo() -> None:
    """Modo interativo com navegação guiada por opções."""
    track_service = TrackService()
    challenge_service = ChallengeService(track_service)
    certificate_service = CertificateService(track_service)

    while True:
        render_banner()
        console.print("[bold cyan]Escolha uma das opções abaixo:[/bold cyan]")
        console.print("  [bold 1]1[/bold 1]. 📚 Consultar Trilha de Estudos ([bold cyan]trilha[/bold cyan])")
        console.print("  [bold 2]2[/bold 2]. ⚡ Gerar Desafio de Código ([bold cyan]desafio[/bold cyan])")
        console.print("  [bold 3]3[/bold 3]. 🏆 Emitir Certificado Fictício ([bold cyan]certificado[/bold cyan])")
        console.print("  [bold 4]4[/bold 4]. 🔍 Validar Autenticidade de Certificado ([bold cyan]verificar[/bold cyan])")
        console.print("  [bold 5]5[/bold 5]. 📋 Listar Todas as Tecnologias ([bold cyan]listar[/bold cyan])")
        console.print("  [bold 0]0[/bold 0]. 🚪 Sair\n")

        escolha = Prompt.ask("[bold yellow]Opção desejada[/bold yellow]", choices=["1", "2", "3", "4", "5", "0"])

        if escolha == "1":
            cmd_trilha(track_service)
        elif escolha == "2":
            cmd_desafio(challenge_service)
        elif escolha == "3":
            cmd_certificado(certificate_service)
        elif escolha == "4":
            cmd_verificar(certificate_service)
        elif escolha == "5":
            cmd_listar(track_service)
        elif escolha == "0":
            console.print("[bold green]Obrigado por utilizar o Geo-Explorer! Bons estudos! 🚀[/bold green]")
            break

        console.print("\n[dim]Pressione ENTER para continuar...[/dim]")
        input()


def main() -> None:
    """Ponto de entrada da CLI com suporte a argumentos ou menu interativo."""
    parser = argparse.ArgumentParser(
        prog="geo-explorer",
        description="Geo-Explorer: Plataforma de Trilhas de Aprendizagem, Desafios Práticos e Certificação"
    )

    subparsers = parser.add_subparsers(dest="comando", help="Comandos disponíveis")

    # trilha
    p_trilha = subparsers.add_parser("trilha", help="Consulta o plano de estudos de uma tecnologia")
    p_trilha.add_argument("tecnologia", nargs="?", default=None, help="Slug ou nome da tecnologia (ex: ibm-bob, python)")

    # desafio
    p_desafio = subparsers.add_parser("desafio", help="Gera um desafio prático de código")
    p_desafio.add_argument("tecnologia", nargs="?", default=None, help="Slug ou nome da tecnologia (ex: python, devops)")
    p_desafio.add_argument("nivel", nargs="?", default=None, help="Nível: iniciante, intermediario ou avancado")

    # certificado
    p_cert = subparsers.add_parser("certificado", help="Gera certificado de conclusão de trilha")
    p_cert.add_argument("aluno", nargs="?", default=None, help="Nome do(a) estudante")
    p_cert.add_argument("tecnologia", nargs="?", default=None, help="Slug ou nome da tecnologia")

    # verificar
    p_verif = subparsers.add_parser("verificar", help="Valida autenticidade de certificado emitido")
    p_verif.add_argument("codigo", nargs="?", default=None, help="Código de validação ou hash do certificado")

    # listar
    subparsers.add_parser("listar", help="Lista todas as tecnologias e trilhas cadastradas")

    args = parser.parse_args()

    if not args.comando:
        # Se nenhum comando for passado via terminal, entra no menu interativo
        menu_interativo()
        return

    track_service = TrackService()
    challenge_service = ChallengeService(track_service)
    certificate_service = CertificateService(track_service)

    if args.comando == "listar":
        cmd_listar(track_service)
    elif args.comando == "trilha":
        cmd_trilha(track_service, args.tecnologia)
    elif args.comando == "desafio":
        cmd_desafio(challenge_service, args.tecnologia, args.nivel)
    elif args.comando == "certificado":
        cmd_certificado(certificate_service, args.aluno, args.tecnologia)
    elif args.comando == "verificar":
        cmd_verificar(certificate_service, args.codigo)


if __name__ == "__main__":
    main()
