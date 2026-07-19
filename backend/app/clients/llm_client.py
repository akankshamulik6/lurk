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

from app.clients.nvd_client import get_cve_details
from app.clients.abuseipdb_client import check_ip_reputation
from app.clients.virustotal_client import check_file_hash

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_cve_details",
            "description": "Look up details for a specific CVE ID, including CVSS score and description.",
            "parameters": {
                "type": "object",
                "properties": {
                    "cve_id": {"type": "string", "description": "CVE ID, e.g. CVE-2024-3094"}
                },
                "required": ["cve_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "check_ip_reputation",
            "description": "Check if an IP address is known malicious using AbuseIPDB.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ip": {"type": "string", "description": "IPv4 address to check"}
                },
                "required": ["ip"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "check_file_hash",
            "description": "Check a file hash (MD5/SHA1/SHA256) against VirusTotal for malware detection.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_hash": {"type": "string"}
                },
                "required": ["file_hash"],
            },
        },
    },
]

TOOL_FUNCTIONS = {
    "get_cve_details": get_cve_details,
    "check_ip_reputation": check_ip_reputation,
    "check_file_hash": check_file_hash,
}
async def run_agent(user_question: str) -> str:
    system_prompt = """You are a threat intelligence analyst assistant.
Use the available tools to answer the user's question with real data — never guess or invent facts.
If the question doesn't require a tool, answer directly using only general security knowledge, and say so clearly."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_question},
    ]

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient() as client:
        while True:
            payload = {
                "model": "llama-3.3-70b-versatile",
                "messages": messages,
                "tools": TOOLS,
                "tool_choice": "auto",
                "temperature": 0.2,
            }

            response = await client.post(BASE_URL, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            result = response.json()

            message = result["choices"][0]["message"]
            tool_calls = message.get("tool_calls")

            if tool_calls:
                messages.append(message)

                for call in tool_calls:
                    tool_name = call["function"]["name"]
                    tool_args = json.loads(call["function"]["arguments"])
                    func = TOOL_FUNCTIONS[tool_name]
                    tool_output = await func(**tool_args)

                    messages.append({
                        "role": "tool",
                        "tool_call_id": call["id"],
                        "content": json.dumps(tool_output),
                    })

                continue  # loop back so the model can respond with the tool data

            return message["content"]