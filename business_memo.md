# Business Memo: Pre-Campaign Investigation Priorities

**To:** Product, Marketing & Customer Support Leadership  
**From:** Analytics — Part 1 Data Audit  
**Date:** June 2026  
**Re:** Retention campaign readiness (snapshot 2025-09-30)

---

## Executive Summary

Roughly **47%** of customers are labeled as churned (no purchase in the 60 days after 2025-09-30). Churn is strongly linked to **purchase recency** and **digital engagement**, not loyalty enrollment alone. Before launching blanket discounts, the company should validate three CRM cohorts: long-inactive buyers, low-session app users, and paid-acquisition customers with high return rates.

---

## Key Data Findings

- **2,400** customers; left joins to labels, web events, and interventions retain all customers (no ID loss).
- **1,872** post-snapshot order rows exist for label construction only — they must not drive campaign targeting features.
- **12** duplicate-like orders (`_DUP`) and **429** high-`gross_amount` outliers need a documented treatment before RFM modeling.
- **57.8%** of customers lack a `loyalty_tier`; Silver tier churn (**48.8%**) is nearly identical to not-enrolled (**48.3%**).
- **11.2%** of churned customers had **zero** web sessions in the last 30 days vs **5.0%** of retained customers.
- Customers whose last visit was **≥30 days** before snapshot show **87.8%** churn (n=516).

---

## Top 3 Churn Drivers (from EDA hypotheses)

1. **Order recency:** Recency **>60 days** → **72.3%** churn (n=1,260) vs **11.7%** when last order was within 30 days (n=699).
2. **Digital disengagement:** Median **3** sessions (churned) vs **6** (retained); long site absence (`last_visit_days_ago` ≥30) aligns with **87.8%** churn.
3. **Acquisition & fulfillment friction:** Google Search / Instagram ~**50%** churn vs Organic **39.8%**; churned customers average **8.2%** return rate vs **5.5%** for retained.

---

## Recommended Investigations Before Campaign Launch

**Priority 1 — CRM validation (recency & engagement)**  
- Export customers with recency **>60 days** and `sessions_30d` ≤3; confirm contactability and last successful delivery.  
- Test a **win-back + browse reminder** pilot (not deep discount) on a 5% holdout.

**Priority 2 — Pilot campaigns by channel**  
- Run separate creatives for **Google Search / Instagram** cohorts vs **Organic / Referral**; measure 30-day repurchase, not email clicks alone.  
- For customers with return rate **>8%**, pair offers with **delivery/quality** follow-up from support.

**Priority 3 — Data gaps to fix**  
- Resolve **`_DUP`** order handling in the warehouse before Part 2 RFM.  
- Enrich **loyalty_tier** for 1,386 unenrolled accounts or stop treating tier as a protection signal.  
- Track **post-campaign** outcomes to close the loop on the 60-day churn definition.

---

## Next Steps

1. Complete Part 2 RFM segmentation using **pre-snapshot orders only**.  
2. Align retention budget to **high-recency-risk + low-engagement** segments first.  
3. Use Part 3 churn model to rank customers within segments; avoid using post-snapshot orders as inputs.

---

*Metrics sourced from `eda_audit.ipynb` (Charts 1–6 and recency bucket table).*
