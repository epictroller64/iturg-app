from rich.console import Console
from rich.theme import Theme

class Logger:
    def __init__(self, name: str):
        self.name = name
        self.console = Console(theme=Theme({
            "info": "green",
            "error": "red",
            "debug": "yellow",
            "warn": "yellow"
        }))

    def info(self, message: str):
        """Log an info level message"""
        self.console.print(f"[info][INFO][/info] {self.name}: {message}")

    def error(self, message: str, error: Exception = None):
        """Log an error level message with optional exception"""
        if error:
            self.console.print(f"[error][ERROR][/error] {self.name}: {message} - {str(error)}")
        else:
            self.console.print(f"[error][ERROR][/error] {self.name}: {message}")

    def debug(self, message: str):
        """Log a debug level message"""
        self.console.print(f"[debug][DEBUG][/debug] {self.name}: {message}")

    def warning(self, message: str):
        """Log a warning level message"""
        self.console.print(f"[warn][WARN][/warn] {self.name}: {message}")
