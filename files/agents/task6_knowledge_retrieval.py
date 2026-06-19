"""
Task 6: Knowledge Retrieval Agent
Finds semantically similar previously solved cases from the KB.
Leverages historical resolution data to ground AI recommendations.
"""
import json
import anthropic
from agents.task5_knowledge_base import search_kb_by_bucket_and_type, get_all_kb_records


def retrieve_knowledge(ticket: dict, client: anthropic.Anthropic) -> dict:
    """
    Retrieves the top semantically similar KB cases for the ticket.
    """
    bucket = ticket.get("bucket", {}).get("bucket", "")
    issue_type = ticket.get("issue_type", {}).get("issue_type", "")

    # Pre-filter KB by bucket and issue type
    candidate_records = search_kb_by_bucket_and_type(bucket, issue_type)

    if not candidate_records:
        # Fallback: get all records and let AI pick
        candidate_records = get_all_kb_records()[:15]

    kb_snippet = json.dumps([{
        "id": r["id"], "issue_type": r["issue_type"],
        "solution": r["solution"], "confidence": r["confidence"],
        "risk_level": r["risk_level"]
    } for r in candidate_records], indent=2)

    system_prompt = """You are a Knowledge Retrieval Agent.
Given a ticket and KB records, select the TOP 3 most relevant records.

Return ONLY valid JSON, no markdown:
{
  "retrieved": [
    {
      "kb_id": "KB ID",
      "issue_type": "matched issue type",
      "relevance_score": 0.0-1.0,
      "relevance_reason": "why this matches"
    }
  ],
  "retrieval_confidence": 0.0-1.0
}"""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=512,
        system=system_prompt,
        messages=[{"role": "user", "content": f"""Query: {ticket['query']}
Bucket: {bucket}
Issue Type: {issue_type}

KB Candidates:
{kb_snippet}"""}]
    )
    raw = response.content[0].text.strip().lstrip("```json").lstrip("```").rstrip("```")
    retrieval = json.loads(raw)

    # Enrich with full KB records
    kb_map = {r["id"]: r for r in candidate_records}
    enriched = []
    for item in retrieval.get("retrieved", []):
        full_rec = kb_map.get(item["kb_id"], {})
        enriched.append({**item, "full_record": full_rec})

    retrieval["retrieved"] = enriched
    return {**ticket, "knowledge_retrieval": retrieval}
