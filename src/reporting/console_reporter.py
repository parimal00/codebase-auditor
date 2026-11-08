from rich.console import Console
from rich.table import Table

console = Console()

def display_audit_report(final_state: dict):
    console.print("\n[bold cyan]📊 Codebase Audit Report[/bold cyan]\n")
    
    target_dir = final_state.get("target_dir", ".")
    findings = final_state.get("findings", [])
    
    console.print(f"[bold]Target Directory:[/bold] {target_dir}")
    console.print(f"[bold]Total Findings Discovered:[/bold] {len(findings)}\n")
    
    if not findings:
        console.print("[green]✨ No issues found! Clean codebase.[/green]")
        return

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Severity", style="dim", width=10)
    table.add_column("Category", width=15)
    table.add_column("File / Location", width=20)
    table.add_column("Description")

    for f in findings:
        severity = f.get("severity", "info")
        color = "red" if severity == "high" else "yellow" if severity == "medium" else "blue"
        
        table.add_row(
            f"[{color}]{severity.upper()}[/{color}]",
            f.get("category", "general"),
            f.get("file_path", "N/A"),
            f.get("description", "")
        )

    console.print(table)