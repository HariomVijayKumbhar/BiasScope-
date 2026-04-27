import pandas as pd
from fastapi import APIRouter

from app.models.bias_models import BiasRequest
from app.services.bias_service import calculate_bias_metrics
from app.utils.response_utils import error_response, success_response
from app.utils.session_store import session_store


router = APIRouter(tags=["bias"])


@router.post("/bias")
def run_bias(request: BiasRequest):
    try:
        df = pd.DataFrame(request.dataset)
        protected = request.protected_attrs[0] if request.protected_attrs else ""
        result = calculate_bias_metrics(df, request.target, protected)

        if request.session_id:
            session_store.update(request.session_id, {"bias_results": result})

        return success_response(result)
    except Exception as exc:
        return error_response("Bias analysis failed", str(exc), 422)
