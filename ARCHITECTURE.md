# Architecture

## Pipeline stages

1. **Input validation**: Accept question, anonymized response, and rubric criteria.
2. **Translation (optional)**: Translate non-English text to the model's scoring language.
3. **Relevance gate**: Estimate whether the response addresses the FRQ prompt.
4. **BERT encoding**: Produce contextual embeddings for the answer and rubric criteria.
5. **Criterion matching**: Compare each criterion with the strongest supporting sentence.
6. **Recommendation generation**: Suggest criterion-level points with confidence values.
7. **Teacher review**: Instructor makes the final scoring decision.
8. **Offline audit**: Compare model vs. teacher labels for accuracy, calibration, and group-level error patterns.

## Why criterion-level scoring?

Holistic score prediction can hide why a model assigned a score. Criterion-level outputs give teachers a more inspectable result and make error analysis easier.

## Future production architecture

A stronger version could use a fine-tuned cross-encoder:

```text
[CLS] Rubric Criterion [SEP] Student Response [SEP]
                 │
                 ▼
         Fine-tuned BERT
                 │
        ┌────────┴────────┐
        ▼                 ▼
 criterion probability   evidence span
```

A separate ordinal model could estimate the holistic score, but the UI should still expose criterion-level evidence.
