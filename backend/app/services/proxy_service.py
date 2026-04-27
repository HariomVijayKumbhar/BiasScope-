import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency, pearsonr


def _cramers_v(x: pd.Series, y: pd.Series) -> float:
    confusion = pd.crosstab(x, y)
    if confusion.empty:
        return 0.0
    chi2 = chi2_contingency(confusion, correction=False)[0]
    n = confusion.values.sum()
    if n == 0:
        return 0.0
    phi2 = chi2 / n
    r, k = confusion.shape
    phi2corr = max(0.0, phi2 - ((k - 1) * (r - 1)) / max(n - 1, 1))
    rcorr = r - ((r - 1) ** 2) / max(n - 1, 1)
    kcorr = k - ((k - 1) ** 2) / max(n - 1, 1)
    denom = min((kcorr - 1), (rcorr - 1))
    if denom <= 0:
        return 0.0
    return float(np.sqrt(phi2corr / denom))


def _risk_label(value: float) -> str:
    if value > 0.5:
        return "High"
    if value >= 0.3:
        return "Moderate"
    return "Low"


def detect_proxy_bias(df: pd.DataFrame, protected_attrs: list[str]) -> dict:
    if not protected_attrs:
        raise ValueError("At least one protected attribute is required.")

    protected = protected_attrs[0]
    if protected not in df.columns:
        raise ValueError(f"Protected attribute '{protected}' not found.")

    rows = []
    for col in df.columns:
        if col == protected or col in protected_attrs:
            continue

        s1 = df[col]
        s2 = df[protected]

        if s1.nunique(dropna=True) <= 1 or s2.nunique(dropna=True) <= 1:
            corr = 0.0
        elif pd.api.types.is_numeric_dtype(s1) and pd.api.types.is_numeric_dtype(s2):
            corr = abs(float(pearsonr(s1.fillna(s1.median()), s2.fillna(s2.median()))[0]))
        elif not pd.api.types.is_numeric_dtype(s1) and not pd.api.types.is_numeric_dtype(s2):
            corr = abs(_cramers_v(s1.fillna("missing"), s2.fillna("missing")))
        else:
            x = pd.Series(pd.factorize(s1.fillna("missing"))[0]) if not pd.api.types.is_numeric_dtype(s1) else s1.fillna(s1.median())
            y = pd.Series(pd.factorize(s2.fillna("missing"))[0]) if not pd.api.types.is_numeric_dtype(s2) else s2.fillna(s2.median())
            corr = abs(float(pearsonr(x, y)[0]))

        rows.append(
            {
                "feature": col,
                "correlated_attribute": protected,
                "correlation": float(np.round(corr, 4)),
                "risk_level": _risk_label(corr),
            }
        )

    rows.sort(key=lambda item: item["correlation"], reverse=True)
    return {"proxy_features": rows[:10]}
