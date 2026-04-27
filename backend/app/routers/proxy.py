import pandas as pd
from fastapi import APIRouter

from app.models.proxy_models import ProxyRequest
from app.services.proxy_service import detect_proxy_bias
from app.utils.response_utils import error_response, success_response
from app.utils.session_store import session_store


router = APIRouter(tags=["proxy"])


@router.post("/proxy")
def run_proxy(request: ProxyRequest):
    try:
        df = pd.DataFrame(request.dataset)
        result = detect_proxy_bias(df, request.protected_attrs)

        if request.session_id:
            session_store.update(request.session_id, {"proxy_results": result})

        return success_response(result)
    except Exception as exc:
        return error_response("Proxy detection failed", str(exc), 422)
