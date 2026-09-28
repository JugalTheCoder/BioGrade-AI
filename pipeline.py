from __future__ import annotations

from biofrq.models.bert_scorer import BertSemanticScorer
from biofrq.schemas import CriterionResult, GradeRequest, GradeResponse


class FRQGradingPipeline:
    def __init__(
        self,
        scorer: BertSemanticScorer | None = None,
        criterion_threshold: float = 0.72,
        relevance_threshold: float = 0.40,
    ):
        self.scorer = scorer or BertSemanticScorer()
        self.criterion_threshold = criterion_threshold
        self.relevance_threshold = relevance_threshold

    def grade(self, request: GradeRequest) -> GradeResponse:
        relevance = self.scorer.similarity(request.question, request.response)
        results: list[CriterionResult] = []

        for criterion in request.rubric:
            match = self.scorer.best_evidence(request.response, criterion.description)
            awarded = relevance >= self.relevance_threshold and match.similarity >= self.criterion_threshold
            results.append(
                CriterionResult(
                    criterion_id=criterion.id,
                    awarded=awarded,
                    points_awarded=criterion.points if awarded else 0,
                    confidence=round(match.similarity, 4),
                    evidence=match.evidence,
                )
            )

        score = sum(item.points_awarded for item in results)
        max_score = sum(item.points for item in request.rubric)

        return GradeResponse(
            recommended_score=score,
            max_score=max_score,
            relevance=round(relevance, 4),
            criteria=results,
            requires_teacher_review=True,
        )
