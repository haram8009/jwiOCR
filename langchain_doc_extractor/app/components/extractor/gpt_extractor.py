from langchain_openai import ChatOpenAI
from langchain.schema.runnable import RunnableParallel, RunnablePassthrough
from app.prompts import prompts
from app.components.extractor.base_extractor import BaseExtractor
from app.utils.logger import log_all_methods
import logging
logger = logging.getLogger(__name__)

@log_all_methods
class GPTExtractor(BaseExtractor):
    def __init__(self, api_key: str, prompt_name: str = "extract_basic"):
        self.llm = ChatOpenAI(
            temperature=0,
            model="gpt-4.1-mini",
            openai_api_key=api_key
        )
        self.chain = prompts[prompt_name] | self.llm
        # for parallel processing, use Runnable Parallel
        # self.chain = RunnableParallel({
        #     "basic": prompts["extract_basic"] | self.llm,
        #     "detailed": prompts["extract_full_bl"] | self.llm,
        #     "original_text": RunnablePassthrough()
        # })

    def extract(self, text: str, context: dict = {}) -> dict:
        result = self.chain.invoke({"text": text})
        logger.info(f"GPT Extractor Result: {result}")
        # return self._parse_result(result.content)
        return result.content


    async def extract_batch(self, inputs: list[dict]) -> list[str]:
        """
        inputs: List of {"text": ..., "filename": ...}
        returns: List of LLM response and filename dictionary {"text": ..., "filename": ...}
        """
        results = await self.chain.abatch(inputs)
        # NOTE: abatch() returns a list of results in the same order as inputs
        return [ {"filename": inp["filename"], "result": res.content} for inp, res in zip(inputs, results)]
