from fastapi import APIRouter
from app.prompts import prompts

router = APIRouter()

def list_prompt_names() -> list:
    return [name for name in prompts.keys()]


@router.get("/prompts")
def get_prompt_list() -> dict:
    return {
        "prompts": [
            list_prompt_names()
        ]
    }