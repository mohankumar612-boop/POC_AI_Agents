"""
Task 4: Issue Type Detection Agent
Identifies the precise issue type within a bucket.
Enables precise KB retrieval and solution matching.
"""
import json
import anthropic
from knowledge_base.kb_records import ISSUE_TYPE_MAP


def detect_issue_type(ticket: dict, client: anthropic.Anthropic) -> dict:
    """
    Detects exact issue type within the assigned bucket.
    """
    bucket_name = ticket.get("bucket", {}).get("bucket", "System")
    known_types = ISSUE_TYPE_MAP.get(bucket_name, [])
    types_str = ", ".join(known_types) if known_types else "not listed"

    system_prompt = f"""You are an issue type detection agent.
Bucket: {bucket_name}
Known issue types for this bucket: {types_str}

Identify the most precise issue type. You may use a known type or define a precise new one.

Return ONLY valid JSON, no markdown:
{{
  "issue_type": "precise issue type label",
  "matched_known": true/false,
  "confidence": 0.0-1.0,
  "sub_category": "more specific detail if needed"
}}"""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=256,
        system=system_prompt,
        messages=[{"role": "user", "content": f"Query: {ticket['query']}\nIntent: {ticket.get('semantic', {}).get('intent', '')}"}]
    )
    raw = response.content[0].text.strip().lstrip("```json").lstrip("```").rstrip("```")
    result = json.loads(raw)
    return {**ticket, "issue_type": result}
