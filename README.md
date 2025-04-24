# langOCR

## Document Extractor
A modular OCR + GPT document extractor system using FastAPI and LangChain.

## 📁 전체 파일 구조 (File Structure)

```bash
doc_extractor/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env
├── sample.pdf
├── output/             # 추출 결과 저장 폴더
├── prompts/
│   ├── extract_basic.json
│   ├── extract_logistics.json
└── app/
    ├── main.py         # 테스트용 실행 코드 
    ├── server.py       # fastAPI 실행 코드
    ├── pipeline.py
    ├── preprocessor.py
    ├── extractor.py
    ├── output_handler.py
    ├── prompt_loader.py
    └── interfaces/
        ├── preprocessor.py
        ├── extractor.py
        └── output_handler.py
```
## 🧩 주요 기능 (Features)

- 📄 PDF 또는 이미지 문서의 텍스트 자동 추출 (OCR)
- 💬 템플릿 기반 GPT 문서 정보 추출
- 📤 JSON 포맷 결과 반환 및 저장
- 🛠️ FastAPI REST API + Swagger 문서
- 🐳 Docker 환경 

## ⚙️ 실행 흐름 (Processing Pipeline)

1. PDF 또는 이미지 업로드
2. 텍스트 추출 (`PDFPreprocessor`)
3. 템플릿 로드 (`prompt_loader`)
4. GPT 추론 (`GPTExtractor`)
5. 결과 저장 (`JSONSaver`)
6. FastAPI를 통해 API 호출 가능 (`/extract`, `/prompts`)

## 🚀 실행 방법
### 1️⃣ Docker로 실행
```bash
docker-compose down && docker-compose up --build
FastAPI Swagger 문서: http://localhost:8000/docs
```

### 2️⃣ 로컬 개발환경 실행 (venv 권장)
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate
pip install -r requirements.txt

# 테스트용 실행
PYTHONPATH=. python app/main.py
```

### 3️⃣ 실행 결과 확인
테스트용 실행 후 추출된 JSON 결과: `output/result.json`

