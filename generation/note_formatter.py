
def format_notes(notes, document_id):
    return {
        "document_id": document_id,
        "title": notes.get(
            "title",
            "Generated Study Notes"
        ),
        "summary": notes.get("summary", []),
        "key_points": notes.get("key_points", []),
        "keywords": notes.get("keywords", []),
        "word_count": notes.get("word_count", 0),
        "method": notes.get("method", "Extractive NLP")
    }
