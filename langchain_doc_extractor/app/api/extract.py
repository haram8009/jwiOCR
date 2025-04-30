from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from app.services.extract_service import ExtractService 
from app.schemas.file_data import FileData

router = APIRouter()
service = ExtractService()

@router.post("/extract")
async def extract(
    file: UploadFile = File(...),
    prompt_name: str = Form(...)
):
    try:
        file.filename = file.filename.replace(" ", "_")
        contents = await file.read()
        filedata = {
            "filename": file.filename,
            "content_type": file.content_type,
            "contents": contents
        }
        filedata = FileData(**filedata)  # Validate the file data 

        result = await service.extract_document(filedata, prompt_name)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": "Extraction failed.", "detail": str(e)}
        )


@router.post("/extract/bulk")
async def extract_bulk(
    files: list[UploadFile] = File(...),
    prompt_name: str = Form(...)
):
    try:
        filedata_list = []
        for file in files:
            contents = await file.read()
            filedata = FileData(
                filename=file.filename.replace(" ", "_"),
                content_type=file.content_type,
                contents=contents
            )
            filedata_list.append(filedata)

        if not filedata_list:
            return JSONResponse(
                status_code=400,
                content={"message": "No files provided."}
            )

        results = await service.extract_document_bulk(filedata_list, prompt_name)
        return results

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": "Bulk extraction failed.", "detail": str(e)}
        )
