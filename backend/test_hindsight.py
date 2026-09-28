import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

client = Hindsight(
    base_url=os.getenv("HINDSIGHT_API_URL"),
    api_key=os.getenv("HINDSIGHT_API_KEY"),
)

bank_id = os.getenv("HINDSIGHT_BANK_ID", "incidentpilot")

print("Storing memory...")

client.retain(
    bank_id=bank_id,
    content="""
Incident INC-001
Service: payment-api
Status code: 500
Error: Database connection timeout

Root cause:
PostgreSQL connection pool exhaustion.

Successful resolution:
Increased the connection pool from 20 to 50
and restarted payment-api.

Resolution time: 11 minutes.
""",
    context="Resolved IncidentPilot production incident",
)

print("Memory stored successfully.")

print("\nRecalling memory...")

response = client.recall(
    bank_id=bank_id,
    query="Have we seen a database connection problem in payment-api before?"
)

print("\nRESULT:")
print(response)

client.close()