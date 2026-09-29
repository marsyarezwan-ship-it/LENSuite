import os
import re
import pandas as pd


# ============================================================
# SUBTLEX-US DATA
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

SUBTLEX_PATH = os.path.join(
    BASE_DIR,
    "data",
    "SUBTLEX-US.xlsx"
)


def load_subtlex():

    data = pd.read_excel(
        SUBTLEX_PATH,
        usecols=[
            "Word",
            "SUBTLWF",
            "Dom_PoS_SUBTLEX",
            "Zipf-value"
        ]
    )

    # Normalise words for matching
    data["Word"] = (
        data["Word"]
        .astype(str)
        .str.lower()
        .str.strip()
    )

    return data


def build_frequency_lookup(data):

    lookup = {}

    for _, row in data.iterrows():

        word = row["Word"]

        lookup[word] = {
            "zipf": row["Zipf-value"],
            "frequency_per_million":
                row["SUBTLWF"],
            "pos":
                row["Dom_PoS_SUBTLEX"]
        }

    return lookup


SUBTLEX_DATA = load_subtlex()

FREQUENCY_LOOKUP = build_frequency_lookup(
    SUBTLEX_DATA
)

def lookup_word(word):

    normalised_word = (
        word.lower().strip()
    )

    return FREQUENCY_LOOKUP.get(
        normalised_word
    )

# ============================================================
# LEXICAL FREQUENCY PROFILER
# ============================================================

FUNCTION_WORDS = {
    "a", "an", "the",
    "and", "or", "but",
    "of", "in", "on", "at", "to", "from",
    "for", "with", "by",
    "is", "am", "are", "was", "were",
    "be", "been", "being",
    "do", "does", "did",
    "have", "has", "had",
    "i", "you", "he", "she", "it",
    "we", "they",
    "me", "him", "her", "us", "them",
    "my", "your", "his", "our", "their",
    "this", "that", "these", "those"
}


def analyse_lexical_frequency(text):

    words = re.findall(
        r"\b[A-Za-z'-]+\b",
        text
    )

    normalised_words = [
        word.lower()
        for word in words
    ]

    # Analyse unique lexical types rather than
    # repeatedly flagging the same word.
    unique_words = sorted(
        set(normalised_words)
    )

    analysed_items = []
    unmatched_items = []

    for word in unique_words:

        # Function words are excluded from
        # teacher-facing lexical review.
        if word in FUNCTION_WORDS:
            continue

        corpus_data = lookup_word(word)

        if corpus_data is None:

            unmatched_items.append(word)
            continue

        analysed_items.append({
            "word": word,
            "zipf": corpus_data["zipf"],
            "frequency_per_million":
                corpus_data["frequency_per_million"],
            "pos": corpus_data["pos"]
        })

    return {
        "analysed_items": analysed_items,
        "unmatched_items": unmatched_items,
        "matched_count": len(analysed_items),
        "unmatched_count": len(unmatched_items)
    }
    normalised_word = (
        word.lower().strip()
    )

    return FREQUENCY_LOOKUP.get(
        normalised_word
    )