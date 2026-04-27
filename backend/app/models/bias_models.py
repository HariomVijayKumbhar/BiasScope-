from pydantic import BaseModel


class BiasRequest(BaseModel):
    session_id: str | None = None
    dataset: list[dict]
    target: str
    protected_attrs: list[str]


class MetricResult(BaseModel):
    name: str
    value: float
    passed: bool
    threshold: str
    description: str
    interpretation: str


class BiasResponse(BaseModel):
    metrics: list[MetricResult]
    overall_passed: bool
    protected_attribute: str
    privileged_group: str
    unprivileged_group: str
