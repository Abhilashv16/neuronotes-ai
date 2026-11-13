
from pathlib import Path


def generate_notes(nlp_result, filename):

    summary = nlp_result.get("summary", [])
    keywords = nlp_result.get("keywords", [])
    key_points = nlp_result.get("key_points", [])

    return {
        "title": Path(filename).stem,
        "summary": summary,
        "key_points": key_points,
        "keywords": keywords,
        "word_count": nlp_result.get(
            "word_count", 0
        ),
        "generation_method": "Extractive NLP"
    }
