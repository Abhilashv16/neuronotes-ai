
from functools import lru_cache


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


@lru_cache(maxsize=1)
def load_model():
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(MODEL_NAME)


def generate_embedding(text):
    if not text.strip():
        return []

    model = load_model()

    embedding = model.encode(
        text,
        normalize_embeddings=True
    )

    return embedding.tolist()


def calculate_similarity(text1, text2):
    import numpy as np

    vector1 = generate_embedding(text1)
    vector2 = generate_embedding(text2)

    if not vector1 or not vector2:
        return 0.0

    return float(np.dot(vector1, vector2))
