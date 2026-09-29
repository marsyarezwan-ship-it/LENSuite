from pathlib import Path
import re
import pandas as pd


# ---------------------------------------------------------
# CEFR-J Vocabulary Profile
# ---------------------------------------------------------

DATA_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "cefrj-vocabulary-profile-1.5.csv"
)

CEFR_ORDER = {
    "A1": 1,
    "A2": 2,
    "B1": 3,
    "B2": 4,
    "C1": 5,
    "C2": 6,
}


def load_cefrj_vocabulary():
    """
    Load the CEFR-J Vocabulary Profile.

    The source dataset contains:
    - headword
    - pos
    - CEFR
    - CoreInventory 1
    - CoreInventory 2
    - Threshold
    """

    df = pd.read_csv(DATA_PATH)

    df["headword"] = (
        df["headword"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    df["CEFR"] = (
        df["CEFR"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    return df


def lookup_word(word):
    """
    Return all CEFR-J entries for a headword.

    A word may have more than one entry because its
    CEFR level can differ according to part of speech.
    """

    df = load_cefrj_vocabulary()

    word = str(word).strip().lower()

    matches = df[df["headword"] == word]

    if matches.empty:
        return []

    results = []

    for _, row in matches.iterrows():
        results.append(
            {
                "word": row["headword"],
                "pos": row["pos"],
                "cefr": row["CEFR"],
            }
        )

    return results


def compare_with_target(word_level, target_level):
    """
    Compare a CEFR-J lexical level with the teacher-selected
    target CEFR level.

    This comparison is descriptive evidence only.
    It does not determine whether a word is pedagogically
    appropriate or inappropriate.
    """

    word_level = str(word_level).upper()
    target_level = str(target_level).upper()

    if word_level not in CEFR_ORDER or target_level not in CEFR_ORDER:
        return "not_assessed"

    if CEFR_ORDER[word_level] <= CEFR_ORDER[target_level]:
        return "at_or_below_target"

    return "above_target"


# ---------------------------------------------------------
# Conservative headword matching
# ---------------------------------------------------------

def generate_headword_candidates(word):
    """
    Generate conservative possible headword forms for an
    inflected English word.

    The original word is always checked first.
    """

    word = str(word).strip().lower()

    candidates = [word]

    # Plural / third-person -ies
    # studies -> study
    if word.endswith("ies") and len(word) > 4:
        candidates.append(word[:-3] + "y")

    # -ing forms
    # playing -> play
    if word.endswith("ing") and len(word) > 5:
        stem = word[:-3]

        # playing -> play
        candidates.append(stem)

        # making -> make
        candidates.append(stem + "e")

        # running -> run
        if len(stem) >= 2 and stem[-1] == stem[-2]:
            candidates.append(stem[:-1])

    # -ed forms
    if word.endswith("ed") and len(word) > 4:
        stem = word[:-2]

        # worked -> work
        candidates.append(stem)

        # liked -> like
        candidates.append(stem + "e")

        # stopped -> stop
        if len(stem) >= 2 and stem[-1] == stem[-2]:
            candidates.append(stem[:-1])

    # Plural / third-person -es
    if word.endswith("es") and len(word) > 3:
        candidates.append(word[:-2])
        candidates.append(word[:-1])

    # Simple plural / third-person -s
    # friends -> friend
    # likes -> like
    # students -> student
    if (
        word.endswith("s")
        and len(word) > 3
        and not word.endswith("ss")
    ):
        candidates.append(word[:-1])

    # Remove duplicates while preserving order
    return list(dict.fromkeys(candidates))


def lookup_word_with_headword(word):
    """
    Look up a surface form and conservative possible
    headword forms.

    Preference is given to a useful base-form match when
    an inflected surface form may otherwise produce a
    misleading exact-match entry.

    This is conservative morphological matching, not
    full contextual POS tagging.
    """

    word = str(word).strip().lower()
    candidates = generate_headword_candidates(word)

    matches = []

    for candidate in candidates:
        entries = lookup_word(candidate)

        if entries:
            matches.append(
                {
                    "surface_word": word,
                    "matched_headword": candidate,
                    "entries": entries,
                }
            )

    if not matches:
        return None

    # -------------------------------------------------
    # Prefer useful base forms for common inflections
    # -------------------------------------------------

    # -ing forms: playing -> play
    if word.endswith("ing"):
        for match in matches:
            if match["matched_headword"] != word:
                verb_entries = [
                    entry
                    for entry in match["entries"]
                    if entry["pos"] == "verb"
                ]

                if verb_entries:
                    match["entries"] = verb_entries
                    return match

    # -ies forms: studies -> study
    if word.endswith("ies"):
        expected = word[:-3] + "y"

        for match in matches:
            if match["matched_headword"] == expected:
                return match

    # -ed forms: worked -> work
    if word.endswith("ed"):
        for match in matches:
            if match["matched_headword"] != word:
                verb_entries = [
                    entry
                    for entry in match["entries"]
                    if entry["pos"] == "verb"
                ]

                if verb_entries:
                    match["entries"] = verb_entries
                    return match

    # -------------------------------------------------
    # Plural / third-person -s and -es
    # -------------------------------------------------
    #
    # If the exact surface form only has a specialised
    # entry but a plausible base headword also exists,
    # prefer the base headword evidence.
    #
    # Example:
    # sports -> sport
    #
    if word.endswith("s") and not word.endswith("ss"):

        base_matches = [
            match
            for match in matches
            if match["matched_headword"] != word
        ]

        if base_matches:
            return base_matches[0]

    # Otherwise retain the exact CEFR-J match.
    return matches[0]

# ---------------------------------------------------------
# Full-text CEFR-J lexical analysis
# ---------------------------------------------------------

def analyse_text_cefr(text, target_level):
    """
    Analyse the vocabulary in a complete text against
    the CEFR-J Vocabulary Profile.

    Results are descriptive. Words above the selected
    target are not automatically considered inappropriate.
    """

    # Extract alphabetic word forms
    words = re.findall(
        r"[A-Za-z]+(?:'[A-Za-z]+)?",
        str(text).lower()
    )

    # Analyse each unique surface word once
    unique_words = sorted(set(words))

    results = {
        "target_level": str(target_level).upper(),
        "at_or_below_target": [],
        "above_target": [],
        "not_classified": [],
    }

    for word in unique_words:

        # Try the surface form first, then conservative
        # possible headword forms.
        lookup_result = lookup_word_with_headword(word)

        if not lookup_result:
            results["not_classified"].append(word)
            continue

        entries = lookup_result["entries"]
        matched_headword = lookup_result["matched_headword"]

        levels = [
            entry["cefr"]
            for entry in entries
            if entry["cefr"] in CEFR_ORDER
        ]

        if not levels:
            results["not_classified"].append(word)
            continue

        # If a word has several POS entries, retain all
        # available CEFR-J evidence rather than pretending
        # we know its POS from spelling alone.
        comparisons = [
            compare_with_target(level, target_level)
            for level in levels
        ]

        item = {
            "word": word,
            "headword": matched_headword,
            "entries": entries,
        }

        # Only classify as above-target when ALL available
        # CEFR-J entries are above the selected target.
        if all(
            comparison == "above_target"
            for comparison in comparisons
        ):
            results["above_target"].append(item)
        else:
            results["at_or_below_target"].append(item)

    classified_count = (
        len(results["at_or_below_target"])
        + len(results["above_target"])
    )

    total_count = len(unique_words)

    results["summary"] = {
        "unique_words": total_count,
        "classified_words": classified_count,
        "at_or_below_target": len(
            results["at_or_below_target"]
        ),
        "above_target": len(
            results["above_target"]
        ),
        "not_classified": len(
            results["not_classified"]
        ),
    }

    return results

def build_teacher_lexical_summary(analysis):
    """
    Convert CEFR-J lexical analysis into a teacher-friendly
    summary.

    The summary provides reference evidence without treating
    above-target or unclassified vocabulary as automatically
    inappropriate.
    """

    target_level = analysis.get("target_level", "")
    summary = analysis.get("summary", {})

    classified = summary.get("classified_words", 0)
    at_or_below = summary.get("at_or_below_target", 0)
    above = summary.get("above_target", 0)
    unclassified = summary.get("not_classified", 0)

    # Calculate percentage using classified items only.
    if classified > 0:
        within_percentage = round(
            (at_or_below / classified) * 100
        )
    else:
        within_percentage = 0

    # -----------------------------------------------------
    # Above-target lexical items
    # -----------------------------------------------------

    learning_opportunities = []

    for item in analysis.get("above_target", []):
        levels = sorted(
            {
                entry["cefr"]
                for entry in item.get("entries", [])
                if entry.get("cefr") in CEFR_ORDER
            },
            key=lambda level: CEFR_ORDER[level],
        )

        learning_opportunities.append(
            {
                "word": item.get("word", ""),
                "headword": item.get("headword", ""),
                "reference_levels": levels,
            }
        )

    # -----------------------------------------------------
    # Unclassified items
    # -----------------------------------------------------

    unclassified_words = analysis.get(
        "not_classified",
        []
    )

    # -----------------------------------------------------
    # Teacher-facing interpretation
    # -----------------------------------------------------

    if classified == 0:
        interpretation = (
            "There is not enough classified CEFR-J lexical "
            "evidence to describe the vocabulary profile of "
            "this material."
        )

    else:
        interpretation = (
            f"{at_or_below} of {classified} CEFR-J-classified "
            f"lexical types in this material are referenced at "
            f"or below the selected {target_level} level "
            f"({within_percentage}%). "
            f"Above-target items are not automatically "
            f"inappropriate. They should be considered in "
            f"relation to learner needs, topic relevance, "
            f"context, instructional purpose and available "
            f"support."
        )
    
    return {
        "target_level": target_level,
        "classified_words": classified,
        "at_or_below_target": at_or_below,
        "above_target": above,
        "not_classified": unclassified,
        "within_target_percentage": within_percentage,
        "learning_opportunities": learning_opportunities,
        "unclassified_words": unclassified_words,
        "interpretation": interpretation,
        "reference_note": (
            "CEFR-J levels are used as lexical reference "
            "evidence. They should not be interpreted as an "
            "official CEFR judgement of whether an individual "
            "word is appropriate or inappropriate for a "
            "particular learner."
        ),
    }