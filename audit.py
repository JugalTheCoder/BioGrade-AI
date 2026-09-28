from __future__ import annotations

import pandas as pd


def cohort_error_audit(
    frame: pd.DataFrame,
    cohort_col: str,
    human_score_col: str = "human_score",
    model_score_col: str = "model_score",
) -> pd.DataFrame:
    """Aggregate error diagnostics. Cohort data is for auditing only, never individual scoring."""
    df = frame.copy()
    df["absolute_error"] = (df[human_score_col] - df[model_score_col]).abs()
    df["signed_error"] = df[model_score_col] - df[human_score_col]

    summary = (
        df.groupby(cohort_col, dropna=False)
        .agg(
            n=(model_score_col, "size"),
            mean_human_score=(human_score_col, "mean"),
            mean_model_score=(model_score_col, "mean"),
            mae=("absolute_error", "mean"),
            mean_signed_error=("signed_error", "mean"),
        )
        .reset_index()
    )
    return summary
