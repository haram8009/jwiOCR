import fitz
import pytesseract
from PIL import Image
import io
from app.interfaces.preprocessor import BasePreprocessor


class PDFPreprocessor(BasePreprocessor):
    def extract_text(self, file_path: str, use_ocr: bool = True) -> str:
        doc = fitz.open(file_path)
        full_text = ""
        for page in doc:
            if not use_ocr:
                text = page.get_text()
                full_text += text if text.strip() else ""
            if use_ocr or not text.strip():
                pix = page.get_pixmap(dpi=300)
                img = Image.open(io.BytesIO(pix.tobytes("png")))
                full_text += pytesseract.image_to_string(img)
        doc.close()
        print("Extracted text from PDF:", full_text)  # Debugging line to check extracted text
        return full_text
