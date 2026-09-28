import os

from dotenv import load_dotenv
from groq import AsyncGroq

load_dotenv()

client = AsyncGroq(
    api_key=os.getenv("GROQ_API_KEY")
)


async def generate_incident_recommendation(
    service: str,
    status_code: int,
    error_message: str,
    similar_incidents: list[str],
):
    memories = "\n".join(
        f"- {memory}" for memory in similar_incidents
    )

    prompt = f"""
You are IncidentPilot, a production incident response assistant.

CURRENT INCIDENT
Service: {service}
Status code: {status_code}
Error: {error_message}

RECALLED HINDSIGHT MEMORIES
{memories if memories else "No relevant previous incidents found."}

Your job is to recommend the safest next troubleshooting steps.

STRICT RULES:
- Use only facts from the current incident and recalled memories.
- Never invent previous actions, incidents, metrics, deployments, or outcomes.
- If something is not supported by memory, say it should be verified.
- Keep the answer concise enough to read in under 30 seconds.
- Maximum 3 recommended actions.
- Do not use Markdown tables.
- Do not use **bold**, # headings, or other Markdown formatting.

Return exactly this format:

LIKELY CAUSE
One short paragraph.

RECOMMENDED ACTIONS
1. Action
2. Action
3. Action

MEMORY EVIDENCE
One short paragraph explaining which previous incident/fix supports this recommendation.

CONFIDENCE
High, Medium, or Low - followed by one short reason.
"""

    try:
        response = await client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
    "role": "system",
    "content": (
        "You are IncidentPilot. Give concise, evidence-grounded "
        "production incident recommendations using Hindsight memory. "
        "Never claim a historical fact unless it appears in the supplied memories."
    )
},
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2
        )

        return response.choices[0].message.content

    except Exception as e:
        print(f"AI recommendation error: {e}")
        return "AI recommendation unavailable."