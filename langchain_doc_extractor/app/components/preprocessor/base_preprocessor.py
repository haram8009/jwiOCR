from abc import ABC, abstractmethod
from app.schemas.file_data import FileData

class BasePreprocessor(ABC):
    @abstractmethod
    def extract_text(self, file_data: FileData) -> str:
        pass
