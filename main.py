from fastapi import FastAPI

from biofrq.pipeline import FRQGradingPipeline
from biofrq.schemas import GradeRequest, GradeResponse

app = FastAPI(
    title="BioGrade AI",
    version="0.1.0",
    description="Teacher-assist API for rubric-grounded Biology FRQ evaluation.",
)

pipeline = FRQGradingPipeline()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/grade", response_model=GradeResponse)
def grade_frq(request: GradeRequest) -> GradeResponse:
    return pipeline.grade(request)
