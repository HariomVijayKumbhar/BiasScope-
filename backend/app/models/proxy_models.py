from pydantic import BaseModel


class ProxyRequest(BaseModel):
    session_id: str | None = None
    dataset: list[dict]
    protected_attrs: list[str]


class ProxyFeature(BaseModel):
    feature: str
    correlated_attribute: str
    correlation: float
    risk_level: str


class ProxyResponse(BaseModel):
    proxy_features: list[ProxyFeature]
