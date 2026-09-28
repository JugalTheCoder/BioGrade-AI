import pandas as pd

from biofrq.fairness.audit import cohort_error_audit


def test_cohort_error_audit_returns_expected_columns():
    df = pd.DataFrame(
        {
            "language": ["en", "en", "es", "es"],
            "human_score": [3, 2, 3, 1],
            "model_score": [3, 1, 2, 1],
        }
    )
    result = cohort_error_audit(df, "language")
    assert {"language", "n", "mae", "mean_signed_error"}.issubset(result.columns)
