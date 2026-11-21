from rich.console import Console
from rich.table import Table

console = Console()


def display_audit_report(final_state: dict):
    console.print("\n[bold cyan]📊 Codebase Audit Report[/bold cyan]\n")

    target_dir = final_state.get("target_dir", ".")
    architecture_findings = final_state.get("architecture_findings", [])
    quality_findings = final_state.get("quality_findings", [])
    security_findings = final_state.get("security_findings", [])
    all_findings = final_state.get("findings", [])

    console.print(f"[bold]Target Directory:[/bold] {target_dir}")
    console.print(f"[bold]Total Findings Discovered:[/bold] {len(all_findings)}")
    console.print(
        f"[bold]Architecture:[/bold] {len(architecture_findings)} | "
        f"[bold]Quality:[/bold] {len(quality_findings)} | "
        f"[bold]Security:[/bold] {len(security_findings)}\n"
    )

    def display_findings(title: str, findings: list):
        console.print(f"\n[bold cyan]{title}[/bold cyan]")

        if not findings:
            console.print("[green]No issues found.[/green]")
            return

        table = Table(show_header=True, header_style="bold magenta")

        table.add_column("Severity", width=10)
        table.add_column("Category", width=15)
        table.add_column("Title", width=30)
        table.add_column("File / Location", width=30)
        table.add_column("Description")

        severity_colors = {
            "critical": "bold red",
            "high": "red",
            "medium": "yellow",
            "low": "blue",
        }

        for finding in findings:
            severity = finding.get("severity", "low").lower()
            color = severity_colors.get(severity, "white")

            table.add_row(
                f"[{color}]{severity.upper()}[/{color}]",
                finding.get("category", "general"),
                finding.get("title", "Untitled"),
                finding.get("file_path", "N/A"),
                finding.get("description", ""),
            )

        console.print(table)

    display_findings("📋 Prioritized Audit Findings", all_findings)

    if not all_findings:
        console.print("\n[bold green]✨ No issues found! Clean codebase.[/bold green]")