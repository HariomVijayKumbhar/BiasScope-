import pandas as pd
from fastapi import APIRouter

from app.config import settings
from app.models.counterfactual_models import CounterfactualRequest
from app.services.counterfactual_service import calculate_counterfactual
from app.utils.response_utils import error_response, success_response
from app.utils.session_store import session_store


router = APIRouter(tags=["counterfactual"])


@router.post("/counterfactual")
def run_counterfactual(request: CounterfactualRequest):
    try:
        df = pd.DataFrame(request.dataset)
        result = calculate_counterfactual(df, request.target, request.protected_attrs, settings.max_rows_for_counterfactual)

        if request.session_id:
            session_store.update(request.session_id, {"counterfactual_results": result})

        return success_response(result)
    except Exception as exc:
        return error_response("Counterfactual analysis failed", str(exc), 422)
