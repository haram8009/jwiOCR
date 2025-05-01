# 📄 jwiOCR — Intelligent Document Extraction with OCR + GPT

**jwiOCR** is a modular, production-ready document extraction system that combines OCR and GPT via [LangChain](https://www.langchain.com/) and [FastAPI](https://fastapi.tiangolo.com/).  
It is optimized for extracting structured data (e.g., shipping or invoice fields) from PDFs and images without fixed templates.

---

## ✨ Features

- 🧠 **GPT-powered data extraction** using prompt templates
- 🖼️ **OCR fallback** via Tesseract for scanned PDFs or image-based documents
- 📄 Supports PDF and common image formats (JPEG, PNG)
- ⚡ FastAPI REST API with OpenAPI docs (`/docs`)
- 🧱 Modular architecture: easily extendable preprocessors, extractors, and output handlers
- 🚀 Docker-ready for deployment and scaling
- 📤 Outputs structured JSON per document

---

## 📂 Project Structure

```bash
jwiOCR/
├── docker-compose.yml
├── Dockerfile
├── Jenkinsfile
├── requirements.txt
├── .env                          # Environment variables
├── .env.example
├── .gitignore
├── .dockerignore
├── README.md
├── sample.pdf
├── output/                       # JSON extraction results
├── prompts/                      # Prompt templates (Python-based)
│   ├── __init__.py
│   ├── extract_basic.py
│   ├── extract_full_bl.py
│   └── extract_full_bl_batch.py
├── app/
│   ├── server.py                 # FastAPI entry point
│   ├── components/
│   │   ├── extractor/
│   │   │   ├── __init__.py
│   │   │   ├── base_extractor.py
│   │   │   └── gpt_extractor.py
│   │   ├── output_handler/
│   │   │   ├── __init__.py
│   │   │   ├── base_output_handler.py
│   │   │   └── json_handler.py
│   │   ├── preprocessor/
│   │   │   ├── __init__.py
│   │   │   ├── base_preprocessor.py
│   │   │   └── pdf_preprocessor.py
│   │   └── pipelines.py         # (if needed)
│   ├── services/
│   │   └── extract_service.py
│   ├── schemas/
│   │   └── file_data.py
│   ├── utils/
│   │   └── logger.py
```

## 🔄 Processing Flow
1. Upload a PDF or image document
2. Text extraction via PyMuPDF (with OCR fallback using Tesseract)
3. Prompt selection and injection
4. Inference with GPT via LangChain (GPTExtractor)
5. Parse and save results as structured JSON (JSONHandler)
6. Access via REST API (/extract, /extract/bulk, /prompts)

## 🚀 Getting Started
### 🐳 Run with Docker (recommended)
```bash
docker-compose down && docker-compose up --build
Access the FastAPI docs at: http://localhost:8000/docs
```
### 🧪 Run locally with Python (for development)
```bash
python -m venv venv
source venv/bin/activate         # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Start FastAPI development server
PYTHONPATH=. uvicorn app.server:app --reload
```

## 📬 API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | /extract | Extract data from a single file |
| POST | /extract/bulk | Batch extract multiple files |
| GET | /prompts | List available prompt templates |

All endpoints return structured JSON responses.

---

## 📝 Output Format
Example:

```json
{
  "filename": "invoice123.pdf",
  "result": {
    "invoice_number": "INV-2023-001",
    "exporter": "ACME Corp",
    "amount": "13,400.00"
  }
}
```

## 📌 Future Plans
- Image preprocessing support (IMGPreprocessor)
- Database integration for result storage
- Retry/validation pipeline for low-confidence results