"""
main.py — Agentic AI-Powered Intelligent Issue Resolution Engine
Orchestrates all 10 tasks in sequence:
Task 1: Query Ingestion → Task 2: Semantic Understanding → Task 3: Dynamic Bucketing
→ Task 4: Issue Type Detection → Task 5: KB (resource) → Task 6: Knowledge Retrieval
→ Task 7: Solution Discovery → Task 8: Solution Ranking → Task 9: Risk Assessment
→ Task 10: Email Response Generation
"""
import os
import json
import time
import anthropic
from datetime import datetime

from agents.task1_query_ingestion import ingest_queries, ingest_single_query
from agents.task2_semantic_understanding import understand_query
from agents.task3_dynamic_bucketing import identify_bucket
from agents.task4_issue_type_detection import detect_issue_type
from agents.task5_knowledge_base import get_kb_summary
from agents.task6_knowledge_retrieval import retrieve_knowledge
from agents.task7_solution_discovery import discover_solutions
from agents.task8_solution_ranking import rank_solutions
from agents.task9_risk_assessment import assess_risk
from agents.task10_email_response import generate_email


def run_pipeline(ticket: dict, client: anthropic.Anthropic, verbose: bool = False) -> dict:
    """
    Runs all 10 tasks for a single ticket and returns the enriched result.
    """
    pipeline_start = time.time()
    stages = []

    def log(task_num, task_name, result_key, ticket_state):
        if verbose:
            val = ticket_state.get(result_key, {})
            print(f"  ✓ Task {task_num}: {task_name}")
        return ticket_state

    # Task 1 — already ingested, just pass through
    stages.append(("1", "Query Ingestion", "ingested"))

    # Task 2 — Semantic Understanding
    ticket = understand_query(ticket, client)
    stages.append(("2", "Semantic Understanding", "semantic"))
    if verbose:
        print(f"  ✓ Task 2: Semantic Understanding — Intent: {ticket['semantic'].get('intent')}")

    # Task 3 — Dynamic Bucketing
    ticket = identify_bucket(ticket, client)
    stages.append(("3", "Dynamic Bucketing", "bucket"))
    if verbose:
        print(f"  ✓ Task 3: Dynamic Bucketing — Bucket: {ticket['bucket'].get('bucket')}")

    # Task 4 — Issue Type Detection
    ticket = detect_issue_type(ticket, client)
    stages.append(("4", "Issue Type Detection", "issue_type"))
    if verbose:
        print(f"  ✓ Task 4: Issue Type Detection — Type: {ticket['issue_type'].get('issue_type')}")

    # Task 5 — KB is a resource, no per-ticket call needed

    # Task 6 — Knowledge Retrieval
    ticket = retrieve_knowledge(ticket, client)
    stages.append(("6", "Knowledge Retrieval", "knowledge_retrieval"))
    retrieved_count = len(ticket.get("knowledge_retrieval", {}).get("retrieved", []))
    if verbose:
        print(f"  ✓ Task 6: Knowledge Retrieval — {retrieved_count} KB records matched")

    # Task 7 — Solution Discovery
    ticket = discover_solutions(ticket, client)
    stages.append(("7", "Solution Discovery", "discovered_solutions"))
    sol_count = len(ticket.get("discovered_solutions", {}).get("solutions", []))
    if verbose:
        print(f"  ✓ Task 7: Solution Discovery — {sol_count} solutions generated")

    # Task 8 — Solution Ranking
    ticket = rank_solutions(ticket, client)
    stages.append(("8", "Solution Ranking", "solution_ranking"))
    if verbose:
        best = ticket.get("solution_ranking", {}).get("best_solution_title", "N/A")
        print(f"  ✓ Task 8: Solution Ranking — Best: {best}")

    # Task 9 — Risk Assessment
    ticket = assess_risk(ticket, client)
    stages.append(("9", "Risk Assessment", "risk_assessment"))
    if verbose:
        risk = ticket.get("risk_assessment", {}).get("risk_level", "N/A")
        action = ticket.get("risk_assessment", {}).get("recommended_action", "N/A")
        print(f"  ✓ Task 9: Risk Assessment — Level: {risk} | Action: {action}")

    # Task 10 — Email Response Generation
    ticket = generate_email(ticket, client)
    stages.append(("10", "Email Response Generation", "email_response"))
    if verbose:
        print(f"  ✓ Task 10: Email Response Generated")

    ticket["_pipeline_meta"] = {
        "processed_at": datetime.now().isoformat(),
        "processing_time_seconds": round(time.time() - pipeline_start, 2),
        "stages_completed": len(stages),
        "model": "claude-sonnet-4-6"
    }
    return ticket


def save_result(result: dict, output_dir: str = "output") -> str:
    """Save pipeline result to JSON."""
    os.makedirs(output_dir, exist_ok=True)
    ticket_id = result.get("ticket_id", "unknown")
    filename = f"{output_dir}/{ticket_id}.json"
    with open(filename, "w") as f:
        json.dump(result, f, indent=2)
    return filename


def process_csv(csv_path: str, limit: int = 5, verbose: bool = True) -> list[dict]:
    """
    Process tickets from a CSV file through the full pipeline.
    Limit controls how many tickets to process (default 5 for POC demo).
    """
    client = anthropic.Anthropic()
    tickets = ingest_queries(csv_path=csv_path)
    print(f"\n📥 Ingested {len(tickets)} tickets from {csv_path}")
    print(f"🔄 Processing first {min(limit, len(tickets))} tickets...\n")

    results = []
    for i, ticket in enumerate(tickets[:limit]):
        print(f"\n{'='*60}")
        print(f"🎫 Ticket {i+1}/{min(limit, len(tickets))}: [{ticket['ticket_id']}]")
        print(f"   Query: {ticket['query']}")
        print(f"{'='*60}")
        result = run_pipeline(ticket, client, verbose=verbose)
        results.append(result)
        save_result(result)
        print(f"   ⏱  {result['_pipeline_meta']['processing_time_seconds']}s")

    print(f"\n✅ Processed {len(results)} tickets. Results saved to /output/")
    return results


def process_single(query: str, ticket_id: str = "MANUAL-001", verbose: bool = True) -> dict:
    """Process a single query through the full pipeline."""
    client = anthropic.Anthropic()
    ticket = ingest_single_query(query, ticket_id)
    print(f"\n🎫 Processing: [{ticket_id}]")
    print(f"   Query: {query}")
    print(f"{'='*60}")
    result = run_pipeline(ticket, client, verbose=verbose)
    save_result(result)
    return result


if __name__ == "__main__":
    import sys

    print("╔══════════════════════════════════════════════════════════╗")
    print("║  Agentic AI-Powered Intelligent Issue Resolution Engine  ║")
    print("║       10-Task Pipeline | Claude Sonnet 4.6               ║")
    print("╚══════════════════════════════════════════════════════════╝\n")

    # Show KB summary
    kb = get_kb_summary()
    print(f"📚 Knowledge Base: {kb['total_records']} records across {len(kb['buckets'])} buckets")

    print("\nMode: [1] CSV batch (tickets_sample.csv)  [2] Single query")
    choice = input("Enter 1 or 2: ").strip()

    if choice == "1":
        result = process_csv("data/tickets_sample.csv", limit=3, verbose=True)
    else:
        q = input("Enter your support query: ").strip()
        result = process_single(q, "MANUAL-001", verbose=True)
        r = result
        print(f"\n{'='*60}")
        print(f"📧 EMAIL RESPONSE")
        print(f"{'='*60}")
        print(f"Subject: {r.get('email_response', {}).get('subject', '')}")
        print()
        print(r.get('email_response', {}).get('body', ''))
        print(f"\nRisk Level: {r.get('risk_assessment', {}).get('risk_level', 'N/A')}")
        print(f"Confidence: {r.get('solution_ranking', {}).get('best_solution_confidence', 0):.0%}")
