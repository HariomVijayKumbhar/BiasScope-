from pydantic import BaseModel


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    audit_context: dict
    history: list[ChatMessage] = []


class ChatResponse(BaseModel):
    reply: str
