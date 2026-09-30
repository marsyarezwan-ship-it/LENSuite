"""LENSuite Writing & Discourse evidence engine.
Separates Genre, Communicative Function, Discourse & Organisation, and Register.
Evidence is descriptive only: no automated writing score or CEFR certification.
"""
import re

GENRES = {
    "email": {
        "opening/greeting": [r"(?im)^\s*(?:dear|hi|hello|hey)\b"],
        "closing/sign-off": [r"(?im)^\s*(?:best wishes|best regards|kind regards|regards|take care|see you|bye|love|from|your friend|yours sincerely|yours faithfully)\b"],
        "direct address": [r"\byou\b", r"\byour\b"],
    },
    "letter": {
        "opening/greeting": [r"(?im)^\s*dear\b"],
        "closing/sign-off": [r"(?im)^\s*(?:yours sincerely|yours faithfully|best wishes|kind regards|regards)\b"],
    },
    "narrative": {
        "chronological sequencing": [r"\b(?:first|then|next|after that|later|afterwards|finally|eventually|suddenly)\b"],
        "past-time reference": [r"\b(?:yesterday|last\s+(?:night|week|weekend|month|year|holiday|school holiday)|\d+\s+(?:day|days|week|weeks|month|months|year|years)\s+ago|one day|once)\b"],
        "event progression": [r"\b(?:went|came|saw|met|visited|arrived|left|started|began|decided|returned|stayed|travelled|traveled|walked|played|enjoyed|experienced|happened)\b"],
    },
    "article": {
        "title/headline": [r"(?m)^\s*#{0,3}\s*[A-Z][^.!?]{3,80}$"],
        "developed body": [r"\b(?:for example|for instance|in addition|however|therefore|as a result)\b"],
    },
    "report": {
        "report-style heading": [r"(?im)^\s*(?:report|introduction|findings|recommendations|conclusion)\s*:?\s*$"],
        "findings/recommendation language": [r"\b(?:findings|results|it is recommended|recommendation|the results show|the findings show)\b"],
    },
    "argumentative": {
        "position/opinion": [r"\b(?:i think|i believe|in my opinion|from my point of view|it can be argued|this essay argues)\b"],
        "reason/support": [r"\b(?:because|since|therefore|for example|for instance|as a result)\b"],
        "contrast/counter-position": [r"\b(?:however|although|on the other hand|in contrast|whereas|while)\b"],
    },
    "informative": {
        "information/explanation": [r"\b(?:for example|for instance|this means|refers to|is defined as|because|therefore)\b"],
    },
    "descriptive": {
        "descriptive language": [r"\b(?:looks|seems|appears|beautiful|large|small|bright|dark|quiet|busy|friendly|interesting|colourful|colorful)\b"],
    },
    "dialogue": {
        "speaker turns": [r"(?m)^\s*[A-Z][A-Za-z .'-]{0,30}:\s+"],
        "interactional language": [r"\b(?:hello|hi|thanks|thank you|please|sorry|what do you think|do you agree)\b"],
    },
}

FUNCTIONS = {
    "describing past experiences": [
        r"\b(?:i|we)\s+(?:went|came|saw|met|visited|arrived|left|stayed|travelled|traveled|played|enjoyed|experienced|had|was|were)\b",
        r"\b(?:yesterday|last\s+(?:night|week|weekend|month|year|holiday|school holiday)|\d+\s+(?:day|days|week|weeks|month|months|year|years)\s+ago)\b",
        r"\b(?:first|then|next|after that|later|afterwards|finally)\b",
    ],
    "giving advice": [r"\b(?:you\s+should|you\s+shouldn't|you\s+could|you\s+might|you\s+ought to|why don't you|how about|i suggest|i recommend|try to)\b"],
    "making suggestions": [r"\b(?:you\s+could|you\s+might|why don't (?:you|we)|how about|what about|let's|i suggest|i recommend|perhaps|maybe)\b"],
    "expressing opinion": [r"\b(?:i think|i believe|in my opinion|from my point of view|from my perspective|i feel that)\b"],
    "giving reasons": [r"\b(?:because|since|therefore|this is because|as a result|so that)\b"],
    "describing pros and cons": [r"\b(?:advantage|disadvantage|benefit|drawback|pros?|cons?|on the one hand|on the other hand)\b"],
    "comparing": [r"\b(?:similarly|likewise|whereas|while|compared with|compared to|in contrast|however|both)\b"],
    "describing": [r"\b(?:is|are|was|were|has|have|looks|seems|appears)\b"],
    "persuading": [r"\b(?:should|must|need to|it is important|i strongly believe|therefore|for these reasons)\b"],
    "explaining": [r"\b(?:because|this means|in other words|for example|therefore|as a result|refers to)\b"],
}

COHESION = ["and","but","because","so","however","therefore","although","while","first","then","next","finally","also","in addition","for example","for instance","as a result","on the other hand","after that","later","afterwards","meanwhile","instead"]
INFORMAL = [r"\b(?:hi|hey|thanks|can't|don't|won't|i'm|you're|we're|it's|let's|bye)\b"]
FORMAL = [r"\b(?:dear sir|dear madam|yours faithfully|yours sincerely|furthermore|moreover|therefore|with regard to|i am writing to)\b"]
SEMIFORMAL = [r"\b(?:dear\s+[A-Z][A-Za-z'-]+|best wishes|kind regards|regards|thank you|please|could you|would you)\b"]


def _label(value):
    return re.sub(r"\s+", " ", (value or "").strip().lower())


def _hits(patterns, text):
    found = []
    for p in patterns:
        found.extend(m.group(0).strip() for m in re.finditer(p, text, re.I | re.M))
    return list(dict.fromkeys(found))


def _paragraphs(text):
    """Count prose-like blank-line blocks, not every worksheet line."""
    blocks = re.split(r"\n\s*\n+", (text or "").strip())
    kept = []
    for block in blocks:
        b = block.strip()
        if not b:
            continue
        words = re.findall(r"\b[\w'-]+\b", b)
        if len(words) <= 3 and not re.search(r"[.!?]", b):
            continue
        lines = [x.strip() for x in b.splitlines() if x.strip()]
        if lines and all(re.match(r"^(?:[-•*]|\d+[.)]|[A-Za-z][.)])\s+", x) or x.endswith(":") for x in lines):
            continue
        kept.append(b)
    return kept


def _function_groups(function):
    f = _label(function)
    groups = []
    if "past experience" in f: groups.append("describing past experiences")
    if "advice" in f: groups.append("giving advice")
    if "suggest" in f: groups.append("making suggestions")
    if "opinion" in f or "view" in f: groups.append("expressing opinion")
    if "reason" in f or "justify" in f: groups.append("giving reasons")
    if "pros and cons" in f or ("advantage" in f and "disadvantage" in f): groups.append("describing pros and cons")
    if "compar" in f: groups.append("comparing")
    if "persuad" in f: groups.append("persuading")
    if "explain" in f: groups.append("explaining")
    if "describ" in f and "past experience" not in f and "pros and cons" not in f: groups.append("describing")
    return list(dict.fromkeys(groups))


def analyse_writing(text, genre="", register="", communicative_function=""):
    text = text or ""
    g, r = _label(genre), _label(register)
    paragraphs = _paragraphs(text)

    genre_evidence, genre_examples = {}, {}
    for feature, patterns in GENRES.get(g, {}).items():
        found = _hits(patterns, text)
        genre_evidence[feature] = bool(found)
        genre_examples[feature] = found[:5]

    groups = _function_groups(communicative_function)
    function_evidence = {group: len(_hits(FUNCTIONS[group], text)) for group in groups}
    function_examples = {group: _hits(FUNCTIONS[group], text)[:8] for group in groups}

    lower = text.lower()
    cohesion = {}
    for marker in COHESION:
        count = len(re.findall(r"(?<!\w)" + re.escape(marker) + r"(?!\w)", lower))
        if count:
            cohesion[marker] = count

    informal, formal, semiformal = _hits(INFORMAL, text), _hits(FORMAL, text), _hits(SEMIFORMAL, text)

    return {
        "genre": genre or "Not specified",
        "register": register or "Not specified",
        "communicative_function": communicative_function or "Not specified",
        "paragraph_count": len(paragraphs),
        "paragraph_note": "Counts prose-like blank-line blocks; short headings and list/question blocks are excluded.",
        "genre_supported": g in GENRES,
        "genre_evidence": genre_evidence,
        "genre_examples": genre_examples,
        "function_supported": bool(groups),
        "function_groups": groups,
        "function_evidence": function_evidence,
        "function_examples": function_examples,
        "cohesion_marker_types": len(cohesion),
        "cohesion_markers": cohesion,
        "informal_cues": len(informal),
        "formal_cues": len(formal),
        "semi_formal_cues": len(semiformal),
        "informal_examples": informal[:8],
        "formal_examples": formal[:8],
        "semi_formal_examples": semiformal[:8],
        "reference_note": "Rule-based observable writing/discourse evidence only; this is not an automated writing score, genre certification or CEFR certification.",
    }


def _flag(lens, feature, status, observation, analysis, interpretation):
    return {"lens": lens, "feature": feature, "status": status, "observation": observation,
            "evidence": analysis["reference_note"], "interpretation": interpretation, "analysis": analysis}


def build_writing_flags(text, genre="", register="", communicative_function=""):
    a = analyse_writing(text, genre, register, communicative_function)
    flags = []

    # GENRE
    if not _label(genre):
        flags.append(_flag("Genre Lens","Genre evidence","NOT SPECIFIED","No target genre was specified.",a,"No genre comparison was attempted."))
    elif not a["genre_supported"]:
        flags.append(_flag("Genre Lens","Genre evidence","NOT ASSESSED",f"A dedicated detector for the requested genre '{genre}' is not yet available.",a,"Absence of a detector is not evidence of a mismatch."))
    else:
        present = [k for k,v in a["genre_evidence"].items() if v]
        missing = [k for k,v in a["genre_evidence"].items() if not v]
        if present:
            obs = "Observable genre-related evidence: " + ", ".join(present) + "."
            if missing: obs += " Other monitored cues not detected: " + ", ".join(missing) + "."
            status = "EVIDENCE FOUND"
        else:
            obs, status = f"No monitored {genre} genre cues were detected by the current rule set.", "REVIEW"
        flags.append(_flag("Genre Lens",f"{genre} genre evidence",status,obs,a,"Detected cues support teacher review but do not establish genre quality or task fulfilment."))

    # COMMUNICATIVE FUNCTION
    if not _label(communicative_function):
        flags.append(_flag("Communicative Function Lens","Communicative-function evidence","NOT SPECIFIED","No communicative function was specified.",a,"No communicative-function comparison was attempted."))
    elif not a["function_supported"]:
        flags.append(_flag("Communicative Function Lens","Communicative-function evidence","NOT ASSESSED",f"A dedicated detector for '{communicative_function}' is not yet available.",a,"Absence of a detector is not evidence that the function is absent."))
    else:
        total = sum(a["function_evidence"].values())
        if total:
            groups = [k for k,v in a["function_evidence"].items() if v]
            obs, status = f"Observable evidence relevant to '{communicative_function}' was detected ({total} instance(s)): " + ", ".join(groups) + ".", "EVIDENCE FOUND"
        else:
            obs, status = f"The current rule set did not detect observable cues associated with '{communicative_function}'.", "REVIEW"
        flags.append(_flag("Communicative Function Lens",communicative_function,status,obs,a,"Surface evidence can indicate representation of a communicative purpose; successful communication remains a teacher judgement."))

    # DISCOURSE & ORGANISATION
    parts = []
    if a["paragraph_count"]: parts.append(f"{a['paragraph_count']} prose-like paragraph/block(s)")
    if a["cohesion_marker_types"]: parts.append(f"{a['cohesion_marker_types']} cohesion-marker type(s)")
    status = "EVIDENCE FOUND" if parts else "REVIEW"
    obs = ("Detected " + "; ".join(parts) + ".") if parts else "Limited paragraphing/cohesion evidence was detected by the current rule set."
    flags.append(_flag("Discourse & Organisation Lens","Paragraphing, cohesion and organisation",status,obs,a,"These are descriptive organisation cues only; more paragraphs or connectors do not automatically mean better writing."))

    # REGISTER
    r = _label(register)
    if not r:
        status, obs = "NOT SPECIFIED", "No target register was specified."
    elif r == "informal":
        status = "EVIDENCE FOUND" if a["informal_cues"] else "REVIEW"
        obs = f"Detected {a['informal_cues']} observable informal-register cue(s)." if a["informal_cues"] else "Limited observable informal-register cues were detected."
    elif r == "formal":
        status = "EVIDENCE FOUND" if a["formal_cues"] else "REVIEW"
        obs = f"Detected {a['formal_cues']} observable formal-register cue(s)." if a["formal_cues"] else "Limited observable formal-register cues were detected."
    elif r in {"semi-formal","semiformal","semi formal"}:
        total = a["semi_formal_cues"] + a["formal_cues"] + a["informal_cues"]
        status = "EVIDENCE FOUND" if total else "REVIEW"
        obs = f"Observable register cues detected (semi-formal: {a['semi_formal_cues']}, formal: {a['formal_cues']}, informal: {a['informal_cues']})." if total else "Limited observable semi-formal register cues were detected."
    elif r == "neutral":
        status, obs = "PROFILED", f"Register cues profiled: {a['informal_cues']} informal, {a['semi_formal_cues']} semi-formal and {a['formal_cues']} formal cue(s)."
    else:
        status, obs = "NOT ASSESSED", f"The requested register '{register}' is not yet covered by a dedicated detector."
    flags.append(_flag("Register Lens",f"{register or 'Register'} evidence",status,obs,a,"Register depends on audience, relationship, purpose and context; keyword cues are evidence for teacher review, not an appropriateness judgement."))

    return flags


def build_writing_flag(text, genre="", register="", communicative_function=""):
    """Backward-compatible aggregate result for older code."""
    flags = build_writing_flags(text, genre, register, communicative_function)
    status = "REVIEW" if any(f["status"] in {"REVIEW","MISMATCH"} for f in flags) else "EVIDENCE FOUND"
    return {
        "lens":"Writing & Discourse Lens",
        "feature":"Genre, communicative function, discourse/organisation and register",
        "status":status,
        "observation":" ".join(f"{f['lens']}: {f['observation']}" for f in flags),
        "evidence":flags[0]["evidence"],
        "interpretation":"Use the separate evidence dimensions to support teacher review.",
        "analysis":flags[0]["analysis"],
        "component_flags":flags,
    }
