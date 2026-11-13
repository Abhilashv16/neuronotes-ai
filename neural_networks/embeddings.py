
from functools import lru_cache


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


class EmbeddingUnavailableError(RuntimeError):
    pass


@lru_cache(maxsize=1)
def load_model():

    try:
        from sentence_transformers import SentenceTransformer

        return SentenceTransformer(MODEL_NAME)

    except Exception as error:
        raise EmbeddingUnavailableError(
            f"Unable to load embedding model: {error}"
        ) from error


def generate_embedding(text):

    if not text.strip():
        return []

    try:
        model = load_model()

        embedding = model.encode(
            text,
            normalize_embeddings=True
        )

        return embedding.tolist()

    except EmbeddingUnavailableError:
        raise

    except Exception as error:
        raise EmbeddingUnavailableError(
            f"Embedding generation failed: {error}"
        ) from error
