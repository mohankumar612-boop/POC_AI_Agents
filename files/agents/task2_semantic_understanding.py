"""
Task 2: Semantic Understanding Agent
Uses Claude to understand user intent beyond keyword matching.
Different wording of the same issue maps to the same intent.
"""
import json
import anthropic


def understand_query(ticket: dict, client: anthropic.Anthropic) -> dict:
    """
    Semantic analysis: extracts intent, urgency, sentiment, keywords.
    """
    system_prompt = """You are a semantic understanding agent for IT support tickets.
Analyze the query and extract structured meaning. Users describe the same issue differently.
Your job: normalize the meaning and extract intent.

Return ONLY valid JSON, no markdown:
{
  "intent": "short normalized intent label (e.g. Login Issue, OTP Failure)",
  "urgency": "critical|high|medium|low",
  "sentiment": "frustrated|angry|confused|neutral|polite",
  "summary": "one sentence summary",
  "keywords": ["3-6 keywords"],
  "user_impact": "brief description of business impact"
}"""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=512,
        system=system_prompt,
        messages=[{"role": "user", "content": f"Analyze: {ticket['query']}"}]
    )
    raw = response.content[0].text.strip().lstrip("```json").lstrip("```").rstrip("```")
    result = json.loads(raw)
    return {**ticket, "semantic": result}
