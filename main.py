
import argparse
import sys
from pathlib import Path

from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.pretty import pprint

from src.ingestion.codebase_walker import CodebaseWalker
from src.ingestion.ast_parser import PythonASTParser
from src.agents.graph_router import build_audit_graph
from src.reporting.console_reporter import display_audit_report
from src.reporting.exporter import export_report
from src.vector_store.code_indexer import CodebaseVectorStore


console = Console()


def show_banner():
    console.print(
        Panel.fit(
            "[bold cyan]CODEBASE INTELLIGENCE AUDITOR[/bold cyan]\n"
            "[dim]AI-powered codebase analysis and architecture auditing[/dim]",
            border_style="cyan"
        )
    )


def get_arguments():
    parser = argparse.ArgumentParser(
        description="AI-powered codebase intelligence and auditing tool."
    )

    parser.add_argument(
        "--path",
        type=Path,
        default=Path("."),
        help="Path to the repository to analyze."
    )

    parser.add_argument(
        "--mode",
        choices=["audit", "ask"],
        help="Operation to perform: full audit or ask a codebase question."
    )

    parser.add_argument(
        "--query",
        type=str,
        help="Question to ask about the codebase (used with ask mode)."
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=Path("audit_report.json"),
        help="Path where the audit report will be exported."
    )

    parser.add_argument(
        "--show-graph",
        action="store_true",
        help="Display the LangGraph workflow."
    )

    return parser.parse_args()


def get_user_input(args):
    """Collect operation and query from CLI arguments or interactive input."""

    mode = args.mode

    if mode is None:
        console.print("\n[bold]Select an operation:[/bold]")
        console.print("  [cyan]1.[/cyan] Full codebase audit")
        console.print("  [cyan]2.[/cyan] Ask a question about the codebase")

        choice = Prompt.ask(
            "\nSelect an option",
            choices=["1", "2"],
            default="1"
        )

        mode = "audit" if choice == "1" else "ask"

    query = args.query

    if mode == "ask" and not query:
        query = Prompt.ask("\nWhat would you like to know about the codebase?")

    if mode == "audit":
        query = (
            "Perform a comprehensive codebase audit. "
            "Analyze architecture, code quality, and security."
        )

    return mode, query


def prepare_codebase(target_dir: Path):
    """Scan the repository and extract Python AST metadata."""

    console.print(f"\n[bold]Repository:[/bold] {target_dir.resolve()}")

    walker = CodebaseWalker(str(target_dir))
    parser = PythonASTParser()

    with console.status("[cyan]Scanning repository...[/cyan]"):
        files = walker.build_file_tree()

    console.print(f"[green]✓[/green] Found {len(files)} files.")

    python_files = [
        file for file in files
        if file.get("extension") == "py"
    ]

    if not python_files:
        raise ValueError("No Python files found in the repository.")

    parsed_data = []

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:

        task = progress.add_task(
            "Parsing Python files...",
            total=len(python_files)
        )

        for file in python_files:
            code = walker.read_file(file["relative_path"])

            ast_metadata = parser.parse_code(
                code,
                file["relative_path"]
            )

            parsed_data.append(ast_metadata)
            progress.advance(task)

    console.print(
        f"[green]✓[/green] Parsed {len(parsed_data)} Python files."
    )

    return walker, files, parsed_data


def build_initial_state(
    target_dir: Path,
    files: list,
    parsed_data: list,
    query: str
):
    return {
        "target_dir": str(target_dir.resolve()),
        "file_tree": files,
        "parsed_ast": parsed_data,
        "findings": [],
        "current_node": "entry",
        "user_query": query,
        "route": "",
        "router_reasoning": "",
        "rag_response": {},
        "retrieved_matches": []
    }


def run_ingestion(args):
    target_dir = args.path.resolve()

    if not target_dir.exists() or not target_dir.is_dir():
        raise ValueError(f"Invalid repository path: {target_dir}")

    mode, query = get_user_input(args)

    walker, files, parsed_data = prepare_codebase(target_dir)

    with console.status("[cyan]Indexing codebase...[/cyan]"):
        vector_store = CodebaseVectorStore()
        vector_store.index_parsed_ast(parsed_data, walker)

    console.print("[green]✓[/green] Codebase indexed successfully.")

    initial_state = build_initial_state(
        target_dir,
        files,
        parsed_data,
        query
    )

    app = build_audit_graph()

    if args.show_graph:
        console.print("\n[bold]Workflow graph:[/bold]")
        app.get_graph().print_ascii()

    with console.status(
        "[bold cyan]Running AI agents...[/bold cyan]"
    ):
        final_state = app.invoke(initial_state)

    if mode == "audit":
        display_audit_report(final_state)

        export_report(
            final_state,
            output_path=str(args.output)
        )

        console.print(
            f"\n[green]✓ Audit report saved to {args.output}[/green]"
        )

    else:
        console.print("\n[bold cyan]RAG Response[/bold cyan]")
        pprint(final_state.get("rag_response", {}))


def main():
    args = get_arguments()
    

    show_banner()

    try:
        run_ingestion(args)
        console.print("\n[bold green]Operation completed successfully![/bold green]")

    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled.[/yellow]")
        sys.exit(130)

    except Exception as error:
        console.print(
            Panel(
                f"[red]{error}[/red]",
                title="Execution Failed",
                border_style="red"
            )
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
