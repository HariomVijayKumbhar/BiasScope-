from dataclasses import dataclass, field
import os
from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    environment: str = os.getenv("ENVIRONMENT", "development")
    max_upload_size_mb: int = int(os.getenv("MAX_UPLOAD_SIZE_MB", "50"))
    max_rows_for_counterfactual: int = int(os.getenv("MAX_ROWS_FOR_COUNTERFACTUAL", "1000"))
    allowed_origins: list[str] = field(
        default_factory=lambda: [
            item.strip()
            for item in os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
            if item.strip()
        ]
    )


settings = Settings()
