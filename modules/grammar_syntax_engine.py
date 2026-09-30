"""LENSuite Grammar & Syntax evidence engine.

Rule-based evidence detection for common English grammar/syntax targets encountered
across Malaysian primary and secondary ELT. It reports observable evidence only;
it does not assign CEFR mastery or certify curriculum suitability.
"""
import re
from collections import Counter

PATTERNS = {
    "be": [r"\b(?:am|is|are|was|were|be|been|being)\b"],
    "have": [r"\b(?:have|has|had)\b"],
    "present simple": [r"\b(?:do|does|don't|doesn't)\b", r"\b\w+s\b"],
    "present continuous": [r"\b(?:am|is|are)\s+\w+ing\b"],
    "past simple": [r"\b\w+ed\b", r"\b(?:was|were|went|had|did|said|came|saw|took|made|got|gave|found|thought|told|left|felt|brought|began|wrote|ran|ate|drank)\b"],
    "past continuous": [r"\b(?:was|were)\s+\w+ing\b"],
    "present perfect": [r"\b(?:have|has)\s+(?:\w+ed|been|done|gone|seen|made|taken|written|given|known|found|thought|told)\b"],
    "past perfect": [r"\bhad\s+(?:\w+ed|been|done|gone|seen|made|taken|written|given|known|found|thought|told)\b"],
    "future will": [r"\bwill(?:\s+not|n't)?\s+\w+\b"],
    "going to": [r"\b(?:am|is|are)\s+going\s+to\s+\w+\b"],
    "modal verbs": [r"\b(?:can|could|may|might|must|shall|should|will|would)\b", r"\bought\s+to\b", r"\bhave\s+to\b"],
    "advice and suggestions": [r"\b(?:should|shouldn't|could|might|ought\s+to)\b", r"\bwhy\s+don't\s+you\b", r"\bhow\s+about\b", r"\bi\s+(?:suggest|recommend)\b"],
    "ability": [r"\b(?:can|can't|could|couldn't|be able to)\b"],
    "permission": [r"\b(?:can|could|may)\s+(?:i|we|you)\b"],
    "obligation": [r"\b(?:must|have\s+to|has\s+to|need\s+to)\b"],
    "possibility": [r"\b(?:may|might|could)\b"],
    "articles": [r"\b(?:a|an|the)\b"],
    "quantifiers": [r"\b(?:some|any|much|many|a lot of|lots of|few|a few|little|a little|enough|several)\b"],
    "comparatives": [r"\b\w+er\s+than\b", r"\bmore\s+\w+\s+than\b", r"\bless\s+\w+\s+than\b"],
    "superlatives": [r"\bthe\s+\w+est\b", r"\bthe\s+most\s+\w+\b", r"\bthe\s+least\s+\w+\b"],
    "imperatives": [r"(?m)^(?:please\s+)?[A-Za-z]+\b"],
    "there is are": [r"\bthere\s+(?:is|are|was|were)\b"],
    "wh questions": [r"\b(?:who|what|when|where|why|which|whose|how)\b[^?.!]*\?"],
    "yes no questions": [r"\b(?:am|is|are|was|were|do|does|did|have|has|had|can|could|will|would|should|may|might|must)\b[^?.!]*\?"],
    "relative clauses": [r"\b(?:who|whom|whose|which|that)\b"],
    "conditionals": [r"\bif\b[^.!?]*\b(?:will|would|can|could|may|might|present|past)\b", r"\bif\b"],
    "passive voice": [r"\b(?:am|is|are|was|were|be|been|being)\s+\w+(?:ed|en)\b"],
    "reported speech": [r"\b(?:said|told|asked|reported|explained)\b(?:\s+that)?\b"],
    "gerunds": [r"\b\w+ing\b"],
    "infinitives": [r"\bto\s+[a-z]+\b"],
    "coordination": [r"\b(?:and|but|or|so|yet)\b"],
    "subordination": [r"\b(?:because|although|though|while|when|before|after|if|unless|since|so that|whereas)\b"],
}

ALIASES = {
    "simple present": "present simple", "present tense": "present simple",
    "present progressive": "present continuous", "simple past": "past simple",
    "past tense": "past simple", "past progressive": "past continuous",
    "modals": "modal verbs", "modal": "modal verbs",
    "modal verbs for advice and suggestions": "advice and suggestions",
    "modal verbs for advice and suggestion": "advice and suggestions",
    "advice": "advice and suggestions", "suggestions": "advice and suggestions",
    "comparative adjectives": "comparatives", "superlative adjectives": "superlatives",
    "passive": "passive voice", "reported language": "reported speech",
    "relative clause": "relative clauses", "conditional": "conditionals",
    "question forms": "wh questions", "wh-questions": "wh questions",
}

def _normalise_target(target):
    t = re.sub(r"\s+", " ", (target or "").strip().lower())
    if t in ALIASES: return ALIASES[t]
    for alias, canonical in ALIASES.items():
        if alias in t: return canonical
    for canonical in PATTERNS:
        if canonical in t: return canonical
    return t

def analyse_grammar_syntax(text, target=""):
    canonical = _normalise_target(target)
    patterns = PATTERNS.get(canonical, [])
    hits=[]
    for pattern in patterns:
        hits.extend(m.group(0) for m in re.finditer(pattern, text, flags=re.I|re.M))
    # General syntax evidence is useful regardless of selected target.
    sentences=[s.strip() for s in re.split(r'(?<=[.!?])\s+', " ".join(text.split())) if s.strip()]
    coordination=sum(len(re.findall(PATTERNS["coordination"][0], s, flags=re.I)) for s in sentences)
    subordination=sum(len(re.findall(PATTERNS["subordination"][0], s, flags=re.I)) for s in sentences)
    complex_candidates=sum(1 for s in sentences if re.search(PATTERNS["subordination"][0], s, flags=re.I))
    compound_candidates=sum(1 for s in sentences if re.search(PATTERNS["coordination"][0], s, flags=re.I))
    return {
        "requested_target": target or "Not specified",
        "canonical_target": canonical or "not specified",
        "supported_target": bool(patterns),
        "evidence_count": len(hits),
        "evidence_examples": list(dict.fromkeys(hits))[:12],
        "sentence_count": len(sentences),
        "coordination_markers": coordination,
        "subordination_markers": subordination,
        "compound_sentence_candidates": compound_candidates,
        "complex_sentence_candidates": complex_candidates,
        "reference_note": "Rule-based observable evidence only; this does not establish grammatical accuracy, CEFR mastery, or curriculum suitability."
    }

def build_grammar_flag(text, target=""):
    a=analyse_grammar_syntax(text,target)
    if not (target or "").strip():
        return {"lens":"Grammar & Syntax Lens","feature":"Grammar target","status":"NOT SPECIFIED","observation":"No specific grammar target was supplied.","evidence":a["reference_note"],"interpretation":"Use the general syntax profile descriptively; no target-specific judgement is made.","analysis":a}
    if not a["supported_target"]:
        return {"lens":"Grammar & Syntax Lens","feature":target,"status":"NOT ASSESSED","observation":f"The current rule-based registry does not yet have a reliable detector for '{target}'.","evidence":a["reference_note"],"interpretation":"The target remains for teacher review rather than being inferred automatically.","analysis":a}
    if a["evidence_count"]:
        examples=", ".join(a["evidence_examples"][:8])
        return {"lens":"Grammar & Syntax Lens","feature":target,"status":"EVIDENCE FOUND","observation":f"Detected {a['evidence_count']} observable instance(s) relevant to the selected target. Examples: {examples}.","evidence":a["reference_note"],"interpretation":"The detected forms provide evidence that the target is represented. Accuracy, range, meaning and pedagogical appropriateness remain teacher judgements.","analysis":a}
    return {"lens":"Grammar & Syntax Lens","feature":target,"status":"REVIEW","observation":f"No observable instances matching the current detector for '{target}' were found.","evidence":a["reference_note"],"interpretation":"Review whether the requested grammar focus needs clearer representation in the learner-facing material.","analysis":a}
