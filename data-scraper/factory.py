from logger import Logger

class LoggerFactory:
    _loggers = {}
    
    @classmethod
    def get_logger(cls, name: str) -> Logger:
        if name not in cls._loggers:
            cls._loggers[name] = Logger(name)
        return cls._loggers[name]