from colorama import Fore, Style

class Logger:
    def __init__(self, name: str):
        self.name = name
        self.fore = Fore
        self.style = Style

    def info(self, message: str):
        """Log an info level message"""
        print(f"{self.fore.GREEN}[INFO]{self.style.RESET_ALL} {self.name}: {message}")

    def error(self, message: str, error: Exception = None):
        """Log an error level message with optional exception"""
        if error:
            print(f"{self.fore.RED}[ERROR]{self.style.RESET_ALL} {self.name}: {message} - {str(error)}")
        else:
            print(f"{self.fore.RED}[ERROR]{self.style.RESET_ALL} {self.name}: {message}")

    def debug(self, message: str):
        """Log a debug level message"""
        print(f"{self.fore.YELLOW}[DEBUG]{self.style.RESET_ALL} {self.name}: {message}")

    def warning(self, message: str):
        """Log a warning level message"""
        print(f"{self.fore.YELLOW}[WARN]{self.style.RESET_ALL} {self.name}: {message}")
