from typing import List
from fastapi import APIRouter, UploadFile, File, HTTPException

router = APIRouter()

@router.post("/upload")
async def upload_documents(
    files: List[UploadFile] = File(
        ...,
        description="Select one or more PDF or image files"
    )
):
    return {
        "total_files": len(files),
        "files": [file.filename for file in files]
    }