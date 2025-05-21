from utilities import Logger,Utils
from io import StringIO
import sys
class LoggerStream:
    def __init__(self,is_dump_to_file: bool, is_logger: bool = False):
        self.is_logger = is_logger
        self.is_dump_to_file = is_dump_to_file
        self.log = Logger().logger
        self.buffer = StringIO()
        self.log_message = None
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._clear_attributes()

    def __del__(self):
        self._clear_attributes()

    def _clear_attributes(self):
        """Clear object attributes during exit."""
        self.flush()
        attributes = [
            'is_logger', 'is_dump_to_file',  'log', 'log_message'
        ]
        for attr in attributes:
            setattr(self, attr, None)

    def write(self, message):
        if self.is_logger or self.is_dump_to_file:
            self.buffer.write(message)
            sys.stdout.write(message)
    
    def writeToLog(self):
        if self.is_logger:
            self.log_message = self.buffer.getvalue().strip()
        if self.log_message:
            self.log.info(self.log_message)
            
            
    def writeToFile(self,filePath:str):
        if self.is_dump_to_file:
            self.log_message = self.buffer.getvalue().strip()
        if self.log_message:
            Utils.writeFile(value=self.log_message,filePath=filePath,mode="w")
                
    def flush(self):
        self.buffer = StringIO()