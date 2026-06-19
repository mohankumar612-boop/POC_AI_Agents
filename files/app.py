"""
app.py — Streamlit Application
Agentic AI-Powered Intelligent Issue Resolution Engine
Full UI: Single Ticket | CSV Batch | Knowledge Base | Analytics
"""
import os
import sys
import json
import time
import io
import anthropic
import streamlit as st
import pandas as pd
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.task1_query_ingestion import ingest_queries, ingest_single_query
from agents.task5_knowledge_base import get_kb_summary, get_all_kb_records
from knowledge_base.kb_records import BUCKET_LIST
from main import run_pipeline, save_result

# ─────────────────────────────────────────────
# Page Config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Agentic AI Issue Resolution Engine",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# CSS Styling
# ─────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1e3a5f 0%, #2d6a9f 50%, #1a8cbc 100%);
        padding: 2rem 2.5rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        color: white;
    }
    .main-header h1 { color: white; margin: 0; font-size: 2rem; font-weight: 700; }
    .main-header p { color: #b8d4f0; margin: 0.5rem 0 0; font-size: 1rem; }

    .pipeline-stage {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-left: 4px solid #2d6a9f;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        margin: 0.4rem 0;
        font-size: 0.88rem;
    }
    .pipeline-stage.done { border-left-color: #16a34a; background: #f0fdf4; }
    .pipeline-stage.running { border-left-color: #d97706; background: #fffbeb; }

    .metric-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1.2rem;
        text-align: center;
        box-shadow: 0 1px 4px rgba(0,0,0,0.05);
    }
    .metric-card .value { font-size: 2rem; font-weight: 700; color: #1e3a5f; }
    .metric-card .label { font-size: 0.82rem; color: #64748b; margin-top: 0.2rem; }

    .email-box {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1.5rem;
        font-family: 'Courier New', monospace;
        font-size: 0.88rem;
        line-height: 1.6;
        white-space: pre-wrap;
    }

    .risk-low { background:#dcfce7; color:#15803d; padding:4px 12px; border-radius:20px; font-weight:600; font-size:0.85rem; }
    .risk-medium { background:#fef3c7; color:#92400e; padding:4px 12px; border-radius:20px; font-weight:600; font-size:0.85rem; }
    .risk-high { background:#fee2e2; color:#991b1b; padding:4px 12px; border-radius:20px; font-weight:600; font-size:0.85rem; }

    .bucket-badge {
        background: #dbeafe;
        color: #1d4ed8;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 600;
    }
    .confidence-bar-container { background:#e2e8f0; border-radius:4px; height:8px; margin-top:4px; }
    .confidence-bar { background:#2d6a9f; border-radius:4px; height:8px; }

    .step-item {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 0.6rem 1rem;
        margin: 0.3rem 0;
        display: flex;
        align-items: flex-start;
        gap: 0.75rem;
    }
    .step-num {
        background: #2d6a9f;
        color: white;
        border-radius: 50%;
        width: 22px;
        height: 22px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.75rem;
        font-weight: 700;
        flex-shrink: 0;
    }
    div[data-testid="stTabs"] button { font-weight: 600; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────
@st.cache_resource
def get_client():
    return anthropic.Anthropic()


def risk_badge(level: str) -> str:
    cls = {"Low": "risk-low", "Medium": "risk-medium", "High": "risk-high"}.get(level, "risk-low")
    return f'<span class="{cls}">⚠ {level} Risk</span>'


def confidence_html(score: float) -> str:
    pct = int(score * 100)
    color = "#16a34a" if pct >= 80 else "#d97706" if pct >= 60 else "#dc2626"
    return f"""<div style='font-size:0.85rem; color:{color}; font-weight:600;'>{pct}% confidence</div>
<div class='confidence-bar-container'><div class='confidence-bar' style='width:{pct}%; background:{color};'></div></div>"""


def display_result(result: dict):
    """Renders the full pipeline result in Streamlit."""
    ticket_id = result.get("ticket_id", "N/A")
    query = result.get("query", "")
    semantic = result.get("semantic", {})
    bucket = result.get("bucket", {})
    issue = result.get("issue_type", {})
    ranking = result.get("solution_ranking", {})
    risk = result.get("risk_assessment", {})
    email = result.get("email_response", {})
    meta = result.get("_pipeline_meta", {})
    retrieval = result.get("knowledge_retrieval", {})
    solutions = result.get("discovered_solutions", {}).get("solutions", [])

    st.markdown(f"### 🎫 Ticket `{ticket_id}` — Results")
    st.markdown(f"> *{query}*")

    # Summary row
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.metric("Bucket", bucket.get("bucket", "—"))
    with c2:
        st.metric("Issue Type", issue.get("issue_type", "—")[:30] + ("…" if len(issue.get("issue_type",""))>30 else ""))
    with c3:
        st.metric("Urgency", semantic.get("urgency", "—").upper())
    with c4:
        st.metric("Risk Level", risk.get("risk_level", "—"))
    with c5:
        st.metric("Processing", f"{meta.get('processing_time_seconds', 0)}s")

    st.divider()

    col_left, col_right = st.columns([3, 2])

    with col_left:
        # Email
        st.markdown("#### 📧 Generated Email Response")
        subject = email.get("subject", "")
        body = email.get("body", "No email generated.")
        st.markdown(f"**Subject:** `{subject}`")
        st.markdown(f'<div class="email-box">{body}</div>', unsafe_allow_html=True)

        # Download button
        email_text = f"Subject: {subject}\n\n{body}"
        st.download_button(
            "⬇ Download Email",
            data=email_text,
            file_name=f"email_{ticket_id}.txt",
            mime="text/plain",
            use_container_width=True
        )

    with col_right:
        # Semantic
        st.markdown("#### 🔍 Semantic Understanding")
        st.markdown(f"**Intent:** {semantic.get('intent', '—')}")
        st.markdown(f"**Sentiment:** {semantic.get('sentiment', '—').capitalize()}")
        st.markdown(f"**Summary:** {semantic.get('summary', '—')}")
        keywords = semantic.get("keywords", [])
        if keywords:
            kw_html = " ".join([f'<span style="background:#e0e7ff;color:#3730a3;padding:2px 8px;border-radius:12px;font-size:0.8rem;margin:2px;">{k}</span>' for k in keywords])
            st.markdown(f"**Keywords:** {kw_html}", unsafe_allow_html=True)

        st.divider()

        # Bucket & Classification
        st.markdown("#### 🪣 Bucket & Classification")
        b_conf = bucket.get("confidence", 0)
        st.markdown(f"**Bucket:** <span class='bucket-badge'>{bucket.get('bucket', '—')}</span>", unsafe_allow_html=True)
        st.markdown(confidence_html(b_conf), unsafe_allow_html=True)
        st.markdown(f"**Issue Type:** {issue.get('issue_type', '—')}")
        st.markdown(f"*{bucket.get('reasoning', '')}*")

        st.divider()

        # Risk
        st.markdown("#### 🛡 Risk Assessment")
        st.markdown(risk_badge(risk.get("risk_level", "Low")), unsafe_allow_html=True)
        st.markdown(f"**Action:** {risk.get('recommended_action', '—')}")
        if risk.get("human_review_required"):
            st.warning("⚠ Human review required before sending.")
        else:
            st.success("✅ Safe for automated response")

    st.divider()

    # Best Solution Steps
    st.markdown("#### 🏆 Top Ranked Solution")
    st.markdown(f"**{ranking.get('best_solution_title', '—')}**")
    st.markdown(confidence_html(ranking.get("best_solution_confidence", 0)), unsafe_allow_html=True)
    steps = ranking.get("best_solution_steps", [])
    if steps:
        cols = st.columns(min(len(steps), 3))
        for i, step in enumerate(steps):
            with cols[i % 3]:
                st.markdown(f"""<div class='step-item'>
<div class='step-num'>{i+1}</div>
<div style='font-size:0.85rem;'>{step}</div>
</div>""", unsafe_allow_html=True)

    # Discovered Solutions comparison
    if solutions:
        with st.expander("📋 All Discovered Solutions (A / B / C)"):
            sol_cols = st.columns(len(solutions))
            for i, sol in enumerate(solutions):
                with sol_cols[i]:
                    st.markdown(f"**Solution {sol.get('solution_id', i+1)}: {sol.get('title', '')}**")
                    st.caption(f"⏱ {sol.get('estimated_time', 'N/A')}")
                    for step in sol.get("steps", []):
                        st.markdown(f"• {step}")

    # KB Matches
    retrieved = retrieval.get("retrieved", [])
    if retrieved:
        with st.expander(f"📚 Knowledge Base Matches ({len(retrieved)})"):
            for item in retrieved:
                fr = item.get("full_record", {})
                rel = item.get("relevance_score", 0)
                if fr:
                    st.markdown(f"**{fr.get('id')} — {fr.get('issue_type')}** | Relevance: {rel:.0%}")
                    st.markdown(f"*{fr.get('solution', '')}*")
                    st.divider()

    # Raw JSON
    with st.expander("🔧 Raw Pipeline JSON"):
        st.json(result)


# ─────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙ Configuration")
    api_key = st.text_input("Anthropic API Key", type="password",
        value=os.getenv("ANTHROPIC_API_KEY", ""),
        help="Set ANTHROPIC_API_KEY env variable or enter here")
    if api_key:
        os.environ["ANTHROPIC_API_KEY"] = api_key

    st.divider()
    st.markdown("### 📊 Knowledge Base")
    kb_info = get_kb_summary()
    st.metric("Total KB Records", kb_info["total_records"])
    st.metric("Buckets Covered", len(kb_info["buckets"]))

    st.divider()
    st.markdown("### 🏗 Pipeline Stages")
    stages = [
        ("1", "Query Ingestion"),
        ("2", "Semantic Understanding"),
        ("3", "Dynamic Bucketing"),
        ("4", "Issue Type Detection"),
        ("5", "Knowledge Base"),
        ("6", "Knowledge Retrieval"),
        ("7", "Solution Discovery"),
        ("8", "Solution Ranking"),
        ("9", "Risk Assessment"),
        ("10", "Email Generation"),
    ]
    for num, name in stages:
        st.markdown(f"**Task {num}** — {name}")

    st.divider()
    st.caption("🤖 Powered by Claude Sonnet 4.6")
    st.caption("📄 POC — Logeshwari P")


# ─────────────────────────────────────────────
# Main Header
# ─────────────────────────────────────────────
st.markdown("""
<div class="main-header">
  <h1>🤖 Agentic AI-Powered Intelligent Issue Resolution Engine</h1>
  <p>10-Task Agentic Pipeline · Semantic Understanding · Dynamic Bucketing · Risk Assessment · Auto Email Generation</p>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Tabs
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "🎫 Single Ticket",
    "📦 CSV Batch Processing",
    "📚 Knowledge Base",
    "📊 Analytics"
])


# ── TAB 1: Single Ticket ────────────────────
with tab1:
    st.markdown("### Enter a Support Query")
    st.markdown("*Type or paste a customer support ticket to run through the full 10-task AI pipeline.*")

    sample_queries = {
        "Select a sample...": "",
        "Unable to login after password reset": "Unable to login after password reset",
        "OTP not received on registered mobile": "OTP not received on registered mobile number. I tried multiple times.",
        "Payment failed but amount deducted": "I made a payment of $250 but got an error. The amount was deducted from my account but no confirmation received.",
        "Invoice not generated after payment": "Invoice not generated after successful payment. I need it for reimbursement urgently.",
        "Report download failing": "I'm unable to download the monthly sales report. It shows generating but nothing downloads.",
        "Account locked after login attempts": "My account got locked after 3 wrong password attempts. I need access urgently for a presentation.",
        "Image upload not working": "I've been trying to upload my profile picture for hours but it keeps failing with no error message.",
        "Application crashes on startup": "The application crashes every time I open it. Tried reinstalling twice but same issue.",
    }

    selected = st.selectbox("Quick samples:", list(sample_queries.keys()))
    default_query = sample_queries[selected]

    query_text = st.text_area(
        "Support Query",
        value=default_query,
        height=120,
        placeholder="e.g. Unable to login after password reset. I've tried multiple times..."
    )

    ticket_id_input = st.text_input("Ticket ID (optional)", value="TKT-" + datetime.now().strftime("%H%M%S"))

    run_btn = st.button("🚀 Run Full Pipeline", type="primary", use_container_width=True)

    if run_btn:
        if not query_text.strip():
            st.error("Please enter a support query.")
        elif not os.getenv("ANTHROPIC_API_KEY"):
            st.error("Please enter your Anthropic API Key in the sidebar.")
        else:
            client = get_client()
            ticket = ingest_single_query(query_text, ticket_id_input)

            # Progress display
            progress_container = st.container()
            with progress_container:
                st.markdown("#### 🔄 Running Pipeline...")
                progress = st.progress(0)
                status_text = st.empty()

                task_labels = [
                    "Task 1: Query Ingestion ✓",
                    "Task 2: Semantic Understanding...",
                    "Task 3: Dynamic Bucketing...",
                    "Task 4: Issue Type Detection...",
                    "Task 5: Knowledge Base (loaded) ✓",
                    "Task 6: Knowledge Retrieval...",
                    "Task 7: Solution Discovery...",
                    "Task 8: Solution Ranking...",
                    "Task 9: Risk Assessment...",
                    "Task 10: Email Generation...",
                ]

                # Run with stage-by-stage progress via callbacks
                from agents.task2_semantic_understanding import understand_query
                from agents.task3_dynamic_bucketing import identify_bucket
                from agents.task4_issue_type_detection import detect_issue_type
                from agents.task6_knowledge_retrieval import retrieve_knowledge
                from agents.task7_solution_discovery import discover_solutions
                from agents.task8_solution_ranking import rank_solutions
                from agents.task9_risk_assessment import assess_risk
                from agents.task10_email_response import generate_email

                def upd(step, label):
                    progress.progress(step / 10)
                    status_text.markdown(f"**{label}**")

                upd(1, task_labels[0])
                upd(2, task_labels[1])
                ticket = understand_query(ticket, client)

                upd(3, task_labels[2])
                ticket = identify_bucket(ticket, client)

                upd(4, task_labels[3])
                ticket = detect_issue_type(ticket, client)

                upd(5, task_labels[4])
                upd(6, task_labels[5])
                ticket = retrieve_knowledge(ticket, client)

                upd(7, task_labels[6])
                ticket = discover_solutions(ticket, client)

                upd(8, task_labels[7])
                ticket = rank_solutions(ticket, client)

                upd(9, task_labels[8])
                ticket = assess_risk(ticket, client)

                upd(10, task_labels[9])
                ticket = generate_email(ticket, client)
                ticket["_pipeline_meta"] = {
                    "processed_at": datetime.now().isoformat(),
                    "processing_time_seconds": "—",
                    "model": "claude-sonnet-4-6"
                }

                progress.progress(1.0)
                status_text.markdown("**✅ Pipeline Complete!**")

            save_result(ticket)
            st.success("✅ All 10 tasks completed successfully!")
            st.divider()
            display_result(ticket)


# ── TAB 2: CSV Batch ─────────────────────────
with tab2:
    st.markdown("### Batch Process Tickets from CSV")
    st.markdown("Upload a CSV with `ticket_id` and `query` columns, or use the sample dataset.")

    col_upload, col_sample = st.columns([2, 1])
    with col_upload:
        uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
    with col_sample:
        st.markdown("**Or use sample data:**")
        use_sample = st.button("📁 Load tickets_sample.csv")
        use_100 = st.button("📁 Load tickets_100_sample.csv")

    csv_content = None
    csv_label = ""

    if uploaded_file:
        csv_content = uploaded_file.read().decode("utf-8")
        csv_label = uploaded_file.name
    elif use_sample:
        with open("data/tickets_sample.csv") as f:
            csv_content = f.read()
        csv_label = "tickets_sample.csv"
    elif use_100:
        with open("data/tickets_100_sample.csv") as f:
            csv_content = f.read()
        csv_label = "tickets_100_sample.csv"

    if csv_content:
        tickets_raw = ingest_queries(csv_content=csv_content)
        st.success(f"✅ Loaded **{len(tickets_raw)} tickets** from `{csv_label}`")

        df_preview = pd.DataFrame(tickets_raw)[["ticket_id", "query"]]
        st.dataframe(df_preview, use_container_width=True, height=200)

        limit = st.slider("Tickets to process (API calls per ticket ≈ 8):", 1, min(10, len(tickets_raw)), 3)

        if st.button("🚀 Process Selected Tickets", type="primary"):
            if not os.getenv("ANTHROPIC_API_KEY"):
                st.error("Please enter your Anthropic API Key in the sidebar.")
            else:
                client = get_client()
                batch_results = []
                overall_progress = st.progress(0)
                result_containers = []

                for i, ticket in enumerate(tickets_raw[:limit]):
                    st.markdown(f"---\n#### 🎫 [{i+1}/{limit}] Ticket `{ticket['ticket_id']}`")
                    st.caption(f"*{ticket['query']}*")

                    with st.spinner(f"Running pipeline for ticket {ticket['ticket_id']}..."):
                        result = run_pipeline(ticket, client, verbose=False)
                        save_result(result)
                        batch_results.append(result)

                    # Quick summary
                    r = result
                    c1, c2, c3, c4 = st.columns(4)
                    with c1:
                        st.metric("Bucket", r.get("bucket", {}).get("bucket", "—"))
                    with c2:
                        st.metric("Issue Type", (r.get("issue_type", {}).get("issue_type", "—"))[:25])
                    with c3:
                        st.metric("Risk", r.get("risk_assessment", {}).get("risk_level", "—"))
                    with c4:
                        st.metric("Confidence", f"{r.get('solution_ranking', {}).get('best_solution_confidence', 0):.0%}")

                    with st.expander("📧 View Email Response"):
                        st.markdown(f"**{r.get('email_response', {}).get('subject', '')}**")
                        st.text(r.get('email_response', {}).get('body', ''))

                    overall_progress.progress((i + 1) / limit)

                # Summary table
                st.divider()
                st.markdown("### 📊 Batch Summary")
                summary_data = []
                for r in batch_results:
                    summary_data.append({
                        "Ticket ID": r.get("ticket_id"),
                        "Query": r.get("query", "")[:60] + "…",
                        "Bucket": r.get("bucket", {}).get("bucket", "—"),
                        "Issue Type": r.get("issue_type", {}).get("issue_type", "—"),
                        "Urgency": r.get("semantic", {}).get("urgency", "—"),
                        "Risk": r.get("risk_assessment", {}).get("risk_level", "—"),
                        "Action": r.get("risk_assessment", {}).get("recommended_action", "—"),
                        "Confidence": f"{r.get('solution_ranking', {}).get('best_solution_confidence', 0):.0%}",
                    })
                df_summary = pd.DataFrame(summary_data)
                st.dataframe(df_summary, use_container_width=True)

                # Download results
                csv_out = df_summary.to_csv(index=False)
                st.download_button("⬇ Download Summary CSV", csv_out, "batch_results.csv", "text/csv")

                json_out = json.dumps(batch_results, indent=2)
                st.download_button("⬇ Download Full JSON", json_out, "batch_results.json", "application/json")


# ── TAB 3: Knowledge Base ────────────────────
with tab3:
    st.markdown("### 📚 Knowledge Base Repository")
    kb_summary = get_kb_summary()

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="metric-card"><div class="value">{kb_summary["total_records"]}</div><div class="label">Total Records</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card"><div class="value">{len(kb_summary["buckets"])}</div><div class="label">Buckets</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-card"><div class="value">{kb_summary["risk_distribution"]["Low"]}</div><div class="label">Low Risk</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="metric-card"><div class="value">{kb_summary["risk_distribution"]["High"]}</div><div class="label">High Risk</div></div>', unsafe_allow_html=True)

    st.divider()

    # Filters
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        bucket_filter = st.selectbox("Filter by Bucket", ["All"] + BUCKET_LIST)
    with col_f2:
        risk_filter = st.selectbox("Filter by Risk", ["All", "Low", "Medium", "High"])

    records = get_all_kb_records()
    if bucket_filter != "All":
        records = [r for r in records if r["bucket"] == bucket_filter]
    if risk_filter != "All":
        records = [r for r in records if r["risk_level"] == risk_filter]

    st.markdown(f"**Showing {len(records)} records**")

    for rec in records:
        with st.expander(f"**{rec['id']}** — {rec['issue_type']} ({rec['bucket']})"):
            col_a, col_b = st.columns([3, 1])
            with col_a:
                st.markdown(f"**Solution:** {rec['solution']}")
                if rec.get("steps"):
                    st.markdown("**Steps:**")
                    for i, s in enumerate(rec["steps"], 1):
                        st.markdown(f"{i}. {s}")
                st.caption(f"*Notes: {rec.get('notes', '')}*")
            with col_b:
                st.markdown(risk_badge(rec["risk_level"]), unsafe_allow_html=True)
                st.metric("Confidence", f"{rec['confidence']:.0%}")
                st.metric("Avg Resolution", rec.get("avg_resolution_time", "N/A"))


# ── TAB 4: Analytics ─────────────────────────
with tab4:
    st.markdown("### 📊 Pipeline Analytics & KB Insights")

    kb_sum = get_kb_summary()

    # Bucket distribution
    st.markdown("#### Knowledge Base — Bucket Distribution")
    bucket_df = pd.DataFrame(list(kb_sum["buckets"].items()), columns=["Bucket", "Records"])
    bucket_df = bucket_df.sort_values("Records", ascending=False)
    st.bar_chart(bucket_df.set_index("Bucket"))

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Risk Distribution")
        risk_df = pd.DataFrame(list(kb_sum["risk_distribution"].items()), columns=["Risk Level", "Count"])
        st.bar_chart(risk_df.set_index("Risk Level"))

    with col2:
        st.markdown("#### KB Confidence by Bucket")
        records = get_all_kb_records()
        bucket_conf = {}
        for r in records:
            b = r["bucket"]
            if b not in bucket_conf:
                bucket_conf[b] = []
            bucket_conf[b].append(r["confidence"])
        avg_conf = {b: round(sum(v) / len(v) * 100, 1) for b, v in bucket_conf.items()}
        conf_df = pd.DataFrame(list(avg_conf.items()), columns=["Bucket", "Avg Confidence %"])
        st.bar_chart(conf_df.set_index("Bucket"))

    # Output files
    st.divider()
    st.markdown("#### 📁 Processed Ticket Results")
    output_dir = "output"
    if os.path.exists(output_dir):
        files = [f for f in os.listdir(output_dir) if f.endswith(".json")]
        if files:
            st.markdown(f"**{len(files)} tickets processed** — stored in `/output/`")
            results_data = []
            for fname in files:
                with open(os.path.join(output_dir, fname)) as f:
                    r = json.load(f)
                results_data.append({
                    "Ticket ID": r.get("ticket_id"),
                    "Query": r.get("query", "")[:50],
                    "Bucket": r.get("bucket", {}).get("bucket", "—"),
                    "Issue Type": r.get("issue_type", {}).get("issue_type", "—"),
                    "Risk": r.get("risk_assessment", {}).get("risk_level", "—"),
                    "Confidence": f"{r.get('solution_ranking', {}).get('best_solution_confidence', 0):.0%}",
                    "Processed At": r.get("_pipeline_meta", {}).get("processed_at", "—")[:19],
                })
            st.dataframe(pd.DataFrame(results_data), use_container_width=True)
        else:
            st.info("No tickets processed yet. Use the Single Ticket or CSV Batch tab.")
    else:
        st.info("No output directory yet. Process a ticket to see results here.")

    # POC Info
    st.divider()
    st.markdown("""
#### 📋 POC Information
| Item | Detail |
|------|--------|
| **Document Type** | Proof of Concept (POC) |
| **Prepared By** | Logeshwari P |
| **Model** | Claude Sonnet 4.6 |
| **Tasks** | 10 Agentic Tasks |
| **KB Records** | 60+ curated records |
| **Buckets** | Authentication, Payment, Upload, Notification, Profile, Reporting, System, Search, Support, Account |
| **Risk Levels** | Low · Medium · High |
| **Output** | Email + JSON per ticket |
""")
