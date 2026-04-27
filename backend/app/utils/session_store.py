from datetime import datetime, timezone
from uuid import uuid4


class SessionStore:
    def __init__(self) -> None:
        self._store: dict[str, dict] = {}

    def create(self, payload: dict) -> str:
        session_id = str(uuid4())
        self._store[session_id] = {
            "created_at": datetime.now(timezone.utc).isoformat(),
            **payload,
        }
        return session_id

    def update(self, session_id: str, payload: dict) -> None:
        if session_id not in self._store:
            return
        self._store[session_id].update(payload)

    def get(self, session_id: str) -> dict | None:
        return self._store.get(session_id)


session_store = SessionStore()
