from biofrq.nlp.relevance import lexical_relevance


def test_relevant_biology_response_scores_above_unrelated_response():
    q = "Explain how natural selection changes allele frequencies in a population"
    relevant = "Natural selection changes allele frequencies when organisms with heritable traits reproduce more."
    unrelated = "My favorite movie has great music and cinematography."
    assert lexical_relevance(q, relevant) > lexical_relevance(q, unrelated)
