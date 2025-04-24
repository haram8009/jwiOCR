from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from app.interfaces.extractor import BaseExtractor
from app.prompt_loader import load_prompt
import json
import re

class GPTExtractor(BaseExtractor):
    def __init__(self, api_key: str, prompt_name: str = "extract_basic"):
        self.llm = ChatOpenAI(
            temperature=0,
            model="gpt-3.5-turbo",
            openai_api_key=api_key
        )
        self.prompt_template = load_prompt(prompt_name)

    def extract(self, text: str, context: dict = {}) -> dict:
        prompt = ChatPromptTemplate.from_template(self.prompt_template)
        chain = prompt | self.llm
        result = chain.invoke({"text": text})
        print(f"GPT Extractor Result: {result.content}")
        return self._parse_result(result.content)

    def _parse_result(self, content: str):
        match = re.search(r'\{.*\}', content, re.DOTALL)
        try:
            return json.loads(match.group()) if match else {"error": "Invalid format"}
        except json.JSONDecodeError:
            return {"error": "Failed to parse JSON", "raw": content}
        except Exception as e:
            return {"error": str(e), "raw": content}
