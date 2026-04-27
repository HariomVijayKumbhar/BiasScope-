from pydantic import BaseModel, Field


class ExplainRequest(BaseModel):
    session_id: str | None = None
    bias_results: dict
    counterfactual_results: dict
    proxy_results: dict
    domain: str = "other"
    protected_attribute: str = ""


class Issue(BaseModel):
    title: str
    description: str
    metric: str


class Recommendation(BaseModel):
    title: str
    description: str
    priority: str = Field(pattern="^(immediate|short-term|long-term)$")
    code: str


class ExplainResponse(BaseModel):
    summary: str
    severity: str = Field(pattern="^(critical|high|medium|low)$")
    issues: list[Issue]
    recommendations: list[Recommendation]
