
import os
import uuid
import json
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "data" / "uploaded"
METADATA_FILE = BASE_DIR / "data" / "documents.json"

ALLOWED_EXTENSIONS = {".pdf", ".jpg", ".jpeg", ".png"}

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def load_metadata():
    if not METADATA_FILE.exists():
        return []

    with open(METADATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_metadata(documents):
    METADATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(METADATA_FILE, "w", encoding="utf-8") as f:
        json.dump(documents, f, indent=4)


@router.post("/upload")
async def upload_documents(files: List[UploadFile] = File(...)):
    uploaded_documents = []

    for file in files:
        extension = Path(file.filename).suffix.lower()

        if extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file format: {file.filename}"
            )

        document_id = str(uuid.uuid4())
        safe_filename = f"{document_id}{extension}"
        file_path = UPLOAD_DIR / safe_filename

        try:
            content = await file.read()

            if not content:
                raise HTTPException(
                    status_code=400,
                    detail=f"Empty file: {file.filename}"
                )

            with open(file_path, "wb") as f:
                f.write(content)

            document_info = {
                "id": document_id,
                "filename": file.filename,
                "stored_filename": safe_filename,
                "file_type": extension,
                "file_size": len(content),
                "status": "uploaded"
            }

            uploaded_documents.append(document_info)

        finally:
            await file.close()

    existing_documents = load_metadata()
    existing_documents.extend(uploaded_documents)
    save_metadata(existing_documents)

    return {
        "message": "Documents uploaded successfully",
        "total_uploaded": len(uploaded_documents),
        "documents": uploaded_documents
    }
