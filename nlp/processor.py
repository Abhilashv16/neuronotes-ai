
import re
from collections import Counter


STOP_WORDS = {
    "the", "is", "are", "was", "were",
    "a", "an", "and", "or", "but",
    "to", "of", "in", "on", "for",
    "with", "as", "by", "from",
    "that", "this", "it", "be",
    "has", "have", "had", "will",
    "we", "they", "their", "you"
}


def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def split_sentences(text):
    return [
        sentence.strip()
        for sentence in re.split(
            r"(?<=[.!?])\s+",
            clean_text(text)
        )
        if len(sentence.strip()) > 20
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

    frequencies = Counter(words)

    return [
        word for word, count
        in frequencies.most_common(limit)
    ]


def generate_summary(sentences, max_sentences=7):

    if not sentences:
        return []

    words = re.findall(
        r"\b[a-zA-Z][a-zA-Z'-]{2,}\b",
        " ".join(sentences).lower()
    )

    frequencies = Counter(
        word for word in words
        if word not in STOP_WORDS
    )

    if not frequencies:
        return sentences[:max_sentences]

    max_frequency = max(frequencies.values())

    scored_sentences = []

    for index, sentence in enumerate(sentences):

        sentence_words = re.findall(
            r"\b[a-zA-Z][a-zA-Z'-]{2,}\b",
            sentence.lower()
        )

        score = sum(
            frequencies[word] / max_frequency
            for word in sentence_words
            if word in frequencies
        )

        score /= max(len(sentence_words), 1)

        scored_sentences.append(
            (score, index, sentence)
        )

    selected = sorted(
        scored_sentences,
        reverse=True
    )[:max_sentences]

    selected.sort(key=lambda item: item[1])

    return [
        sentence for score, index, sentence in selected
    ]


def process_text(text):

    cleaned = clean_text(text)

    sentences = split_sentences(cleaned)

    keywords = extract_keywords(cleaned)

    summary = generate_summary(sentences)

    return {
        "cleaned_text": cleaned,
        "sentences": sentences,
        "keywords": keywords,
        "summary": summary,
        "key_points": summary[:5],
        "word_count": len(cleaned.split())
    }
