"""
Task 1: Query Ingestion Agent
Reads CSV, validates records, standardizes into uniform structure.
Real-world relevance: ServiceNow, Zendesk, Freshdesk
"""
import csv
import io
from typing import Any


def ingest_queries(csv_path: str | None = None, csv_content: str | None = None) -> list[dict[str, Any]]:
    """
    Reads ticket CSV (path or raw content), validates and standardizes records.
    Returns list of standardized ticket dicts.
    """
    rows = []

    if csv_content:
        reader = csv.DictReader(io.StringIO(csv_content))
        for row in reader:
            rows.append(row)
    elif csv_path:
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
    else:
        raise ValueError("Provide either csv_path or csv_content")

    standardized = []
    seen_ids = set()

    for idx, row in enumerate(rows):
        # Normalize field names
        ticket_id = (row.get("ticket_id") or row.get("id") or str(idx + 1)).strip()
        query = (row.get("query") or row.get("description") or row.get("issue") or "").strip()

        # Validate
        if not query:
            continue  # Skip empty queries
        if ticket_id in seen_ids:
            ticket_id = f"{ticket_id}-DUP{idx}"
        seen_ids.add(ticket_id)

        standardized.append({
            "ticket_id": ticket_id,
            "query": query,
            "source": "CSV",
            "status": "open",
            "ingested": True,
        })

    return standardized


def ingest_single_query(query_text: str, ticket_id: str = "MANUAL-001") -> dict[str, Any]:
    """Standardize a single manually entered query."""
    return {
        "ticket_id": ticket_id,
        "query": query_text.strip(),
        "source": "Manual",
        "status": "open",
        "ingested": True,
    }
