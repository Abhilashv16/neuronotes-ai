
def generate_notes(nlp_result, filename):
    keywords = nlp_result.get("keywords", [])
    key_points = nlp_result.get("key_points", [])
    word_count = nlp_result.get("word_count", 0)

    summary = " ".join(key_points[:3])

    if not summary:
        summary = "No sufficient text was extracted."

    return {
        "title": filename,
        "summary": summary,
        "key_points": key_points,
        "keywords": keywords,
        "word_count": word_count,
        "sections": [
            {
                "heading": "Summary",
                "content": summary
            },
            {
                "heading": "Key Points",
                "content": key_points
            },
            {
                "heading": "Important Keywords",
                "content": keywords
            }
        ]
    }
