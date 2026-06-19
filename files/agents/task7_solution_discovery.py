"""
Task 7: Solution Discovery Agent
Generates multiple solution candidates based on issue type and retrieved KB cases.
Provides optionality for the ranking agent.
"""
import json
import anthropic


def discover_solutions(ticket: dict, client: anthropic.Anthropic) -> dict:
    """
    Generates Solution A, B, C based on KB retrieval and issue context.
    """
    retrieval = ticket.get("knowledge_retrieval", {})
    retrieved = retrieval.get("retrieved", [])

    kb_context = ""
    for item in retrieved[:3]:
        fr = item.get("full_record", {})
        if fr:
            kb_context += f"\n- {fr.get('issue_type')}: {fr.get('solution')} (Confidence: {fr.get('confidence', 0):.0%})"

    system_prompt = """You are a Solution Discovery Agent for IT support.
Generate exactly 3 distinct solution candidates (A, B, C) with different approaches.
Solutions must come from the KB context or be grounded in proven IT practices.

Return ONLY valid JSON, no markdown:
{
  "solutions": [
    {
      "solution_id": "A",
      "title": "short solution title",
      "approach": "brief approach description",
      "steps": ["step 1", "step 2", "step 3"],
      "estimated_time": "e.g. 10 minutes",
      "kb_grounded": true/false,
      "source_kb_id": "KB ID or null"
    }
  ]
}"""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=system_prompt,
        messages=[{"role": "user", "content": f"""Query: {ticket['query']}
Bucket: {ticket.get('bucket', {}).get('bucket', '')}
Issue Type: {ticket.get('issue_type', {}).get('issue_type', '')}

KB Knowledge:
{kb_context or 'No direct KB match - generate from IT best practices'}"""}]
    )
    raw = response.content[0].text.strip().lstrip("```json").lstrip("```").rstrip("```")
    result = json.loads(raw)
    return {**ticket, "discovered_solutions": result}
