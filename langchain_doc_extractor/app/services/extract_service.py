import asyncio
from app.components.preprocessor import PDFPreprocessor
from app.components.extractor import GPTExtractor
from app.components.output_handler import JSONHandler
from app.schemas.file_data import FileData
from app.utils.logger import log_all_methods


@log_all_methods
class ExtractService:
    def __init__(self):
        self.preprocessor = PDFPreprocessor()
        self.output_handler = JSONHandler()

    async def extract_document(self, filedata: FileData, prompt_name: str) -> dict:
        if filedata.content_type == "application/pdf":
            return await self.extract_document_pdf(filedata, prompt_name)
        elif filedata.content_type in ("image/png", "image/jpeg"):
            return self.extract_document_img(filedata, prompt_name)
        else:
            raise ValueError(f"Unsupported content type: {filedata.content_type}")

    async def extract_document_pdf(self, filedata: FileData, prompt_name: str) -> dict:
        # 텍스트 추출 + filename prefix 포함
        text = self.preprocessor.preprocess_text(filedata)
        extractor = GPTExtractor(prompt_name=prompt_name)
        result = await extractor.extract(({"text": text, "filename": filedata.filename}))
        return self.output_handler.parse(result['result'])

    def extract_document_img(self, filedata: FileData, prompt_name: str) -> dict:
        raise NotImplementedError("Image support not implemented yet")

    async def extract_document_bulk(self, filedata_list: list[FileData], prompt_name: str) -> list[dict]:
        pdf_files = [f for f in filedata_list if f.content_type == "application/pdf"]
        img_files = [f for f in filedata_list if f.content_type in ("image/png", "image/jpeg")]

        # PDF bulk extraction
        if img_files:
            raise NotImplementedError("Image bulk extraction is not supported yet.")
            # return await self.extract_document_img_bulk(img_files, prompt_name)
        if pdf_files:
            return await self.extract_document_pdf_bulk(pdf_files, prompt_name)
        if not pdf_files and not img_files:
            raise ValueError("No supported files found in the input list.")


    async def extract_document_pdf_bulk(self, filedata_list: list[FileData], prompt_name: str) -> list[dict]:
        extractor = GPTExtractor(prompt_name=prompt_name)

        # asynchronous processing
        texts = await self.preprocessor.preprocess_text_batch_parallel(filedata_list)

        inputs = [
            {"text": text, "filename": filedata.filename}
            for text, filedata in zip(texts, filedata_list)
        ]

        raw_results = await extractor.extract_batch_parallel(inputs) 

        return [
            {
                "filename": item["filename"],
                "result": self.output_handler.parse(item["result"])
            }
            for item in raw_results
        ]
