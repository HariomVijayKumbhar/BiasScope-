from datetime import datetime, timezone
from fastapi import APIRouter

from app.utils.response_utils import success_response


router = APIRouter(tags=["health"])


@router.get("/health")
def health_check():
    return success_response(
        {
            "status": "API is running",
            "version": "1.0.0",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    )
