from abc import ABC, abstractmethod

class BasePreprocessor(ABC):
    @abstractmethod
    def extract_text(self, file_path: str) -> str:
        pass
