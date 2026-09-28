from fastapi import FastAPI

from app.api.incidents import router as incident_router
from app.database.db import Base, engine
from app.models.incident import Incident
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="IncidentPilot AI",
    description="AI-powered incident response automation platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    incident_router,
    prefix="/incidents",
    tags=["Incidents"]
)


@app.get("/")
def root():
    return {
        "message": "IncidentPilot AI backend is running"
    }