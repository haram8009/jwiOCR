import os
from dotenv import load_dotenv
from openai import OpenAI

from app.components.preprocessor import PDFPreprocessor
from app.components.extractor import GPTExtractor
from app.components.output_handler import JSONHandler
from app.schemas.file_data import FileData
from app.utils.logger import log_all_methods


@log_all_methods
class ExtractService:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.preprocessor = PDFPreprocessor()
        self.output_handler = JSONHandler()

    def extract_document(self, filedata: FileData, prompt_name: str) -> dict:
        if filedata.content_type == "application/pdf":
            return self.extract_document_pdf(filedata, prompt_name)
        elif filedata.content_type in ("image/png", "image/jpeg"):
            return self.extract_document_img(filedata, prompt_name)
        else:
            raise ValueError(f"Unsupported content type: {filedata.content_type}")

    def extract_document_pdf(self, filedata: FileData, prompt_name: str) -> dict:
        # 텍스트 추출 + filename prefix 포함
        text = self.preprocessor.extract_text(filedata)
        extractor = GPTExtractor(api_key=self.api_key, prompt_name=prompt_name)
        result = extractor.extract(text)
        return self.output_handler.parse(result)

    def extract_document_img(self, filedata: FileData, prompt_name: str) -> dict:
        raise NotImplementedError("Image support not implemented yet")

    async def extract_document_bulk(self, filedata_list: list[FileData], prompt_name: str) -> list[dict]:
        extractor = GPTExtractor(api_key=self.api_key, prompt_name=prompt_name)

        inputs = [
            {
                "text": self.preprocessor.extract_text(filedata),
                "filename": filedata.filename
            }
            for filedata in filedata_list
        ]

        raw_results = await extractor.extract_batch(inputs)

        return [
            {
                "filename": item["filename"],
                "result": self.output_handler.parse(item["result"])
            }
            for item in raw_results
        ]
