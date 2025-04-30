import os
import asyncio
import time
from langchain_openai import ChatOpenAI
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
