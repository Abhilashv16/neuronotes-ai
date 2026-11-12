
import re
from collections import Counter


STOP_WORDS = {
    "the", "is", "are", "was", "were", "a", "an",
    "and", "or", "but", "in", "on", "at", "to",
    "of", "for", "with", "by", "from", "as", "it",
    "this", "that", "these", "those", "be", "been",
    "being", "has", "have", "had", "do", "does",
    "did", "will", "would", "could", "should",
    "can", "may", "might", "must", "not", "we",
    "they", "he", "she", "you", "i", "their",
    "our", "your", "its", "them", "his", "her"
}


def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_sentences(text):
    sentences = re.split(
        r"(?<=[.!?])\s+",
        clean_text(text)
    )

    return [
        sentence.strip()
        for sentence in sentences
        if len(sentence.strip()) > 20
    ]


def extract_keywords(text, limit=15):
    words = re.findall(
        r"\b[a-zA-Z][a-zA-Z0-9'-]*\b",
        text.lower()
    )

    filtered_words = [
        word for word in words
        if word not in STOP_WORDS and len(word) > 2
    ]

    frequency = Counter(filtered_words)

    return [
        word for word, count in frequency.most_common(limit)
    ]


def extract_key_points(text, limit=10):
    sentences = extract_sentences(text)

    if not sentences:
        return []

    keywords = extract_keywords(text, limit=30)

    keyword_set = set(keywords)

    scored_sentences = []

    for index, sentence in enumerate(sentences):
        words = re.findall(
            r"\b[a-zA-Z][a-zA-Z0-9'-]*\b",
            sentence.lower()
        )

        score = sum(
            1 for word in words
            if word in keyword_set
        )

        scored_sentences.append(
            (score, index, sentence)
        )

    selected = sorted(
        scored_sentences,
        key=lambda item: (-item[0], item[1])
    )[:limit]

    selected.sort(key=lambda item: item[1])

    return [
        sentence for score, index, sentence in selected
    ]


def process_text(text):
    cleaned_text = clean_text(text)

    return {
        "cleaned_text": cleaned_text,
        "sentences": extract_sentences(cleaned_text),
        "keywords": extract_keywords(cleaned_text),
        "key_points": extract_key_points(cleaned_text),
        "word_count": len(cleaned_text.split())
    }
