from fastapi import APIRouter

from app.models.chat_models import ChatRequest
from app.services.gemini_service import chat_reply
from app.utils.response_utils import error_response, success_response


router = APIRouter(tags=["chat"])


@router.post("/chat")
def run_chat(request: ChatRequest):
    try:
        history = [h.model_dump() for h in request.history]
        reply = chat_reply(request.message, request.audit_context, history)
        return success_response({"reply": reply})
    except Exception as exc:
        return error_response("Chat failed", f"Unexpected error: {exc}", 500)
