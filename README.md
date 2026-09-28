# BioGrade AI 🧬🤖

> A BERT + machine-translation powered **teacher-assist** system for evaluating Biology Free-Response Questions (FRQs) with rubric-grounded scoring, explainable feedback, and fairness auditing.

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Transformers](https://img.shields.io/badge/HuggingFace-Transformers-yellow)
![FastAPI](https://img.shields.io/badge/API-FastAPI-009688)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/status-research%20prototype-purple)

## Why this project exists

Biology FRQs require teachers to interpret open-ended responses, compare them against a rubric, ignore irrelevant material, and provide useful feedback. That work is time-consuming and can vary from grader to grader.

**BioGrade AI** explores whether NLP can help instructors review responses faster and more consistently. The system does **not** make final academic decisions. Instead, it produces a rubric-aligned recommendation, evidence spans, confidence information, and feedback for a teacher to review.

### Core goals

- Score responses against **explicit rubric criteria** rather than keyword matching.
- Use **BERT embeddings** to capture semantic meaning.
- Support multilingual responses with a configurable **machine-translation** stage.
- Detect off-topic or irrelevant content before scoring.
- Generate criterion-level explanations and feedback.
- Audit model behavior across language and response-style cohorts when those cohorts are available for research evaluation.
- Keep student identities out of the model pipeline by using anonymized IDs only.

---

## Architecture

```text
Student FRQ
   │
   ├──► Anonymization / validation
   │
   ├──► Language detection
   │         │
   │         └──► Translation model (if needed)
   │
   ├──► BERT encoder
   │
   ├──► Rubric semantic matcher
   │       ├── criterion similarity
   │       ├── evidence extraction
   │       └── relevance gate
   │
   ├──► Score recommendation + confidence
   │
   ├──► Fairness / drift diagnostics
   │
   └──► Teacher review dashboard / API
```

## Features

### 1. BERT rubric scoring
Each rubric criterion is embedded with BERT and compared against the student's response. The model estimates whether the response demonstrates each required biological concept.

### 2. Translation-aware grading
Responses can optionally be translated into English before scoring. The original and translated text remain separate so teachers can inspect what changed.

### 3. Relevance filtering
The pipeline computes semantic relevance between the question and response. Highly off-topic answers are flagged instead of being rewarded merely because they contain biology vocabulary.

### 4. Explainable evidence
For each rubric criterion, the system identifies the sentence that best supports the recommendation.

### 5. Fairness auditing
The evaluation module compares error rates and score distributions across configured research cohorts. It is designed for **bias detection**, not for using demographic attributes to alter a student's grade.

### 6. Human-in-the-loop workflow
Every result is a recommendation. A teacher can accept, edit, or reject the suggested criterion scores.

---

## Repository structure

```text
bio-frq-ai/
├── configs/
│   └── default.yaml
├── data/
│   └── sample/
│       ├── rubric.json
│       └── responses.csv
├── docs/
│   ├── ARCHITECTURE.md
│   └── MODEL_CARD.md
├── src/biofrq/
│   ├── api/
│   │   └── main.py
│   ├── fairness/
│   │   └── audit.py
│   ├── models/
│   │   └── bert_scorer.py
│   ├── nlp/
│   │   ├── relevance.py
│   │   └── translation.py
│   ├── pipeline.py
│   └── schemas.py
├── tests/
│   ├── test_fairness.py
│   └── test_relevance.py
├── .github/workflows/ci.yml
├── app.py
├── pyproject.toml
└── README.md
```

---

## Quick start

### 1. Clone and install

```bash
git clone https://github.com/YOUR_USERNAME/bio-frq-ai.git
cd bio-frq-ai
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

### 2. Run the API

```bash
uvicorn biofrq.api.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

### 3. Run the Streamlit demo

```bash
streamlit run app.py
```

### 4. Run tests

```bash
pytest -q
```

---

## Example request

```json
{
  "question": "Explain how natural selection can change allele frequencies in a population.",
  "response": "Individuals with advantageous heritable traits survive and reproduce more often, so alleles associated with those traits become more common over generations.",
  "rubric": [
    {
      "id": "c1",
      "description": "Identifies differential survival or reproduction"
    },
    {
      "id": "c2",
      "description": "Explains that advantageous heritable alleles increase in frequency across generations"
    }
  ]
}
```

Example response:

```json
{
  "recommended_score": 2,
  "max_score": 2,
  "relevance": 0.91,
  "criteria": [
    {
      "criterion_id": "c1",
      "awarded": true,
      "confidence": 0.88,
      "evidence": "Individuals with advantageous heritable traits survive and reproduce more often"
    },
    {
      "criterion_id": "c2",
      "awarded": true,
      "confidence": 0.90,
      "evidence": "alleles associated with those traits become more common over generations"
    }
  ],
  "requires_teacher_review": true
}
```

---

## Data design

Training and evaluation records should be de-identified before they enter this repository.

Recommended schema:

| Field | Description |
|---|---|
| `response_id` | Random identifier |
| `question_id` | FRQ identifier |
| `response_text` | Student response |
| `human_score` | Instructor-provided reference score |
| `criterion_labels` | Criterion-level labels |
| `language` | Language code if known |
| `split` | train / validation / test |

Do **not** place student names, emails, IDs, or other direct identifiers in model-training files.

---

## Model strategy

The starter implementation is intentionally modular:

- `bert-base-uncased` for English semantic encoding.
- MarianMT-compatible translation models for optional translation.
- Cosine similarity for an interpretable baseline criterion matcher.
- A configurable threshold for criterion recommendations.
- A relevance gate to reduce false positives from unrelated content.

A production research iteration could replace the baseline head with:

1. a fine-tuned BERT multi-label classifier,
2. a cross-encoder that jointly reads the response and rubric,
3. a calibrated ordinal regression head for holistic score prediction,
4. or an ensemble combining semantic similarity and criterion classification.

---

## Evaluation

Useful metrics include:

- Exact score agreement
- Quadratic weighted kappa
- Mean absolute error
- Criterion-level precision / recall / F1
- Calibration error
- Teacher override rate
- Translation vs. no-translation delta
- Performance gaps across research cohorts

The goal is **consistent teacher support**, not replacing instructor judgment.

---

## Responsible-use principles

1. **Teacher review required** for final grades.
2. **No student names** in training/evaluation datasets.
3. **No protected characteristic should be used to change an individual score.**
4. Fairness attributes, when legally and ethically available for research, should be used only for aggregate auditing.
5. The system should surface low-confidence cases rather than pretending certainty.
6. Model recommendations and teacher overrides should be logged for quality review.
7. Translation output should be inspectable because translation errors can affect downstream scoring.

See [`docs/MODEL_CARD.md`](docs/MODEL_CARD.md) for limitations and intended use.

---

## Roadmap

- [x] BERT semantic rubric matcher
- [x] Relevance detection
- [x] Optional translation layer
- [x] Criterion evidence extraction
- [x] FastAPI endpoint
- [x] Streamlit demo
- [x] Fairness-audit utilities
- [x] CI test workflow
- [ ] Fine-tune on instructor-scored Biology FRQs
- [ ] Add quadratic weighted kappa evaluation
- [ ] Add calibration curves
- [ ] Add teacher override analytics
- [ ] Add rubric versioning
- [ ] Add multilingual benchmark suite
- [ ] Add retrieval of reference course material
- [ ] Add experiment tracking with MLflow / W&B

---

## Project name ideas

- **BioGrade AI**
- **FRQ-BERT**
- **RubricLM Bio**
- **BioScore Engine**
- **GradeLens Bio**

---

## License

MIT for the starter code. Training data and educational datasets may have separate privacy, licensing, or institutional requirements.
