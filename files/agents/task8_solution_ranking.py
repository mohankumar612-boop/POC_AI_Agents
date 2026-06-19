"""
Task 8: Solution Ranking Agent
Selects the best solution from candidates using multi-factor evaluation.
Factors: Similarity · Confidence · Knowledge Match · Risk
"""
import json
import anthropic


def rank_solutions(ticket: dict, client: anthropic.Anthropic) -> dict:
    """
    Ranks solutions by composite score and selects the best fit.
    """
    solutions = ticket.get("discovered_solutions", {}).get("solutions", [])
    retrieval_confidence = ticket.get("knowledge_retrieval", {}).get("retrieval_confidence", 0.5)

    solutions_str = json.dumps(solutions, indent=2)

    system_prompt = f"""You are a Solution Ranking Agent.
Evaluate solutions using these factors:
1. Relevance to the specific issue (30%)
2. KB confidence score (25%)
3. Estimated resolution speed (20%)
4. Risk level (15%)
5. Simplicity for the user (10%)

KB Retrieval Confidence: {retrieval_confidence:.0%}

Return ONLY valid JSON, no markdown:
{{
  "ranked_solutions": [
    {{
      "rank": 1,
      "solution_id": "A/B/C",
      "title": "solution title",
      "composite_score": 0.0-1.0,
      "confidence": 0.0-1.0,
      "ranking_reason": "why ranked here"
    }}
  ],
  "best_solution_id": "A/B/C",
  "best_solution_title": "title",
  "best_solution_steps": ["step1", "step2"],
  "best_solution_confidence": 0.0-1.0,
  "executive_summary": "one sentence recommendation"
}}"""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=768,
        system=system_prompt,
        messages=[{"role": "user", "content": f"""Query: {ticket['query']}
Issue Type: {ticket.get('issue_type', {}).get('issue_type', '')}

Solutions to Rank:
{solutions_str}"""}]
    )
    raw = response.content[0].text.strip().lstrip("```json").lstrip("```").rstrip("```")
    result = json.loads(raw)
    return {**ticket, "solution_ranking": result}
