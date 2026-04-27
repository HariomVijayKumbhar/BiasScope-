import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


def _build_model(df: pd.DataFrame, target: str) -> tuple[Pipeline, pd.DataFrame, pd.Series]:
    y = (df[target].astype(str).str.lower().isin(["1", "true", "yes", "approved", "selected", "pass"]).astype(int))
    X = df.drop(columns=[target])

    numeric_cols = X.select_dtypes(include=["number"]).columns.tolist()
    categorical_cols = [c for c in X.columns if c not in numeric_cols]

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", Pipeline([("imputer", SimpleImputer(strategy="median"))]), numeric_cols),
            (
                "cat",
                Pipeline([
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("onehot", OneHotEncoder(handle_unknown="ignore")),
                ]),
                categorical_cols,
            ),
        ]
    )

    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", LogisticRegression(max_iter=300, random_state=42)),
        ]
    )
    model.fit(X, y)
    return model, X, y


def _flip_value(series: pd.Series, value):
    uniq = [x for x in series.dropna().unique().tolist()]
    if len(uniq) < 2:
        return value
    if pd.api.types.is_numeric_dtype(series):
        median = float(series.median())
        return median if value != median else float(series.mean())
    for candidate in uniq:
        if candidate != value:
            return candidate
    return value


def calculate_counterfactual(df: pd.DataFrame, target: str, protected_attrs: list[str], max_rows: int) -> dict:
    if target not in df.columns:
        raise ValueError(f"Target column '{target}' not found.")
    if not protected_attrs:
        raise ValueError("At least one protected attribute is required.")

    protected = protected_attrs[0]
    if protected not in df.columns:
        raise ValueError(f"Protected attribute '{protected}' not found.")

    sample_df = df.head(max_rows).copy()
    model, X, _ = _build_model(sample_df, target)

    original_pred = model.predict(X)
    cf_X = X.copy()
    cf_X[protected] = cf_X[protected].apply(lambda v: _flip_value(X[protected], v))
    cf_pred = model.predict(cf_X)

    changed_mask = original_pred != cf_pred
    flip_rate = float(np.round(changed_mask.mean() * 100, 4))
    fairness_score = float(np.round(100.0 - flip_rate, 4))

    if flip_rate < 5:
        risk_label = "Very Fair"
    elif flip_rate <= 20:
        risk_label = "Moderate Concern"
    else:
        risk_label = "High Risk - Immediate Review Required"

    flips = []
    changed_indices = np.where(changed_mask)[0][:20]
    for idx in changed_indices:
        flips.append(
            {
                "row_index": int(idx),
                "protected_attribute": protected,
                "original_value": str(X.iloc[idx][protected]),
                "flipped_value": str(cf_X.iloc[idx][protected]),
                "original_prediction": int(original_pred[idx]),
                "new_prediction": int(cf_pred[idx]),
            }
        )

    return {
        "fairness_score": fairness_score,
        "flip_rate": flip_rate,
        "risk_label": risk_label,
        "sample_flips": flips,
    }
