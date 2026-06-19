"""
Task 3: Dynamic Bucketing Agent
Groups similar issues into broad categories (buckets).
Enables triage at scale without manual intervention.
Buckets: Authentication, Payment, Upload, Notification, Profile, Reporting, System, Search, Support, Account
"""
import json
import anthropic
from knowledge_base.kb_records import BUCKET_LIST


def identify_bucket(ticket: dict, client: anthropic.Anthropic) -> dict:
    """
    Assigns the ticket to the most appropriate bucket using AI + known bucket taxonomy.
    """
    buckets_str = ", ".join(BUCKET_LIST)
    semantic = ticket.get("semantic", {})

    system_prompt = f"""You are a dynamic bucketing agent for IT support.
Assign the ticket to exactly ONE of these buckets: {buckets_str}

Return ONLY valid JSON, no markdown:
{{
  "bucket": "bucket name from the list",
  "confidence": 0.0-1.0,
  "reasoning": "one sentence reason"
}}"""

    content = f"""Query: {ticket['query']}
Intent: {semantic.get('intent', '')}
Keywords: {semantic.get('keywords', [])}"""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=256,
        system=system_prompt,
        messages=[{"role": "user", "content": content}]
    )
    raw = response.content[0].text.strip().lstrip("```json").lstrip("```").rstrip("```")
    result = json.loads(raw)
    return {**ticket, "bucket": result}
