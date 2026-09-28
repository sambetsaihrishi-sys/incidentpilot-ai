import os

from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

HINDSIGHT_API_URL = os.getenv("HINDSIGHT_API_URL")
HINDSIGHT_API_KEY = os.getenv("HINDSIGHT_API_KEY")
HINDSIGHT_BANK_ID = os.getenv("HINDSIGHT_BANK_ID", "incidentpilot")

client = Hindsight(
    base_url=HINDSIGHT_API_URL,
    api_key=HINDSIGHT_API_KEY,
)


async def recall_similar_incidents(
    service: str,
    status_code: int,
    error_message: str,
):
    query = f"""
    Find previous resolved production incidents similar to this incident.

    Service: {service}
    Status code: {status_code}
    Error: {error_message}

    Return memories that may help diagnose or resolve this incident.
    """

    try:
        response = await client.arecall(
            bank_id=HINDSIGHT_BANK_ID,
            query=query,
            max_tokens=1000,
        )

        return [result.text for result in response.results[:3]]

    except Exception as e:
        print(f"Hindsight recall error: {e}")
        return []


async def retain_resolved_incident(
    incident_id: int,
    service: str,
    status_code: int,
    error_message: str,
    endpoint: str,
    severity: str,
    root_cause: str,
    resolution: str,
    resolution_time_minutes: int,
):
    memory = f"""
    Resolved production incident.

    Incident ID: {incident_id}
    Service: {service}
    Status code: {status_code}
    Endpoint: {endpoint}
    Severity: {severity}
    Error: {error_message}

    Root cause:
    {root_cause}

    Successful resolution:
    {resolution}

    Resolution time:
    {resolution_time_minutes} minutes.

    This resolution was confirmed successful.
    """

    try:
        await client.aretain(
            bank_id=HINDSIGHT_BANK_ID,
            content=memory,
            context="Resolved IncidentPilot production incident",
        )

        return True

    except Exception as e:
        print(f"Hindsight retain error: {e}")
        return False