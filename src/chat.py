"""CLI para interação com o sistema RAG usando Rich."""

import sys
from pathlib import Path

# Adicionar diretório raiz ao path para imports
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from langchain.messages import HumanMessage
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from src.config import get_settings
from src.prompts import format_rag_prompt
from src.search import search_documents_for_question
from src.services.llm import get_llm

console = Console()


def main():
    """Função principal do CLI."""
    settings = get_settings()
    llm = get_llm(settings)
    
    # Header
    console.print("\n[bold blue]╔═══════════════════════════════════════════════════════════╗[/bold blue]")
    console.print("[bold blue]║[/bold blue]  [bold cyan]Sistema de Busca Semântica RAG[/bold cyan]                       [bold blue]║[/bold blue]")
    console.print("[bold blue]╚═══════════════════════════════════════════════════════════╝[/bold blue]\n")
    console.print("Digite '[bold yellow]sair[/bold yellow]', '[bold yellow]exit[/bold yellow]' ou '[bold yellow]quit[/bold yellow]' para encerrar\n")
    
    while True:
        try:
            # Solicitar pergunta do usuário
            question = Prompt.ask("[bold cyan]💬 Pergunta[/bold cyan]")
            
            if question.lower().strip() in ['sair', 'exit', 'quit']:
                console.print("\n[bold green]Até logo! 👋[/bold green]\n")
                break
            
            if not question.strip():
                console.print("[bold yellow]⚠️  Por favor, digite uma pergunta válida.[/bold yellow]\n")
                continue
            
            # Buscar contexto
            with console.status("[bold green]🔍 Buscando informações no banco de dados...[/bold green]", spinner="dots"):
                contexto = search_documents_for_question(question)
            
            if not contexto:
                console.print(
                    Panel(
                        "[bold yellow]Nenhum documento relevante foi encontrado no banco de dados.[/bold yellow]",
                        title="[bold yellow]⚠️  Aviso[/bold yellow]",
                        border_style="yellow"
                    )
                )
                console.print()
                continue
            
            # Montar prompt
            prompt = format_rag_prompt(contexto, question)
            
            # Processar resposta com LLM
            with console.status("[bold green]🤖 Processando resposta com IA...[/bold green]", spinner="dots"):
                response = llm.invoke([HumanMessage(content=prompt)])
            
            # Exibir resposta
            console.print(
                Panel(
                    response.content,
                    title="[bold green]✅ Resposta[/bold green]",
                    border_style="green",
                    padding=(1, 2)
                )
            )
            console.print()
            
        except KeyboardInterrupt:
            console.print("\n\n[bold yellow]Interrompido pelo usuário.[/bold yellow]")
            console.print("[bold green]Até logo! 👋[/bold green]\n")
            break
        except Exception as e:
            console.print(
                Panel(
                    f"[bold red]Erro: {str(e)}[/bold red]",
                    title="[bold red]❌ Erro[/bold red]",
                    border_style="red"
                )
            )
            console.print()


if __name__ == "__main__":
    main()
