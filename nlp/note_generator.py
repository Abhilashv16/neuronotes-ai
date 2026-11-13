
from collections import Counter
import re

from nlp.text_processor import (
    split_sentences,
    extract_keywords
)


def summarize_text(text, max_sentences=7):
    sentences = split_sentences(text)

    if not sentences:
        return []

    words = re.findall(
        r"\b[a-zA-Z][a-zA-Z'-]{2,}\b",
        text.lower()
    )

    frequencies = Counter(words)

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


def generate_notes(text):
    summary = summarize_text(text)

    keywords = extract_keywords(text)

    return {
        "title": "Generated Study Notes",
        "summary": summary,
        "key_points": summary[:5],
        "keywords": keywords,
        "word_count": len(text.split()),
        "method": "Extractive NLP"
    }
