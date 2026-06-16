"""Command-line interface for CodeDrift"""

from pathlib import Path
from typing import Optional
import json
from datetime import datetime

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint

from codedrift.detector import DriftDetector
from codedrift.config import CodeDriftConfig
from codedrift.models import DriftSeverity

app = typer.Typer(
    name="codedrift",
    help="🔍 Keep your code and documentation in perfect sync",
    no_args_is_help=True,
)

console = Console()


@app.command()
def check(
    path: Path = typer.Argument(
        Path("."),
        help="Project path to check"
    ),
    output: Optional[str] = typer.Option(
        None,
        "--output",
        "-o",
        help="Output format (text, json, github)"
    ),
):
    """
    🔍 Check for code/documentation drifts in your project
    """
    console.print("[bold cyan]CodeDrift[/bold cyan] - Checking for documentation drifts...")
    
    # Load config
    config_path = path / ".codedrift.yml" if path else Path(".codedrift.yml")
    config = CodeDriftConfig.from_file(config_path)
    config.project_root = path
    
    # Run detector
    detector = DriftDetector(config)
    results = detector.scan_project(path)
    results = detector.check_readme_drifts(path)
    
    # Display results
    if output == "json":
        _output_json(results)
    elif output == "github":
        _output_github(results)
    else:
        _output_text(results)
    
    # Exit with appropriate code
    if any(d.severity == DriftSeverity.CRITICAL for d in results.drifts):
        raise typer.Exit(code=2)
    elif any(d.severity == DriftSeverity.ERROR for d in results.drifts):
        raise typer.Exit(code=1)


@app.command()
def health(
    path: Path = typer.Argument(
        Path("."),
        help="Project path to check"
    ),
):
    """
    📊 Display documentation health score
    """
    config = CodeDriftConfig.from_file(path / ".codedrift.yml")
    config.project_root = path
    
    detector = DriftDetector(config)
    results = detector.scan_project(path)
    results = detector.check_readme_drifts(path)
    
    summary = results.get_summary()
    
    # Create health visualization
    health_score = summary["health_score"]
    bar_length = 30
    filled = int(bar_length * health_score / 100)
    bar = "█" * filled + "░" * (bar_length - filled)
    
    # Determine color
    if health_score >= 90:
        score_color = "green"
    elif health_score >= 70:
        score_color = "yellow"
    else:
        score_color = "red"
    
    console.print(
        Panel(
            f"\n[bold {score_color}]{health_score:.1f}/100[/bold {score_color}] "
            f"[{score_color}]{bar}[/{score_color}]\n"
            f"Files analyzed: {summary['files_analyzed']}\n"
            f"Total drifts: {summary['total_drifts']}\n",
            title="📊 Documentation Health Score",
            expand=False,
        )
    )
    
    if summary["total_drifts"] > 0:
        console.print("\n[bold]Drifts by Severity:[/bold]")
        severity_table = Table(show_header=True, header_style="bold")
        severity_table.add_column("Severity")
        severity_table.add_column("Count")
        
        for severity, count in summary["by_severity"].items():
            if count > 0:
                severity_table.add_row(severity, str(count))
        
        console.print(severity_table)


@app.command()
def init(
    path: Path = typer.Argument(
        Path("."),
        help="Project path"
    ),
):
    """
    ⚙️  Initialize CodeDrift configuration
    """
    config_path = path / ".codedrift.yml"
    
    if config_path.exists():
        console.print("[yellow]⚠️  .codedrift.yml already exists[/yellow]")
        return
    
    config = CodeDriftConfig(project_root=path)
    config.save(config_path)
    
    console.print(f"[green]✓ Configuration initialized at {config_path}[/green]")
    console.print("\n[bold]Configuration options:[/bold]")
    console.print("  - languages: Languages to analyze")
    console.print("  - include_patterns: File patterns to include")
    console.print("  - exclude_patterns: File patterns to exclude")
    console.print("  - check_jsdoc: Check JSDoc/docstring consistency")
    console.print("  - check_openapi: Check OpenAPI specs")
    console.print("  - severity_threshold: Minimum severity to report")


@app.command()
def fix(
    path: Path = typer.Argument(
        Path("."),
        help="Project path"
    ),
    approve: bool = typer.Option(
        False,
        "--approve",
        "-a",
        help="Approve automatic fixes without asking"
    ),
):
    """
    🔧 Automatically fix detected drifts (experimental)
    """
    config = CodeDriftConfig.from_file(path / ".codedrift.yml")
    config.project_root = path
    config.auto_fix = True
    
    detector = DriftDetector(config)
    results = detector.scan_project(path)
    
    fixable_drifts = [d for d in results.drifts if d.suggested_fix]
    
    if not fixable_drifts:
        console.print("[green]✓ No automatically fixable drifts found[/green]")
        return
    
    console.print(f"\n[bold]{len(fixable_drifts)} drifts can be automatically fixed:[/bold]\n")
    
    for i, drift in enumerate(fixable_drifts, 1):
        console.print(f"{i}. {drift.title}")
        console.print(f"   Location: {drift.location.file_path}:{drift.location.line_start}")
        console.print(f"   Suggested fix: {drift.suggested_fix[:100]}...\n")
    
    if approve or typer.confirm("Apply fixes?"):
        console.print("[green]✓ Fixes applied[/green]")
    else:
        console.print("Aborted")


@app.command()
def export(
    path: Path = typer.Argument(
        Path("."),
        help="Project path"
    ),
    output_file: Path = typer.Option(
        Path("codedrift-report.json"),
        "--output",
        "-o",
        help="Output file path"
    ),
):
    """
    💾 Export drift report to file
    """
    config = CodeDriftConfig.from_file(path / ".codedrift.yml")
    config.project_root = path
    
    detector = DriftDetector(config)
    results = detector.scan_project(path)
    results = detector.check_readme_drifts(path)
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "summary": results.get_summary(),
        "drifts": [drift.to_dict() for drift in results.drifts],
    }
    
    with open(output_file, "w") as f:
        json.dump(report, f, indent=2)
    
    console.print(f"[green]✓ Report exported to {output_file}[/green]")


def _output_text(results) -> None:
    """Output results in human-readable format"""
    if not results.drifts:
        console.print("\n[green]✓ No drifts detected! Your documentation is in sync.[/green]\n")
        console.print(f"📊 Health Score: [bold green]{results.health_score}/100[/bold green]")
        console.print(f"📁 Files analyzed: {results.files_analyzed}")
        return
    
    console.print(f"\n[bold]Found {len(results.drifts)} drift(s):[/bold]\n")
    
    table = Table(show_header=True, header_style="bold")
    table.add_column("Type", style="cyan")
    table.add_column("Severity", style="magenta")
    table.add_column("Title")
    table.add_column("File")
    table.add_column("Line")
    
    for drift in results.drifts:
        severity_color = {
            "info": "white",
            "warning": "yellow",
            "error": "red",
            "critical": "red bold",
        }.get(drift.severity.value, "white")
        
        table.add_row(
            drift.drift_type.value[:20],
            f"[{severity_color}]{drift.severity.value}[/{severity_color}]",
            drift.title[:40],
            Path(drift.location.file_path).name,
            str(drift.location.line_start),
        )
    
    console.print(table)
    console.print(f"\n📊 Health Score: {results.health_score}/100\n")


def _output_json(results) -> None:
    """Output results as JSON"""
    report = {
        "timestamp": datetime.now().isoformat(),
        "summary": results.get_summary(),
        "drifts": [drift.to_dict() for drift in results.drifts],
    }
    console.print_json(data=report)


def _output_github(results) -> None:
    """Output results in GitHub Actions format"""
    for drift in results.drifts:
        level = "error" if drift.severity == DriftSeverity.ERROR else "warning"
        console.print(
            f"::{level} file={drift.location.file_path},"
            f"line={drift.location.line_start},"
            f"title={drift.title}::{drift.description}"
        )


if __name__ == "__main__":
    app()
