from fastapi import APIRouter
from pydantic import ValidationError

from app.models.detect_models import DetectRequest, DetectResponse
from app.services.gemini_service import detect_columns
from app.utils.response_utils import error_response, success_response


router = APIRouter(tags=["detect"])


def _validate_columns(payload: dict, columns: list[str]) -> DetectResponse:
    parsed = DetectResponse(**payload)
    if parsed.target_variable not in columns:
        raise ValueError("Gemini returned a target column not in dataset.")
    invalid = [col for col in parsed.protected_attributes if col not in columns]
    if invalid:
        raise ValueError(f"Gemini returned invalid protected attributes: {invalid}")
    return parsed


@router.post("/detect")
def detect(request: DetectRequest):
    try:
        try:
            payload = detect_columns(request.columns, request.sample_rows)
            parsed = _validate_columns(payload, request.columns)
        except Exception:
            payload = detect_columns(request.columns, request.sample_rows)
            parsed = _validate_columns(payload, request.columns)

        return success_response(parsed.model_dump())
    except (ValidationError, ValueError) as exc:
        return error_response("Detection failed", str(exc), 422)
    except Exception as exc:
        return error_response("Detection failed", f"Unexpected error: {exc}", 500)
