"""
Task 9: Risk Assessment Agent
Classifies risk level of the recommended solution before sending to customer.
Low: OTP Resend, Password Reset
Medium: Subscription Changes, Refund Requests
High: Account Deletion, Financial Transactions
"""
import json
import anthropic


RISK_FRAMEWORK = {
    "Low": ["OTP Resend", "Password Reset", "Clear Cache", "Resend Email", "Retry Upload", "Refresh Page", "Update Profile"],
    "Medium": ["Subscription Changes", "Refund Requests", "Account Unlock", "Role Assignment", "Webhook Config", "Data Re-import"],
    "High": ["Account Deletion", "Financial Transactions", "Data Migration", "System Restart", "Mass Data Update", "Security Changes"]
}


def assess_risk(ticket: dict, client: anthropic.Anthropic) -> dict:
    """
    Classifies risk level and determines if human review is needed.
    """
    best_solution = ticket.get("solution_ranking", {}).get("best_solution_title", "")
    issue_type = ticket.get("issue_type", {}).get("issue_type", "")
    bucket = ticket.get("bucket", {}).get("bucket", "")

    framework_str = json.dumps(RISK_FRAMEWORK, indent=2)

    system_prompt = f"""You are a Risk Assessment Agent for IT support automation.
Classify the risk of automating this solution response.

Risk Framework:
{framework_str}

Return ONLY valid JSON, no markdown:
{{
  "risk_level": "Low|Medium|High",
  "risk_score": 0.0-1.0,
  "risk_factors": ["list of risk factors identified"],
  "human_review_required": true/false,
  "human_review_reason": "reason or null",
  "auto_resolve_safe": true/false,
  "compliance_flag": "PII|Financial|Security|None",
  "recommended_action": "Auto-resolve|Human-review|Escalate"
}}"""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=512,
        system=system_prompt,
        messages=[{"role": "user", "content": f"""Bucket: {bucket}
Issue Type: {issue_type}
Recommended Solution: {best_solution}
Query: {ticket['query']}"""}]
    )
    raw = response.content[0].text.strip().lstrip("```json").lstrip("```").rstrip("```")
    result = json.loads(raw)
    return {**ticket, "risk_assessment": result}
