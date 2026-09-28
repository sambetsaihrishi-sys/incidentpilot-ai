from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.incident import IncidentCreate, IncidentResolution
from app.models.incident import Incident
from app.database.db import get_db
from app.services.hindsight_memory import (
    recall_similar_incidents,
    retain_resolved_incident,
)
from app.services.ai_recommendation import generate_incident_recommendation

router = APIRouter()


@router.post("/")
async def create_incident(
    incident: IncidentCreate,
    db: Session = Depends(get_db)
):
    new_incident = Incident(
        service=incident.service,
        status_code=incident.status_code,
        error_message=incident.error_message,
        endpoint=incident.endpoint,
        response_time_ms=incident.response_time_ms,
        severity=incident.severity
    )

    db.add(new_incident)
    db.commit()
    db.refresh(new_incident)

    similar_memories = await recall_similar_incidents(
        service=incident.service,
        status_code=incident.status_code,
        error_message=incident.error_message
    )

    ai_recommendation = await generate_incident_recommendation(
    service=incident.service,
    status_code=incident.status_code,
    error_message=incident.error_message,
    similar_incidents=similar_memories
)

    return {
    "message": "Incident stored successfully",
    "incident_id": new_incident.id,
    "similar_incidents": similar_memories,
    "ai_recommendation": ai_recommendation
}


@router.post("/{incident_id}/resolve")
async def resolve_incident(
    incident_id: int,
    resolution_data: IncidentResolution,
    db: Session = Depends(get_db)
):
    incident = db.query(Incident).filter(
        Incident.id == incident_id
    ).first()

    if not incident:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    memory_saved = await retain_resolved_incident(
        incident_id=incident.id,
        service=incident.service,
        status_code=incident.status_code,
        error_message=incident.error_message,
        endpoint=incident.endpoint,
        severity=incident.severity,
        root_cause=resolution_data.root_cause,
        resolution=resolution_data.resolution,
        resolution_time_minutes=resolution_data.resolution_time_minutes
    )

    return {
        "message": "Incident resolved successfully",
        "incident_id": incident.id,
        "memory_saved": memory_saved
    }


@router.get("/")
def get_incidents(db: Session = Depends(get_db)):
    incidents = db.query(Incident).all()

    return {
        "total": len(incidents),
        "incidents": incidents
    }