from pydantic import BaseModel
from typing import Literal

class FileData(BaseModel):
    filename: str
    content_type: Literal["application/pdf", "image/png", "image/jpeg"]
    contents: bytes
