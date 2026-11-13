
import re
from collections import Counter

STOP_WORDS = {
    "the", "is", "are", "was", "were", "a", "an",
    "and", "or", "but", "to", "of", "in", "on",
    "for", "with", "as", "by", "from", "that",
    "this", "it", "be", "has", "have", "had"
}


def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def split_sentences(text):
    text = clean_text(text)

    return [
        sentence.strip()
        for sentence in re.split(r"(?<=[.!?])\s+", text)
        if sentence.strip()
    ]


def extract_keywords(text, limit=10):
    words = re.findall(
        r"\b[a-zA-Z][a-zA-Z'-]{2,}\b",
        text.lower()
    )

    words = [
        word for word in words
        if word not in STOP_WORDS
    ]

    frequency = Counter(words)

    return [
        word for word, count
        in frequency.most_common(limit)
    ]
