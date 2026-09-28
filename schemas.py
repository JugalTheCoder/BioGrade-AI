from pydantic import BaseModel, Field


class RubricCriterion(BaseModel):
    id: str
    description: str
    points: int = Field(default=1, ge=0)


class GradeRequest(BaseModel):
    question: str
    response: str
    rubric: list[RubricCriterion]
    source_language: str | None = None


class CriterionResult(BaseModel):
    criterion_id: str
    awarded: bool
    points_awarded: int
    confidence: float
    evidence: str


class GradeResponse(BaseModel):
    recommended_score: int
    max_score: int
    relevance: float
    translated_response: str | None = None
    criteria: list[CriterionResult]
    requires_teacher_review: bool = True
    note: str = "Recommendation only. Final academic judgment remains with the instructor."
