from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from rich.progress import Progress
from curl_cffi import requests

class BaseTester:
    def __init__(self):
        self.console = Console(record=True)
        self.parser = None
        
    def _make_request(self, url: str, headers: dict):
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            self.console.print(Panel(
                f"[bold red]✖ Request Failed[/]\nStatus: {response.status_code}\nURL: {url}",
                style="red",
                title="HTTP Error",
                title_align="left"
            ))
            return None
        return response

    def print_section(self, title: str, style: str = "bold cyan on black", emoji: str = "🚀"):
        self.console.print(Panel.fit(f"{emoji} {title}", style=style, padding=(0, 2)))

    def print_table(self, headers: list, rows: list, title: str):
        table = Table(
            title=f"📊 {title}",
            title_style="bold magenta",
            header_style="bold blue",
            box=None,
            show_header=True,
            expand=True
        )
        for header in headers:
            table.add_column(header, style="cyan")
        for row in rows:
            table.add_row(*[str(item) for item in row])
        self.console.print(table)

    def print_key_value(self, key: str, value: str):
        self.console.print(f"➤ [bold green]{key}:[/] [yellow]{value}[/yellow]")

    def print_markdown(self, content: str, title: str):
        self.console.print(Panel(
            Markdown(content),
            title=f"📝 {title}",
            title_align="left",
            style="dim",
            padding=(1, 4)
        ))

    def run_tests(self, url: str, test_functions: list):
        self.print_section("Starting Automated Tests", "bold white on dark_blue", "🤖")
        self.console.print(f"🔗 Testing URL: [link]{url}[/link]\n")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
        }
        
        with Progress(transient=True) as progress:
            task = progress.add_task("[cyan]Fetching URL...", total=1)
            response = self._make_request(url, headers)
            progress.update(task, advance=1)
            
        if not response:
            return
            
        soup = self.parser.get_soup(response.text)
        self.print_section("Testing Product Fields", "bold blue on black", "🧪")
        
        success_count = 0
        failure_count = 0
        
        for test_fn in test_functions:
            try:
                test_fn(soup)
                success_count += 1
            except Exception as e:
                failure_count += 1
                self.console.print(Panel(
                    f"[bold red]✖ {type(e).__name__}:[/] {str(e)}",
                    style="red",
                    title="Test Failure",
                    title_align="left"
                ))
                self.console.print(f"[dim]{'-'*40}[/dim]")
        
        self.print_section(
            f"Tests Complete: [green]{success_count} passed[/green], [red]{failure_count} failed[/red]",
            "bold white on dark_green" if failure_count == 0 else "bold white on dark_red",
            "🛡️" if failure_count == 0 else "⚠️"
        )
