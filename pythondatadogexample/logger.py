from typing import List
from logging import Logger, StreamHandler

class LoggerFactory:
    def create(self, name: str, stream_handlers: List[StreamHandler]) -> Logger:
        logger = Logger(name)
        
        for handler in stream_handlers:
            logger.addHandler(handler)
        
        return logger