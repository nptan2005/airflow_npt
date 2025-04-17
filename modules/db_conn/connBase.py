from abc import ABC, abstractmethod


class ConnBase(ABC):

    def __init__(self, ConnectionName:str = None):
    
        super().__init__()

        if ConnectionName is None:
            raise ValueError("ConnectionName cannot be None")

        
        
    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __del__(self):
        """"""
        pass
    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
        

    

    @property
    @abstractmethod
    def connection(self):
        pass
    

    
    @property
    @abstractmethod
    def commit(self):
        pass

    @property
    @abstractmethod
    def close(self):
        pass

    
            
    