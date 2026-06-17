# Data Quality Report

**Dataset:** D2C Customer Churn Capstone (Part 1)  
**Snapshot date:** 2025-09-30  
**Universe:** 2,400 customers (`customer_id` is the primary key across one-row-per-customer tables)

---

## Missing Values

| Dataset | Column | Missing % | Notes |
|---------|--------|----------:|-------|
| `customers.csv` | `loyalty_tier` | 57.75% | Customer not enrolled in loyalty programme |
| `customers.csv` | `skin_type` | 16.71% | Optional profile field at signup |
| `orders.csv` (pre-snapshot) | `rating` | 0.71% (58 rows) | Exclude or impute before computing average ratings |
| `web_events_snapshot.csv` | — | 0% | One row per customer; no nulls in activity metrics |
| `churn_labels.csv` | — | 0% | Target and split complete for all 2,400 customers |
| `intervention_history.csv` | — | 0% | Campaign history complete |

**Support tickets:** 1,247 of 2,400 customers have at least one ticket. Absence of tickets is expected, not a join error.

---

## Duplicates & Join Keys

| Check | Result | Recommendation |
|-------|--------|----------------|
| Duplicate `customer_id` in `customers.csv` | 0 | Safe as dimension table |
| Duplicate `order_id` in `orders.csv` | 12 rows with `_DUP` suffix | Treat as duplicate-like records; dedupe or flag before order-level aggregations |
| Left join `customers` → `churn_labels` | 2,400 rows, 0 unmatched | Use `customers` as spine for customer-level EDA |
| Left join `customers` → `web_events_snapshot` | 2,400 rows | Full coverage |
| Left join `customers` → `intervention_history` | 2,400 rows | Full coverage |
| Customers in `tickets_pre` not in `customers` | 0 | Referential integrity holds |

---

## Outliers & Invalid Values

| Issue | Detail | Recommended action |
|-------|--------|-------------------|
| `gross_amount` outliers (IQR 1.5×) | **429** pre-snapshot orders outside [Q1−1.5×IQR, Q3+1.5×IQR]; max **₹24,789.38** | Cap or winsorize for monetary aggregates; investigate top orders manually |
| `_DUP` order IDs | **12** intentional duplicate-like rows | Drop or aggregate one record per true order in Part 2/3 feature builds |
| `discount_pct` | Range 0.0–0.7 | Validate business rules; no negative discounts observed |
| `returned` / `reopened` | Binary 0/1 only | No invalid categorical codes found in audit |

---

## Date & Leakage Risks

| Risk | Count / rule | Guardrail |
|------|----------------|-----------|
| Post-snapshot orders | **1,872** rows with `order_date` > 2025-09-30 | Use `orders_pre` only for RFM and behavioral features |
| Post-snapshot tickets | **0** rows after 2025-09-30 | Ticket file is snapshot-safe |
| Target leakage | `churn_next_60d` in `churn_labels.csv` | Never include as a model feature |
| Split column | `split` in labels | Use for evaluation only, not as a feature |
| Web metrics | Already aggregated for 2025-09-01–2025-09-30 | Safe as snapshot features |

**Leakage rule:** All Part 1 EDA and future modeling features must be computable from data on or before **2025-09-30**.

---

## Recommended Actions for Modeling

1. **Filter orders:** `orders_pre = orders[orders['order_date'] <= '2025-09-30']` before any aggregation.
2. **Deduplicate orders:** Remove or collapse `*_DUP` rows before frequency/monetary calculations.
3. **Handle missing loyalty:** Model as explicit “Not Enrolled” category (57.8% of customers).
4. **Ratings:** Compute `avg_rating` with null-aware aggregation (58 missing order ratings).
5. **Outliers:** Document treatment for `gross_amount` (cap at 99th percentile or IQR fence) in Part 3 model card.
6. **Class imbalance:** Overall churn rate **47.0%** — use precision/recall/F1, not accuracy alone, in Parts 3–4.

---

*Generated from `eda_audit.ipynb` audit cells. Re-run the notebook after any data refresh.*
