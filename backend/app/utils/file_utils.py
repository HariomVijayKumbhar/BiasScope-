from io import BytesIO
import json
import pandas as pd
from fastapi import UploadFile


def validate_csv_upload(file: UploadFile, max_upload_size_mb: int, content: bytes) -> None:
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise ValueError("Only .csv files are allowed.")

    max_bytes = max_upload_size_mb * 1024 * 1024
    if len(content) > max_bytes:
        raise ValueError(f"File size exceeds {max_upload_size_mb}MB limit.")


def read_csv_bytes(content: bytes) -> pd.DataFrame:
    return pd.read_csv(BytesIO(content))


def df_to_records(df: pd.DataFrame) -> list[dict]:
    return json.loads(df.to_json(orient="records"))


def dataset_to_df(dataset: list[dict]) -> pd.DataFrame:
    if not isinstance(dataset, list) or not dataset:
        raise ValueError("Dataset must be a non-empty list of records.")
    return pd.DataFrame(dataset)
