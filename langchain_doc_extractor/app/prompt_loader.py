import json
import os
from functools import lru_cache

@lru_cache
def load_prompt(prompt_name: str, base_dir: str = "prompts") -> str:
    path = os.path.join(base_dir, f"{prompt_name}.json")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Prompt file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)["template"]
