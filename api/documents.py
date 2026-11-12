from pathlib import Path
from fastapi import APIRouter, HTTPException

from utils.storage import (
    UPLOAD_DIR,
    load_documents,
    save_documents,
    get_processed_file
)

router = APIRouter()


@router.get("/documents")
def get_documents():
    try:
        documents = load_documents()

        return {
            "total_documents": len(documents),
            "documents": documents
        }

    except (OSError, ValueError):
        raise HTTPException(
            500,
            "Unable to retrieve documents"
        )


@router.get("/documents/{document_id}")
def get_document(document_id: str):
    try:
        documents = load_documents()

        for document in documents:
            if document.get("id") == document_id:
                return {"document": document}

        raise HTTPException(
            404,
            "Document not found"
        )

    except HTTPException:
        raise

    except (OSError, ValueError):
        raise HTTPException(
            500,
            "Unable to retrieve document"
        )


@router.delete("/documents/{document_id}")
def delete_document(document_id: str):
    try:
        documents = load_documents()

        document = next(
            (
                item for item in documents
                if item.get("id") == document_id
            ),
            None
        )

        if document is None:
            raise HTTPException(
                404,
                "Document not found"
            )

        stored_filename = document.get("stored_filename")

        if (not stored_filename or Path(stored_filename).name != stored_filename
):
            raise HTTPException(500,"Invalid stored filename"
    )

        file_path = UPLOAD_DIR / stored_filename

        # Save updated metadata
        remaining_documents = [
            item for item in documents
            if item.get("id") != document_id
        ]

        save_documents(remaining_documents)

        # Remove original file
        file_removed = False

        if file_path.is_file():
            file_path.unlink()
            file_removed = True

        # Remove processed output
        processed_file = get_processed_file(document_id)
        processed_file.unlink(missing_ok=True)

        return {
            "message": "Document deleted successfully",
            "document_id": document_id,
            "file_removed": file_removed
        }

    except HTTPException:
        raise

    except (OSError, ValueError):
        raise HTTPException(
            500,
            "Unable to delete document"
        )
