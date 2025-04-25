from .base_preprocessor import BasePreprocessor
import fitz
import pytesseract
from PIL import Image
import io
import asyncio

from app.schemas.file_data import FileData
from app.utils.logger import log_all_methods

@log_all_methods
class PDFPreprocessor(BasePreprocessor):    
    def preprocess_text(self, file_data: FileData) -> str:
        return self.preprocess_text_from_bytes(file_data.contents)

    def preprocess_text_from_bytes(self, file_bytes: bytes, use_ocr: bool = False) -> str:
        with fitz.open(stream=file_bytes, filetype="pdf") as doc:
            return self._preprocess_text_from_doc(doc, use_ocr)
        
    def _preprocess_text_from_doc(self, doc, use_ocr: bool) -> str:
        full_text = ""
        for page in doc:
            text = page.get_text()
            if not use_ocr:
                full_text += text if text.strip() else ""
            if use_ocr or not text.strip():
                pix = page.get_pixmap(dpi=300)
                img = Image.open(io.BytesIO(pix.tobytes("png")))
                full_text += pytesseract.image_to_string(img)
        return full_text
    
    async def preprocess_text_batch_parallel(self, filedata_list: list[FileData]) -> list[str]:
        texts = await asyncio.gather(*[
            asyncio.to_thread(self.preprocess_text, filedata) 
            for filedata in filedata_list
        ])
        return texts
