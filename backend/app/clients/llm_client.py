import httpx
import json
from app.config import GROQ_API_KEY

BASE_URL = "https://api.groq.com/openai/v1/chat/completions"

async def summarize_cve(cve_data: dict) -> dict:
    system_prompt = """You are a cybersecurity analyst assistant.
You will be given raw CVE data. Respond ONLY with valid JSON, no markdown, no preamble, no explanation.
Base your answer STRICTLY on the provided data — never invent a CVE ID, score, or fact not present in the input.
If a field in the input data is null or missing (e.g. severity is null), output "UNKNOWN" for that field 
rather than inferring or calculating it yourself, even if you know how it could be derived.

Output format:
{
  "cve_id": string,
  "plain_summary": string (2-3 sentences, non-technical),
  "cvss_score": number or null,
  "severity": string,
  "exploitation_status": string ("known exploited" | "unknown" | "no evidence"),
  "mitigation": string
}"""

    user_message = f"Here is the CVE data:\n{json.dumps(cve_data)}"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        "temperature": 0.2,
        "response_format": {"type": "json_object"},
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(BASE_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()

    text = result["choices"][0]["message"]["content"]
    return json.loads(text)