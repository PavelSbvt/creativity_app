from rich.console import Console
from rich.panel import Panel
import shutil


console = Console(width=200)

def log_error(message: str, details: str = "") -> None:
    """
    Вывод ошибки с панелью
    """

    content = f"[bold white on red] ⚠️ ОШИБКА ⚠️ [/bold white on red]\n\n{message}"
    if details:
        content += f"\n\n[dim]{details}[/dim]"

    console.print(
        Panel(
            content,
            title="[red]Ошибка[/red]",
            border_style="red",
            padding=(1, 2)
        )
    )

def simple_log(message: str) -> None:
    """
    Логгирование с rich
    :param message:
    :return: None
    """

    console.log(f"[green]{message}[/green]")

def debug_log(message: str) -> None:
    """
    доггирование с rich, созданное для дебага
    :param message:
    :return:
    """

    console.log(f"[grey46][Debug] {message}[/grey46]")

# debug_log(f"Ширина консоли: {shutil.get_terminal_size().columns}")