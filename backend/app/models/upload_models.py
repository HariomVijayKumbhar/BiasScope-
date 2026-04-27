from pydantic import BaseModel


class UploadData(BaseModel):
    session_id: str
    columns: list[str]
    preview: list[dict]
    row_count: int
    column_count: int
