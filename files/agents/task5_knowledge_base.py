"""
Task 5: Knowledge Base - Access layer for the 60+ record repository.
Used by Tasks 6 and 7 for retrieval and solution discovery.
"""
from knowledge_base.kb_records import KNOWLEDGE_BASE


def get_kb_summary() -> dict:
    """Returns summary statistics of the knowledge base."""
    buckets = {}
    for rec in KNOWLEDGE_BASE:
        b = rec["bucket"]
        buckets[b] = buckets.get(b, 0) + 1
    return {
        "total_records": len(KNOWLEDGE_BASE),
        "buckets": buckets,
        "risk_distribution": {
            "Low": sum(1 for r in KNOWLEDGE_BASE if r["risk_level"] == "Low"),
            "Medium": sum(1 for r in KNOWLEDGE_BASE if r["risk_level"] == "Medium"),
            "High": sum(1 for r in KNOWLEDGE_BASE if r["risk_level"] == "High"),
        }
    }


def search_kb_by_bucket_and_type(bucket: str, issue_type: str) -> list[dict]:
    """Retrieve KB records matching bucket and issue type."""
    results = []
    bucket_lower = bucket.lower()
    issue_lower = issue_type.lower()

    for rec in KNOWLEDGE_BASE:
        rec_bucket = rec["bucket"].lower()
        rec_issue = rec["issue_type"].lower()

        bucket_match = bucket_lower in rec_bucket or rec_bucket in bucket_lower
        issue_match = any(word in rec_issue for word in issue_lower.split() if len(word) > 3)

        if bucket_match or issue_match:
            results.append(rec)

    return results[:5]  # Top 5 matches


def get_all_kb_records() -> list[dict]:
    return KNOWLEDGE_BASE
