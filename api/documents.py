
import json
from pathlib import Path

from fastapi import APIRouter, HTTPException

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent
METADATA_FILE = BASE_DIR / "data" / "documents.json"


@router.get("/documents")
def get_documents():

    if not METADATA_FILE.exists():
        return {
            "total_documents": 0,
            "documents": []
        }

    try:
        with open(METADATA_FILE, "r", encoding="utf-8") as file:
            documents = json.load(file)

        return {
            "total_documents": len(documents),
            "documents": documents
        }

    except (json.JSONDecodeError, OSError):
        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve document metadata"
        )

@router.get("/documents/{document_id}")
def get_document(document_id: str):

    if not METADATA_FILE.exists():
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    try:
        with open(METADATA_FILE, "r", encoding="utf-8") as file:
            documents = json.load(file)

        for document in documents:
            if document["id"] == document_id:
                return {
                    "document": document
                }

        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    except (json.JSONDecodeError, OSError):
        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve document metadata"
        )