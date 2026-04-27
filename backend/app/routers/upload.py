from fastapi import APIRouter, File, UploadFile

from app.config import settings
from app.utils.file_utils import df_to_records, read_csv_bytes, validate_csv_upload
from app.utils.response_utils import error_response, success_response
from app.utils.session_store import session_store


router = APIRouter(tags=["upload"])


@router.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    try:
        content = await file.read()
        validate_csv_upload(file, settings.max_upload_size_mb, content)
        df = read_csv_bytes(content)

        session_id = session_store.create(
            {
                "dataset": df_to_records(df),
                "columns": df.columns.tolist(),
                "row_count": int(len(df)),
                "column_count": int(df.shape[1]),
            }
        )

        return success_response(
            {
                "session_id": session_id,
                "columns": df.columns.tolist(),
                "preview": df_to_records(df.head(5)),
                "dataset": df_to_records(df),
                "row_count": int(len(df)),
                "column_count": int(df.shape[1]),
            }
        )
    except ValueError as exc:
        return error_response("Upload failed", str(exc), 422)
    except Exception as exc:
        return error_response("Upload failed", f"Unexpected error: {exc}", 500)
