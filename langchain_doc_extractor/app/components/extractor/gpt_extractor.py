import os
import asyncio
import time
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from dotenv import load_dotenv
from app.prompts import prompts
from app.components.extractor.base_extractor import BaseExtractor
from app.utils.logger import log_all_methods
import logging
logger = logging.getLogger(__name__)

@log_all_methods
class GPTExtractor(BaseExtractor):
    def __init__(self, prompt_name: str = "extract_basic"):
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.llm = ChatOpenAI(
            temperature=0,
            model="gpt-4.1-mini",
            openai_api_key=self.api_key
        )
        self.chain = prompts[prompt_name] | self.llm

        self.img_llm = ChatOpenAI(
            temperature=0,
            model="gpt-4o",
            openai_api_key=self.api_key
        )

    async def run_one(self, input : dict) -> dict:
        """
        - input: dict = {
            "text": str, 
            "filename": str        
        }
        - output: dict = {
            "filename": str, 
            "result": str
        }
        """
        start = time.perf_counter()
        res = await self.chain.ainvoke({"text": input["text"]})
        duration = time.perf_counter() - start
        logger.info(f"[GPT] {input['filename']} took {duration:.2f}s")
        return {"filename": input["filename"], "result": res.content}

    async def extract(self, input :dict) -> dict:
        return await self.run_one(input)
        
    async def extract_batch_parallel(self, inputs: list[dict]) -> list[dict]:
        return await asyncio.gather(*[self.run_one(i) for i in inputs])
    
    async def run_one_img(self, input: dict) -> dict:
        """
        - input: dict = {
            "image": list[str],  # base64-encoded image strings with data:image/... prefix
            "filename": str
        }
        - output: dict = {
            "filename": str,
            "result": str
        }
        """
        prompt = prompts["extract_full_bl_batch_with_ocr"]
        rendered_msgs = prompt.format_messages()

        # Build image message with a base64 image list
        img_message = HumanMessage(content=[
            {"type": "text", "text": "Please extract structured data from the following images."},
            *[
                {"type": "image_url", "image_url": {"url": b64}}
                for b64 in input["image"]
            ]
        ])

        full_message = rendered_msgs + [img_message]

        start = time.perf_counter()
        res = await self.img_llm.ainvoke(full_message)
        duration = time.perf_counter() - start

        logger.info(f"[GPT][Image] {input['filename']} took {duration:.2f}s")

        # Log the result content for debugging
        logger.info(f"[GPT][Image] {input['filename']} res: {res}")

        return {"filename": input["filename"], "result": res.content}
    
    async def extract_img(self, input: dict) -> dict:
        return await self.run_one_img(input)
    
    async def extract_img_batch_parallel(self, inputs: list[dict]) -> list[dict]:
        return await asyncio.gather(*[self.run_one_img(i) for i in inputs])
    