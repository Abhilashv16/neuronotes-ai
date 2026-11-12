
_model = None


class EmbeddingUnavailableError(Exception):
    pass


def load_model():
    global _model

    if _model is not None:
        return _model

    try:
        from sentence_transformers import SentenceTransformer

        _model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

        return _model

    except Exception as error:
        raise EmbeddingUnavailableError(
            f"Unable to load embedding model: {error}"
        )


def generate_embedding(text):
    if not text or not text.strip():
        raise ValueError("Cannot generate embedding for empty text")

    model = load_model()

    vector = model.encode(
        text[:10000],
        normalize_embeddings=True
    )

    return {
        "model": "all-MiniLM-L6-v2",
        "dimensions": len(vector),
        "vector": vector.tolist()
    }
