from logger import Logger

class Error(Exception):
    def __init__(self, message: str, logger: Logger, error: Exception = None):
        self.message = message
        super().__init__(self.message)
        self.logger = logger
        self.error = error 
        self.log()

    def log(self):
        self.logger.error(self.message, self.error)

    def __str__(self):
        return f"{self.message} - {self.error}"
