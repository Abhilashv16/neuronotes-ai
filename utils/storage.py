
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = DATA_DIR / "uploaded"
PROCESSED_DIR = DATA_DIR / "processed"

METADATA_FILE = DATA_DIR / "documents.json"

for directory in (UPLOAD_DIR, PROCESSED_DIR):
    directory.mkdir(parents=True, exist_ok=True)


def load_json(file_path, default=None):
    if not file_path.exists():
        return default

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_json(file_path, data):
    file_path.parent.mkdir(parents=True, exist_ok=True)

    temporary_file = file_path.with_suffix(
        file_path.suffix + ".tmp"
    )

    with open(temporary_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    temporary_file.replace(file_path)


def load_documents():
    documents = load_json(METADATA_FILE, [])

    if not isinstance(documents, list):
        raise ValueError("Invalid document metadata")

    return documents


def save_documents(documents):
    save_json(METADATA_FILE, documents)


def get_document(document_id):
    documents = load_documents()

    for document in documents:
        if document.get("id") == document_id:
            return document

    return None


def update_document(document_id, updates):
    documents = load_documents()

    for document in documents:
        if document.get("id") == document_id:
            document.update(updates)
            save_documents(documents)
            return document

    return None


def get_processed_file(document_id):
    return PROCESSED_DIR / f"{document_id}.json"
