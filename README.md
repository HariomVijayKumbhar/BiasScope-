# BiasScope

BiasScope is a no-code, AI-powered bias auditing platform.

## Project Structure
- `backend/` FastAPI API with CSV upload, detection, fairness analysis, report generation, and chat routes.
- `frontend/` React + Tailwind dashboard for upload, audit visualization, recommendations, report download, and chat.

## Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate
# Windows: venv\\Scripts\\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

## Frontend Setup
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

## Access
- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`
