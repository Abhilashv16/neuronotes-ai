
import uuid
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List

from utils.storage import (
    UPLOAD_DIR,
    load_documents,
    save_documents
)

router = APIRouter()

ALLOWED_EXTENSIONS = {".pdf", ".jpg", ".jpeg", ".png"}
MAX_FILE_SIZE = 25 * 1024 * 1024


@router.post("/upload")
async def upload_documents(
    files: List[UploadFile] = File(...)
):
    if not files:
        raise HTTPException(400, "No files provided")

    uploaded = []
    saved_paths = []

    try:
        documents = load_documents()

        for file in files:
            original_filename = Path(
                file.filename or ""
            ).name

            extension = Path(
                original_filename
            ).suffix.lower()

            if extension not in ALLOWED_EXTENSIONS:
                raise HTTPException(
                    400,
                    f"Unsupported file format: {original_filename}"
                )

            content = await file.read(MAX_FILE_SIZE + 1)

            if not content:
                raise HTTPException(
                    400,
                    f"Empty file: {original_filename}"
                )

            if len(content) > MAX_FILE_SIZE:
                raise HTTPException(
                    413,
                    f"File exceeds 25 MB: {original_filename}"
                )

            document_id = str(uuid.uuid4())
            stored_filename = f"{document_id}{extension}"
            file_path = UPLOAD_DIR / stored_filename

            with open(file_path, "wb") as output:
                output.write(content)

            saved_paths.append(file_path)

            document = {
                "id": document_id,
                "filename": original_filename,
                "stored_filename": stored_filename,
                "file_type": extension,
                "file_size": len(content),
                "status": "uploaded"
            }

            uploaded.append(document)

        documents.extend(uploaded)
        save_documents(documents)

        return {
            "message": "Documents uploaded successfully",
            "total_uploaded": len(uploaded),
            "documents": uploaded
        }

    except HTTPException:
        for path in saved_paths:
            path.unlink(missing_ok=True)
        raise

    except (OSError, ValueError):
        for path in saved_paths:
            path.unlink(missing_ok=True)

        raise HTTPException(
            500,
            "Unable to save uploaded documents"
        )

    finally:
        for file in files:
            await file.close()