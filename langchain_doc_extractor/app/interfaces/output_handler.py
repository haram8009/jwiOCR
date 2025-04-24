from abc import ABC, abstractmethod

class BaseOutputHandler(ABC):
    @abstractmethod
    def save(self, data: dict, path: str):
        pass
