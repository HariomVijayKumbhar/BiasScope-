from pydantic import BaseModel


class CounterfactualRequest(BaseModel):
    session_id: str | None = None
    dataset: list[dict]
    target: str
    protected_attrs: list[str]


class FlipSample(BaseModel):
    row_index: int
    protected_attribute: str
    original_value: str
    flipped_value: str
    original_prediction: int
    new_prediction: int


class CounterfactualResponse(BaseModel):
    fairness_score: float
    flip_rate: float
    risk_label: str
    sample_flips: list[FlipSample]
