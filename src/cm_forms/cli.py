import click
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from cm_forms import core

console = Console()

@click.command()
@click.argument("files", nargs=-1, type=click.Path(exists=True, dir_okay=False))
@click.option("--dryrun", is_flag=True, help="Simulate changes and preview diff only.")
def main(files, dryrun):
    """
    cm-forms: A minimalist, CLI HTML form accessibility formatter.
    """
    # 1. Output Notice
    notice_text = Text(
        "NOTICE: This is a pre-alpha planning release (v0.0.1). No guarantees, minimal features live.\n"
        "Visit https://github.com/comfort-mode-toolkit/cm-forms/ to contribute or share feedback.",
        style="bold yellow"
    )
    console.print(Panel(notice_text, title="[cm-forms]", border_style="yellow"))

    if not files:
        console.print("[yellow]No files provided. Usage: cm-forms <htmlfile1> ... [--dryrun][/yellow]")
        return

    # 2. Process Files
    for filepath in files:
        try:
            report = core.process_file(filepath, dryrun=dryrun)
            
            # 3. Output Report
            console.print(f"\n[bold]Processed: {filepath} -> {report['output_path']}[/bold]")
            for change in report['changes']:
                console.print(f"- {change}")
            for warning in report['warnings']:
                console.print(f"- [yellow]WARNING: {warning}[/yellow]")
            
            if dryrun:
                console.print("[dim](Dryrun mode: No files were written)[/dim]")

        except Exception as e:
            console.print(f"[red]Error processing {filepath}: {e}[/red]")

    # 4. Footer
    console.print("\n[dim]For more info and feedback, visit: https://github.com/comfort-mode-toolkit/cm-forms/[/dim]")

if __name__ == "__main__":
    main()
