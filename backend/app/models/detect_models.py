from pydantic import BaseModel, Field


class DetectRequest(BaseModel):
    columns: list[str]
    sample_rows: list[dict]


class DetectResponse(BaseModel):
    target_variable: str
    protected_attributes: list[str]
    domain: str = Field(pattern="^(hiring|loan|medical|other)$")
    confidence: str = Field(pattern="^(high|medium|low)$")
    reasoning: str
