from .base_preprocessor import BasePreprocessor
import fitz
import pytesseract
from PIL import Image
import io
import asyncio
import logging 
import base64

from app.schemas.file_data import FileData
from app.utils.logger import log_all_methods

@log_all_methods
class PDFPreprocessor(BasePreprocessor):    
    def preprocess_text(self, file_data: FileData) -> str:
        return self.preprocess_text_from_bytes(file_data.contents)

    def preprocess_text_from_bytes(self, file_bytes: bytes) -> str:
        with fitz.open(stream=file_bytes, filetype="pdf") as doc:
            return self._preprocess_text_from_doc(doc)
        
    def _preprocess_text_from_doc(self, doc) -> str:
        logger = logging.getLogger("pdf_preprocessor") # DEBUG
        full_text = ""
        for page in doc:
            text = page.get_text()
            full_text += text if text.strip() else ""
            if not text.strip():
                pix = page.get_pixmap(dpi=300)
                img = Image.open(io.BytesIO(pix.tobytes("png")))
                full_text += pytesseract.image_to_string(img)

        logger.debug(f"full_text:\n{full_text}")
        return full_text
    
    async def preprocess_text_batch_parallel(self, filedata_list: list[FileData]) -> list[str]:
        texts = await asyncio.gather(*[
            asyncio.to_thread(self.preprocess_text, filedata) 
            for filedata in filedata_list
        ])
        return texts
    
    async def preprocess_base64(self, file_data: FileData) -> list[str]:
        """
        Converts each page of a PDF to a base64-encoded PNG image.
        :param file_data: FileData object containing the PDF file
        :return: List of base64-encoded images (one per page)
        """
        return await self.preprocess_base64_from_bytes(file_data.contents)
    
    async def preprocess_base64_from_bytes(self, file_bytes: bytes) -> list[str]:
        """
        Converts each page of a PDF to a base64-encoded PNG image.
        :param file_bytes: PDF file in bytes
        :return: List of base64-encoded images (one per page)
        """
        base64_images = []
        with fitz.open(stream=file_bytes, filetype="pdf") as doc:
            for page in doc:
                # Render page as an image
                pix = page.get_pixmap(dpi=300)
                img_bytes = pix.tobytes("png")

                # Encode image to base64
                base64_str = base64.b64encode(img_bytes).decode('utf-8')
                base64_images.append(f"data:image/png;base64,{base64_str}")
        return base64_images

    async def preprocess_base64_batch_parallel(self, filedata_list: list[FileData]) -> list[list[str]]:
        base64_images = await asyncio.gather(*[
            self.preprocess_base64(filedata)
            for filedata in filedata_list
        ])
        return base64_images