
from fastapi import APIRouter, HTTPException

from utils.storage import (
    UPLOAD_DIR,
    get_document,
    update_document,
    save_json,
    get_processed_file
)

from document_processing.extractor import extract_document_text
from nlp.processor import process_text
from neural_networks.embeddings import (
    generate_embedding,
    EmbeddingUnavailableError
)
from generation.notes import generate_notes

router = APIRouter()


@router.post("/documents/{document_id}/process")
def process_document(document_id: str):

    try:
        document = get_document(document_id)

        if document is None:
            raise HTTPException(
                404,
                "Document not found"
            )

        file_path = UPLOAD_DIR / document["stored_filename"]

        if not file_path.is_file():
            raise HTTPException(
                404,
                "Uploaded document file not found"
            )

        # Step 1: PDF or image text extraction
        extracted_text = extract_document_text(file_path)

        if not extracted_text.strip():
            raise HTTPException(
                422,
                "No text could be extracted from the document"
            )

        # Step 2: NLP
        nlp_result = process_text(extracted_text)

        # Step 3: Neural network embeddings
        embedding_result = None
        embedding_status = "available"

        try:
            embedding_result = generate_embedding(
                extracted_text
            )

        except EmbeddingUnavailableError as error:
            embedding_status = "unavailable"

        # Step 4: Note generation
        notes = generate_notes(
            nlp_result,
            document["filename"]
        )

        # Step 5: Save processing results
        result = {
            "document_id": document_id,
            "filename": document["filename"],
            "processing_status": "completed",
            "extracted_text": extracted_text,
            "nlp": nlp_result,
            "embeddings": embedding_result,
            "embedding_status": embedding_status,
            "notes": notes
        }

        result_file = get_processed_file(document_id)
        save_json(result_file, result)

        update_document(
            document_id,
            {"status": "processed"}
        )

        return {
            "message": "Document processed successfully",
            "result": result
        }

    except HTTPException:
        raise

    except RuntimeError as error:
        raise HTTPException(
            503,
            str(error)
        )

    except (OSError, ValueError):
        raise HTTPException(
            500,
            "Document processing failed"
        )


@router.get("/documents/{document_id}/result")
def get_processing_result(document_id: str):

    if get_document(document_id) is None:
        raise HTTPException(
            404,
            "Document not found"
        )

    result_file = get_processed_file(document_id)

    if not result_file.exists():
        raise HTTPException(
            404,
            "Processing result not found"
        )

    try:
        import json

        with open(result_file, "r", encoding="utf-8") as file:
            result = json.load(file)

        return {"result": result}

    except (OSError, ValueError):
        raise HTTPException(
            500,
            "Unable to retrieve processing result"
        )
