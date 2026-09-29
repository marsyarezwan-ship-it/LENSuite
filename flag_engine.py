# ============================================================

# LENSUITE FLAG ENGINE

# ============================================================



SUPPORTED = "SUPPORTED"

REVIEW = "REVIEW"

MISMATCH = "MISMATCH"

NOT_ASSESSED = "NOT ASSESSED"





def create_flag(

    lens,

    status,

    feature,

    observation,

    evidence,

    interpretation,

    teacher_options=None

):



    return {

        "lens": lens,

        "status": status,

        "feature": feature,

        "observation": observation,

        "evidence": evidence,

        "interpretation": interpretation,

        "teacher_options": teacher_options or []

    }

def evaluate_grammar_target(

    target_grammar,

    past_form_count

):



    if not target_grammar:



        return create_flag(

            lens="Grammar & Syntax",

            status=NOT_ASSESSED,

            feature="Target grammar",

            observation="No target grammar was specified.",

            evidence="No teacher-selected grammar target.",

            interpretation=(

                "Grammar alignment cannot be evaluated "

                "without an intended target."

            )

        )



    if "past" in target_grammar.lower():



        if past_form_count > 0:



            return create_flag(

                lens="Grammar & Syntax",

                status=SUPPORTED,

                feature=target_grammar,

                observation=(

                    "Past-tense forms were detected "

                    "in the material."

                ),

                evidence=(

                    f"{past_form_count} past-tense "

                    "tokens detected by the current "

                    "prototype rules."

                ),

                interpretation=(

                    "Observable evidence supports the "

                    "presence of the teacher-selected "

                    "grammar target. This does not by "

                    "itself establish grammatical accuracy "

                    "or pedagogical adequacy."

                )

            )



        return create_flag(

            lens="Grammar & Syntax",

            status=REVIEW,

            feature=target_grammar,

            observation=(

                "No clear past-tense forms were detected."

            ),

            evidence=(

                "The current prototype detector returned "

                "zero matching past-tense tokens."

            ),

            interpretation=(

                "Teacher review is recommended. The absence "

                "of detected forms may indicate limited "

                "realisation of the requested target, but "

                "the prototype detector may also miss "

                "legitimate grammatical forms."

            )

        )



    return create_flag(

        lens="Grammar & Syntax",

        status=NOT_ASSESSED,

        feature=target_grammar,

        observation=(

            "Automatic detection for this grammar target "

            "has not yet been implemented."

        ),

        evidence="No validated detector is currently available.",

        interpretation=(

            "LENSuite does not make an alignment judgement "

            "for this target."

        )

    )

def evaluate_discourse(

    target_genre,

    sequencing_marker_count

):



    if not target_genre:



        return create_flag(

            lens="Discourse",

            status=NOT_ASSESSED,

            feature="Genre",

            observation="No target genre was specified.",

            evidence="No teacher-selected genre.",

            interpretation=(

                "Discourse alignment cannot be evaluated "

                "without an intended genre."

            )

        )



    if target_genre.lower() == "narrative":



        if sequencing_marker_count > 0:



            return create_flag(

                lens="Discourse",

                status=SUPPORTED,

                feature="Narrative organisation",

                observation=(

                    "Sequencing features associated with "

                    "narrative organisation were detected."

                ),

                evidence=(

                    f"{sequencing_marker_count} sequencing "

                    "markers detected."

                ),

                interpretation=(

                    "The material contains observable "

                    "features consistent with the requested "

                    "narrative organisation. These features "

                    "do not independently establish overall "

                    "genre quality."

                )

            )



        return create_flag(

            lens="Discourse",

            status=REVIEW,

            feature="Narrative organisation",

            observation=(

                "No sequencing markers from the current "

                "prototype list were detected."

            ),

            evidence=(

                "Zero sequencing markers detected by the "

                "current prototype rules."

            ),

            interpretation=(

                "Teacher review is recommended. Narrative "

                "organisation may still be present through "

                "features not captured by the current detector."

            )

        )



    return create_flag(

        lens="Discourse",

        status=NOT_ASSESSED,

        feature=target_genre,

        observation=(

            "Automatic discourse analysis for this genre "

            "has not yet been implemented."

        ),

        evidence="No validated genre-specific detector available.",

        interpretation=(

            "LENSuite does not make an alignment judgement "

            "for this genre."

        )

    )

def evaluate_requested_components(

    requested_components,

    answer_key_detected,

    teacher_notes_detected

):



    missing = []

    detected = []



    if "Answer key" in requested_components:



        if answer_key_detected:

            detected.append("Answer key")

        else:

            missing.append("Answer key")



    if "Teacher notes" in requested_components:



        if teacher_notes_detected:

            detected.append("Teacher notes")

        else:

            missing.append("Teacher notes")



    # Nothing was requested

    if not requested_components:



        return create_flag(

            lens="Pedagogical",

            status=NOT_ASSESSED,

            feature="Requested resource components",

            observation=(

                "No additional teacher resources "

                "were requested."

            ),

            evidence=(

                "PromptLENS contains no requested "

                "additional resource components."

            ),

            interpretation=(

                "No component-alignment judgement "

                "is required."

            )

        )



    # Something explicitly requested is missing

    if missing:



        return create_flag(

            lens="Pedagogical",

            status=MISMATCH,

            feature="Requested resource components",

            observation=(

                "One or more explicitly requested "

                "components were not detected."

            ),

            evidence=(

                "Missing: "

                + ", ".join(missing)

                + "."

            ),

            interpretation=(

                "The generated material may not fully "

                "satisfy the teacher's explicit resource "

                "specification. Teacher review is recommended."

            )

        )



    # Everything requested was detected

    return create_flag(

        lens="Pedagogical",

        status=SUPPORTED,

        feature="Requested resource components",

        observation=(

            "The explicitly requested resource "

            "components were detected."

        ),

        evidence=(

            "Detected: "

            + ", ".join(detected)

            + "."

        ),

        interpretation=(

            "Observable evidence supports correspondence "

            "between the requested additional resources "

            "and the generated material."

        )

    )

# ============================================================
# LEXICAL FLAGS
# ============================================================

def evaluate_lexical_frequency(
    analysed_items,
    vocabulary_profile="",
    vocabulary_focus="",
    material_topic=""
):
    """Context-aware corpus-frequency diagnostic."""

    review_items = []

    for item in analysed_items:
        zipf = item["zipf"]

        # Prototype review criterion only.
        # This is NOT an official CEFR threshold.
        if zipf <= 3:
            review_items.append({
                "word": item["word"],
                "pos": item["pos"],
                "zipf": zipf,
                "frequency_per_million":
                    item["frequency_per_million"]
            })

    profile_text = vocabulary_profile or "Not specified"
    focus_text = vocabulary_focus or "Not specified"
    topic_text = material_topic or "Not specified"

    teacher_context = (
        f"Teacher-selected vocabulary profile: {profile_text}. "
        f"Teacher-selected vocabulary/topic focus: {focus_text}. "
        f"Material topic/theme: {topic_text}."
    )

    if review_items:
        identified_words = ", ".join(
            item["word"] for item in review_items
        )

        return create_flag(
            lens="Lexical",
            status=REVIEW,
            feature="Vocabulary frequency",
            observation=(
                f"{len(review_items)} less common lexical "
                f"item(s) were identified for teacher review."
            ),
            evidence=(
                f"Items identified: {identified_words}. "
                "These items fall within the lower-frequency "
                "review range used by the current SUBTLEX-US "
                f"frequency analysis. {teacher_context}"
            ),
            interpretation=(
                "Less common vocabulary may increase lexical "
                "demand for some learners. However, corpus "
                "frequency alone does not establish whether a "
                "word is inappropriate, too difficult, or "
                "unsuitable for the intended CEFR level. "
                "The teacher should consider whether the item "
                "is intentionally useful for the selected "
                "material theme or vocabulary focus. LENSuite "
                "does not automatically infer semantic relevance "
                "at this stage."
            ),
            teacher_options=["KEEP", "SUPPORT", "REPLACE"]
        )

    return create_flag(
        lens="Lexical",
        status=SUPPORTED,
        feature="Vocabulary frequency",
        observation=(
            "No lower-frequency lexical items were identified "
            "by the current frequency criterion."
        ),
        evidence=(
            "No matched lexical items fell within the current "
            f"lower-frequency review range. {teacher_context}"
        ),
        interpretation=(
            "No vocabulary items were selected for "
            "frequency-based review. This does not constitute "
            "a judgement of overall lexical suitability, "
            "semantic relevance, or CEFR appropriateness."
        )
    )
