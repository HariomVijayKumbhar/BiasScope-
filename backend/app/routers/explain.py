from fastapi import APIRouter
from pydantic import ValidationError

from app.models.explain_models import ExplainRequest, ExplainResponse
from app.services.gemini_service import explain_audit
from app.utils.response_utils import error_response, success_response
from app.utils.session_store import session_store


router = APIRouter(tags=["explain"])


@router.post("/explain")
def run_explain(request: ExplainRequest):
    try:
        payload = {
            "bias_results": request.bias_results,
            "counterfactual_results": request.counterfactual_results,
            "proxy_results": request.proxy_results,
            "domain": request.domain,
            "protected_attribute": request.protected_attribute,
        }
        response = explain_audit(payload)
        parsed = ExplainResponse(**response)

        if request.session_id:
            session_store.update(request.session_id, {"explain_results": parsed.model_dump()})

        return success_response(parsed.model_dump())
    except ValidationError as exc:
        return error_response("Explain failed", str(exc), 422)
    except Exception as exc:
        return error_response("Explain failed", f"Unexpected error: {exc}", 500)
