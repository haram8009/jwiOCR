from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.extractor import GPTExtractor
from app.preprocessor import PDFPreprocessor
from app.prompt_loader import load_prompt

import os
import fitz
import pytesseract
from PIL import Image
import io

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def extract_text_from_pdf(file_bytes: bytes) -> str:
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    full_text = ""
    for page in doc:
        text = page.get_text()
        if text.strip():
            full_text += text
        else:
            pix = page.get_pixmap(dpi=300)
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            full_text += pytesseract.image_to_string(img)
    return full_text

@app.get("/prompts")
def get_prompt_list():
    from pathlib import Path
    prompts = [f.stem for f in Path("prompts").glob("*.json")]
    return {"prompts": prompts}

@app.post("/extract")
async def extract(
    file: UploadFile = File(...),
    prompt_name: str = Form(...)
):
    contents = await file.read()
    text = extract_text_from_pdf(contents)

    extractor = GPTExtractor(
        api_key=os.getenv("OPENAI_API_KEY"),
        prompt_name=prompt_name
    )

    result = extractor.extract(text)

    return JSONResponse(content=result)
