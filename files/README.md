# Agentic AI-Powered Intelligent Issue Resolution Engine

**Document Type:** Proof of Concept (POC)  
**Prepared By:** Logeshwari P  
**Model:** Claude Sonnet 4.6 (Anthropic)

---

## Project Overview

An end-to-end Agentic AI pipeline that resolves IT support tickets through 10 automated tasks —
from CSV ingestion to professional email generation — with zero manual intervention.

## 10-Task Agentic Pipeline

| Task | Agent | Description |
|------|-------|-------------|
| 1 | Query Ingestion | CSV reader + validation + standardization |
| 2 | Semantic Understanding | NLP intent extraction beyond keyword matching |
| 3 | Dynamic Bucketing | Auto-groups issues into 10 broad categories |
| 4 | Issue Type Detection | Identifies precise issue type within bucket |
| 5 | Knowledge Base | 60+ curated issue-solution records |
| 6 | Knowledge Retrieval | Semantic search across KB for similar cases |
| 7 | Solution Discovery | Generates Solution A, B, C options |
| 8 | Solution Ranking | Multi-factor ranking → best solution selected |
| 9 | Risk Assessment | Low / Medium / High risk classification |
| 10 | Email Generation | Professional, tone-adaptive customer email |

## Project Structure

```
agentic_itsm/
├── app.py                          # Streamlit application
├── main.py                         # CLI orchestrator
├── requirements.txt
├── agents/
│   ├── task1_query_ingestion.py
│   ├── task2_semantic_understanding.py
│   ├── task3_dynamic_bucketing.py
│   ├── task4_issue_type_detection.py
│   ├── task5_knowledge_base.py
│   ├── task6_knowledge_retrieval.py
│   ├── task7_solution_discovery.py
│   ├── task8_solution_ranking.py
│   ├── task9_risk_assessment.py
│   └── task10_email_response.py
├── knowledge_base/
│   └── kb_records.py               # 60+ KB records
├── data/
│   ├── tickets_sample.csv
│   └── tickets_100_sample.csv
└── output/                         # JSON results per ticket
```

## Buckets Supported
Authentication · Payment · Upload · Notification · Profile ·
Reporting · System · Search · Support · Account

## Risk Levels
- **Low:** OTP Resend, Password Reset, Cache Clear → Auto-resolve
- **Medium:** Subscription Changes, Refund Requests → Review recommended
- **High:** Account Deletion, Financial Transactions → Human review required

---

## Setup & Deployment

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set API Key
```bash
export ANTHROPIC_API_KEY=your_key_here
```

### 3. Run Streamlit App
```bash
streamlit run app.py
```
Open: http://localhost:8501

### 4. CLI Mode
```bash
python main.py
```

### Deploy to Streamlit Cloud
1. Push this folder to a GitHub repository
2. Go to https://share.streamlit.io
3. Connect your repo, set `app.py` as the main file
4. Add `ANTHROPIC_API_KEY` in Secrets settings
5. Deploy

---

## Success Criteria (per POC Document)
- ✅ Accurate query understanding
- ✅ Effective issue grouping (10 buckets)
- ✅ Correct issue type detection
- ✅ Relevant solution retrieval (60+ KB records)
- ✅ Professional email generation
- ✅ Complete end-to-end workflow demonstration
- ✅ Streamlit Application
- ✅ Risk Assessment
- ✅ CSV Dataset support
