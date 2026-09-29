import re

# Common irregular past-tense forms for prototype detection
IRREGULAR_PAST_FORMS = {
    "was", "were", "went", "had", "did", "said",
    "came", "saw", "took", "made", "got", "gave",
    "found", "thought", "told", "became", "left",
    "felt", "put", "brought", "began", "kept",
    "held", "wrote", "stood", "heard", "let",
    "meant", "set", "met", "ran", "paid", "sat",
    "spoke", "lay", "led", "read", "grew", "lost",
    "fell", "sent", "built", "understood", "drew",
    "broke", "spent", "cut", "rose", "drove",
    "bought", "wore", "chose", "ate", "drank"
}


def detect_simple_past(words):

    normalised = [
        word.lower()
        for word in words
    ]

    detected = []

    for word in normalised:

        # Irregular forms
        if word in IRREGULAR_PAST_FORMS:
            detected.append(word)

        # Regular -ed forms
        elif word.endswith("ed") and len(word) > 3:
            detected.append(word)

    return detected

# ============================================================
# DISCOURSE ANALYSIS
# ============================================================

SEQUENCING_MARKERS = [
    "first",
    "firstly",
    "then",
    "next",
    "after that",
    "later",
    "afterwards",
    "finally",
    "in the morning",
    "in the afternoon",
    "in the evening",
    "the next day",
    "last weekend",
    "last week",
    "last month",
    "last year",
    "last school holiday"
]


def detect_sequencing_markers(text):

    lower_text = text.lower()

    detected = []

    for marker in SEQUENCING_MARKERS:

        if marker in lower_text:
            detected.append(marker)

    return detected
# ============================================================
# RESOURCE COMPONENT ANALYSIS
# ============================================================

def detect_resource_components(text):

    lower_text = text.lower()

    answer_key_patterns = [
        "answer key",
        "answers:",
        "suggested answers",
        "sample answers",
        "model answers"
    ]

    teacher_note_patterns = [
        "teacher notes",
        "teacher's notes",
        "teachers' notes",
        "notes for teachers",
        "teacher guidance"
    ]

    answer_key_detected = any(
        pattern in lower_text
        for pattern in answer_key_patterns
    )

    teacher_notes_detected = any(
        pattern in lower_text
        for pattern in teacher_note_patterns
    )

    return {
        "answer_key": answer_key_detected,
        "teacher_notes": teacher_notes_detected
    }

def analyse_text(text):

    # Clean unnecessary whitespace
    clean_text = " ".join(text.split())

    # ========================================================
    # WORD ANALYSIS
    # ========================================================

    words = re.findall(
        r"\b[\w'-]+\b",
        clean_text
    )

    word_count = len(words)

    # Normalise words for lexical analysis
    normalised_words = [
        word.lower()
        for word in words
    ]
    past_forms = detect_simple_past(words)

    unique_past_forms = sorted(
        set(past_forms)
    )
    
    sequencing_markers = detect_sequencing_markers(
        clean_text
    )
    
    resource_components = detect_resource_components(
        clean_text
    )
    # Identify unique words
    unique_words = set(normalised_words)

    unique_word_count = len(unique_words)

    # Type-token ratio (TTR)
    if word_count > 0:

        lexical_diversity = (
            unique_word_count / word_count
        ) * 100

    else:

        lexical_diversity = 0

    # ========================================================
    # SENTENCE ANALYSIS
    # ========================================================

    sentences = re.split(
        r'(?<=[.!?])\s+',
        clean_text
    )

    # Remove empty results
    sentences = [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]

    sentence_count = len(sentences)

    # Calculate sentence lengths
    sentence_lengths = []

    for sentence in sentences:

        sentence_words = re.findall(
            r"\b[\w'-]+\b",
            sentence
        )

        sentence_lengths.append(
            len(sentence_words)
        )

    # ========================================================
    # SENTENCE STATISTICS
    # ========================================================

    if sentence_count > 0:

        average_sentence_length = (
            sum(sentence_lengths)
            / sentence_count
        )

        longest_sentence = max(
            sentence_lengths
        )

    else:

        average_sentence_length = 0
        longest_sentence = 0

    # ========================================================
    # RETURN RESULTS
    # ========================================================

    return {
                "answer_key_detected":
            resource_components["answer_key"],

        "teacher_notes_detected":
            resource_components["teacher_notes"],
            
        "sequencing_markers":
            sequencing_markers,

        "sequencing_marker_count":
            len(sequencing_markers),

        "past_form_count":
            len(past_forms),

        "past_forms":
            unique_past_forms,

        "character_count":
            len(clean_text),

        "word_count":
            word_count,

        "sentence_count":
            sentence_count,

        "average_sentence_length":
            round(
                average_sentence_length,
                1
            ),

        "longest_sentence":
            longest_sentence,

        "unique_word_count":
            unique_word_count,

        "lexical_diversity":
            round(
                lexical_diversity,
                1
            )
            
    }