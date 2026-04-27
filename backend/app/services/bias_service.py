import numpy as np
import pandas as pd


def _binarize(series: pd.Series) -> pd.Series:
    if pd.api.types.is_numeric_dtype(series):
        threshold = series.median()
        return (series >= threshold).astype(int)
    return series.astype(str).str.lower().isin(["1", "true", "yes", "approved", "selected", "pass"]).astype(int)


def _pass_fail_abs_threshold(value: float, threshold: float = 0.1) -> bool:
    return abs(value) <= threshold


def calculate_bias_metrics(df: pd.DataFrame, target: str, protected_attr: str) -> dict:
    if target not in df.columns:
        raise ValueError(f"Target column '{target}' not found.")
    if protected_attr not in df.columns:
        raise ValueError(f"Protected attribute '{protected_attr}' not found.")

    work = df.copy()
    work["y_hat"] = _binarize(work[target])
    groups = work[protected_attr].dropna().astype(str)

    if groups.nunique() < 2:
        raise ValueError("Protected attribute must have at least two groups.")

    group_rates = []
    for g in sorted(groups.unique()):
        mask = work[protected_attr].astype(str) == g
        rate = work.loc[mask, "y_hat"].mean() if mask.any() else 0.0
        group_rates.append((g, float(rate)))

    privileged_group, privileged_rate = max(group_rates, key=lambda x: x[1])
    unprivileged_group, unprivileged_rate = min(group_rates, key=lambda x: x[1])

    # Demographic Parity Difference: P(y_hat=1|unpriv) - P(y_hat=1|priv)
    demographic_parity_difference = unprivileged_rate - privileged_rate

    # Equal Opportunity Difference: approximate using target as label if no separate label exists.
    y_true = _binarize(work[target])
    def tpr(group_name: str) -> float:
        mask = (work[protected_attr].astype(str) == group_name) & (y_true == 1)
        denom = mask.sum()
        if denom == 0:
            return 0.0
        numer = ((work["y_hat"] == 1) & mask).sum()
        return float(numer / denom)

    equal_opportunity_difference = tpr(unprivileged_group) - tpr(privileged_group)

    # Disparate Impact Ratio: P(y_hat=1|unpriv) / P(y_hat=1|priv)
    disparate_impact_ratio = float(unprivileged_rate / privileged_rate) if privileged_rate > 0 else 0.0

    metrics = [
        {
            "name": "Demographic Parity Difference",
            "value": float(np.round(demographic_parity_difference, 6)),
            "passed": _pass_fail_abs_threshold(demographic_parity_difference, 0.1),
            "threshold": "|value| <= 0.1",
            "description": "Checks whether positive outcomes are similarly distributed across groups.",
            "interpretation": "Lower absolute values indicate more balanced selection outcomes.",
        },
        {
            "name": "Equal Opportunity Difference",
            "value": float(np.round(equal_opportunity_difference, 6)),
            "passed": _pass_fail_abs_threshold(equal_opportunity_difference, 0.1),
            "threshold": "|value| <= 0.1",
            "description": "Compares true positive rates between protected groups.",
            "interpretation": "Values near zero indicate comparable opportunity across groups.",
        },
        {
            "name": "Disparate Impact Ratio",
            "value": float(np.round(disparate_impact_ratio, 6)),
            "passed": 0.8 <= disparate_impact_ratio <= 1.25,
            "threshold": "0.8 <= value <= 1.25",
            "description": "Measures selection-rate parity ratio between unprivileged and privileged groups.",
            "interpretation": "Values outside [0.8, 1.25] suggest potentially adverse impact.",
        },
    ]

    return {
        "metrics": metrics,
        "overall_passed": all(m["passed"] for m in metrics),
        "protected_attribute": protected_attr,
        "privileged_group": privileged_group,
        "unprivileged_group": unprivileged_group,
    }
