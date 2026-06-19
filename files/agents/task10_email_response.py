"""
Task 10: Email Response Generation Agent
Generates professional, customer-facing email responses.
Adapts tone to sentiment, urgency, and risk level.
"""
import json
import anthropic
from datetime import datetime


def generate_email(ticket: dict, client: anthropic.Anthropic) -> dict:
    """
    Generates a professional support email response.
    """
    query = ticket["query"]
    semantic = ticket.get("semantic", {})
    bucket = ticket.get("bucket", {}).get("bucket", "")
    issue_type = ticket.get("issue_type", {}).get("issue_type", "")
    ranking = ticket.get("solution_ranking", {})
    risk = ticket.get("risk_assessment", {})

    best_steps = ranking.get("best_solution_steps", [])
    confidence = ranking.get("best_solution_confidence", 0.8)
    risk_level = risk.get("risk_level", "Low")
    sentiment = semantic.get("sentiment", "neutral")
    urgency = semantic.get("urgency", "medium")
    human_review = risk.get("human_review_required", False)
    ticket_id = ticket.get("ticket_id", "N/A")

    steps_str = "\n".join([f"{i+1}. {s}" for i, s in enumerate(best_steps)]) if best_steps else "Our team will investigate and provide a resolution."

    system_prompt = f"""You are a senior IT Support specialist writing a professional email response.

Rules:
- Tone adaptation: frustrated/angry → extra empathetic; neutral → professional; polite → warm
- If urgency is critical/high: acknowledge immediately
- Use numbered steps for technical instructions
- Include ticket reference, confidence, and next steps
- If human_review_required is True: do NOT include technical steps, just acknowledge and say team will follow up
- Risk Level: {risk_level} - adjust language accordingly
- Current Date: {datetime.now().strftime('%B %d, %Y')}

Return ONLY valid JSON, no markdown:
{{
  "subject": "Re: [Ticket #{ticket_id}] <descriptive subject>",
  "body": "Full professional email body",
  "tone": "empathetic|professional|urgent|friendly"
}}"""

    user_content = f"""Ticket ID: {ticket_id}
Query: {query}
Bucket: {bucket}
Issue Type: {issue_type}
Urgency: {urgency}
Sentiment: {sentiment}
Risk Level: {risk_level}
Human Review Required: {human_review}
Confidence: {confidence:.0%}
Executive Summary: {ranking.get('executive_summary', '')}
Steps:
{steps_str}"""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1500,
        system=system_prompt,
        messages=[{"role": "user", "content": user_content}]
    )
    raw = response.content[0].text.strip().lstrip("```json").lstrip("```").rstrip("```")
    result = json.loads(raw)
    return {**ticket, "email_response": result}
