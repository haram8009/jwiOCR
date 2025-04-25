import json
from .base_output_handler import BaseOutputHandler
from app.utils.logger import log_all_methods

@log_all_methods
class JSONHandler(BaseOutputHandler):
    def save(self, result: dict, output_path: str):
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

    def parse(self, raw_result: str) -> dict:
        print(f"Raw result: {raw_result}", type(raw_result) )
        try:
            return json.loads(raw_result) if isinstance(raw_result, str) else raw_result
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to decode GPT response: {e}")
