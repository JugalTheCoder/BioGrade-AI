# Model Card: BioGrade AI

## Intended use

BioGrade AI is a research prototype designed to help teachers review Biology free-response answers against explicit rubrics.

## Not intended for

- Fully autonomous final grades
- Admissions, discipline, placement, or other high-impact student decisions
- Inferring student identity or protected characteristics
- Scoring based on demographic attributes

## Inputs

- Biology FRQ prompt
- Student response
- Explicit rubric criteria
- Optional language metadata for translation routing

## Outputs

- Recommended rubric score
- Criterion-level point suggestions
- Semantic confidence values
- Evidence text spans
- Relevance score

## Known limitations

- BERT similarity is not equivalent to true biological reasoning.
- Negation can be difficult for embedding-only approaches.
- Translation can alter scientific meaning.
- Short answers may have unstable similarity values.
- Rubric wording strongly affects predictions.
- Confidence values from raw semantic similarity are not calibrated probabilities.
- The baseline model has not been established as suitable for real-world grading without task-specific validation.

## Fairness

The repository includes aggregate cohort-error diagnostics for research auditing. Cohort attributes must never be used to raise or lower an individual student's score. Any fairness evaluation should comply with school policy, law, consent requirements, and privacy controls.

## Human oversight

The application deliberately returns `requires_teacher_review = true` for all evaluations.
