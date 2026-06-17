# Part 1 — Data Audit, EDA & Business Understanding

D2C personal-care brand **customer churn intelligence** capstone (Part 1 of 4). This repository audits raw data, explores pre-snapshot behavior vs. churn, and documents data-quality and business findings before modeling.

## Dataset

| File | Description |
|------|-------------|
| `customers.csv` | 2,400 customer profiles |
| `orders.csv` | Order lines (pre- and post-snapshot) |
| `support_tickets.csv` | Support interactions |
| `web_events_snapshot.csv` | 30-day web/app activity at snapshot |
| `churn_labels.csv` | Target `churn_next_60d` + train/val/test split |
| `intervention_history.csv` | Last campaign per customer |

**Snapshot date:** `2025-09-30`  
**Target:** `churn_next_60d` = 1 if no purchase between `2025-10-01` and `2025-11-29`.

### Leakage guardrails

- Use only orders with `order_date <= 2025-09-30` for behavioral features (`orders_pre` in the notebook).
- Do **not** use post-snapshot orders, `churn_next_60d`, or `split` as model inputs.
- See `DATA_DICTIONARY.md` for full column definitions.

## Setup

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

## Run the analysis

```bash
jupyter notebook eda_audit.ipynb
```

Charts are saved under `figures/` when you run the plotting cells. To regenerate figures without Jupyter:

```bash
python execute_eda.py
```

## Repository structure

```
.
├── README.md
├── requirements.txt
├── eda_audit.ipynb              # Main analysis (Phases 1–4)
├── data_quality_report.md       # Data quality audit summary
├── business_memo.md             # Leadership memo
├── DATA_DICTIONARY.md             # Provided schema reference
├── STUDENT_FACING_PROBLEM_STATEMENT.md
├── figures/                     # EDA chart exports (generated)
├── customers.csv
├── orders.csv
├── support_tickets.csv
├── web_events_snapshot.csv
├── churn_labels.csv
└── intervention_history.csv
```

## Key findings (summary)

| Topic | Finding |
|-------|---------|
| Overall churn | ~47% in the 60-day post-snapshot window |
| Recency | >60 days since last order → ~72% churn |
| Engagement | Churned median 3 vs 6 sessions (30d) |
| Channels | Google Search / Instagram ~50% churn; Organic ~40% |
| Returns | Churned customers ~8.2% vs 5.5% return rate |
| Loyalty | Silver / not-enrolled ~48–49% churn; Platinum ~37% |

Five evidence-based hypotheses and six charts are documented in `eda_audit.ipynb`.

## Deliverables checklist (Part 1)

- [x] `eda_audit.ipynb`
- [x] `data_quality_report.md`
- [x] `business_memo.md`
- [x] ≥6 charts (`figures/01`–`06`)
- [x] ≥5 churn hypotheses (notebook + memo)
- [x] `requirements.txt` & `README.md`

## Author notes

**Public repository:** https://github.com/Keshav-Verma-06/d2c-churn-part1-eda

Do not commit secrets, API keys, or machine-specific paths.
