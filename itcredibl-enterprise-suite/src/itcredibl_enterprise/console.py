from rich.box import ROUNDED
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


def header(title: str):
    console.rule(f"[bold cyan]{title}")


def kv_table(mapping: dict, title: str = ""):
    t = Table(title=title or "Details", box=ROUNDED)
    t.add_column("Key", style="bold dim")
    t.add_column("Value")
    for k, v in mapping.items():
        t.add_row(str(k), str(v))
    console.print(t)


def box(text: str, title: str = "Output"):
    console.print(Panel.fit(text, title=title, border_style="cyan"))
