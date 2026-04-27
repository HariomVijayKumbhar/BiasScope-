# BiasScope Backend

## Run Locally

```bash
cd backend
python -m venv venv
source venv/bin/activate
# Windows: venv\\Scripts\\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

## Endpoints
- `GET /health`
- `POST /upload`
- `POST /detect`
- `POST /bias`
- `POST /counterfactual`
- `POST /proxy`
- `POST /explain`
- `GET /report?session_id=<id>`
- `POST /chat`
