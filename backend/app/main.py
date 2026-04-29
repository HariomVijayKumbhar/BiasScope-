from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import bias, chat, counterfactual, detect, explain, health, proxy, report, upload


app = FastAPI(title="BiasScope API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(upload.router)
app.include_router(detect.router)
app.include_router(bias.router)
app.include_router(counterfactual.router)
app.include_router(proxy.router)
app.include_router(explain.router)
app.include_router(report.router)
app.include_router(chat.router)
