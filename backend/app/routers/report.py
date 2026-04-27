from fastapi import APIRouter
from fastapi.responses import Response

from app.services.report_service import build_pdf_report
from app.utils.response_utils import error_response
from app.utils.session_store import session_store


router = APIRouter(tags=["report"])


@router.get("/report")
def generate_report(session_id: str):
    try:
        session = session_store.get(session_id)
        if not session:
            return error_response("Report failed", "Session not found", 404)

        pdf_bytes = build_pdf_report(session)
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=biasscope_report_{session_id}.pdf"},
        )
    except Exception as exc:
        return error_response("Report failed", f"Unexpected error: {exc}", 500)
