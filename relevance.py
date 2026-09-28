from __future__ import annotations

import re


BIOLOGY_TERMS = {
    "cell", "dna", "rna", "protein", "enzyme", "allele", "gene", "genetic",
    "evolution", "selection", "population", "organism", "membrane", "atp",
    "photosynthesis", "respiration", "mitosis", "meiosis", "ecology", "mutation",
}


def lexical_relevance(question: str, response: str) -> float:
    """Lightweight fallback relevance score used by tests and pre-screening."""
    q = set(re.findall(r"[a-zA-Z]+", question.lower()))
    r = set(re.findall(r"[a-zA-Z]+", response.lower()))
    if not q or not r:
        return 0.0

    overlap = len(q & r) / max(1, len(q))
    bio_hits = len(r & BIOLOGY_TERMS) / max(1, min(5, len(BIOLOGY_TERMS)))
    return min(1.0, 0.75 * overlap + 0.25 * bio_hits)
