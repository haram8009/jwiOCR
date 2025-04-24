import json
from app.interfaces.output_handler import BaseOutputHandler

class JSONSaver(BaseOutputHandler):
    def save(self, data: dict, path: str):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
