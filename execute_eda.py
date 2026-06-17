"""Headless runner for eda_audit.ipynb logic (generates figures/)."""
import warnings
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

warnings.filterwarnings("ignore")
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams["figure.figsize"] = (10, 5)
plt.rcParams["figure.dpi"] = 100

BASE_DIR = Path(__file__).parent
FIG_DIR = BASE_DIR / "figures"
FIG_DIR.mkdir(exist_ok=True)
SNAPSHOT = pd.Timestamp("2025-09-30")

customers = pd.read_csv(BASE_DIR / "customers.csv", parse_dates=["signup_date"])
orders = pd.read_csv(BASE_DIR / "orders.csv", parse_dates=["order_date"])
support_tickets = pd.read_csv(BASE_DIR / "support_tickets.csv", parse_dates=["ticket_date"])
web_events = pd.read_csv(BASE_DIR / "web_events_snapshot.csv", parse_dates=["snapshot_date"])
churn_labels = pd.read_csv(BASE_DIR / "churn_labels.csv", parse_dates=["snapshot_date"])
intervention_history = pd.read_csv(BASE_DIR / "intervention_history.csv", parse_dates=["snapshot_date"])

orders_pre = orders[orders["order_date"] <= SNAPSHOT].copy()
tickets_pre = support_tickets[support_tickets["ticket_date"] <= SNAPSHOT].copy()

assert customers["customer_id"].nunique() == 2400
assert len(orders) - len(orders_pre) == 1872

analysis_base = customers.merge(
    churn_labels[["customer_id", "churn_next_60d", "split"]], on="customer_id", how="left"
)
analysis_base = analysis_base.merge(web_events, on="customer_id", how="left")

last_order_date = orders_pre.groupby("customer_id")["order_date"].max().reset_index()
last_order_date["recency_days"] = (SNAPSHOT - last_order_date["order_date"]).dt.days
analysis_base = analysis_base.merge(last_order_date[["customer_id", "recency_days"]], on="customer_id", how="left")
analysis_base["recency_days"] = analysis_base["recency_days"].fillna(999)

order_agg = orders_pre.groupby("customer_id").agg(
    order_count=("order_id", "count"),
    return_rate=("returned", "mean"),
).reset_index()
analysis_base = analysis_base.merge(order_agg, on="customer_id", how="left")
analysis_base["return_rate"] = analysis_base["return_rate"].fillna(0)

# Chart 1
channel_churn = analysis_base.groupby("acquisition_channel", as_index=False).agg(
    churn_rate=("churn_next_60d", "mean"),
    customers=("churn_next_60d", "count"),
)
channel_churn["churn_rate_pct"] = channel_churn["churn_rate"] * 100
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(
    data=channel_churn.sort_values("churn_rate_pct"),
    x="churn_rate_pct",
    y="acquisition_channel",
    ax=ax,
    color="#4C72B0",
)
ax.set_xlabel("Churn rate (%)")
ax.set_ylabel("Acquisition channel")
ax.set_title("Chart 1: 60-day churn rate by acquisition channel")
plt.tight_layout()
plt.savefig(FIG_DIR / "01_churn_by_channel.png", bbox_inches="tight")
plt.close()

# Chart 2
plot_recency = analysis_base[analysis_base["recency_days"] < 400].copy()
plot_recency["churn_label"] = plot_recency["churn_next_60d"].map({0: "Retained", 1: "Churned"})
fig, ax = plt.subplots(figsize=(10, 5))
sns.histplot(data=plot_recency, x="recency_days", hue="churn_label", bins=30, kde=True, element="step", ax=ax)
ax.set_xlabel("Days since last pre-snapshot order")
ax.set_ylabel("Customer count")
ax.set_title("Chart 2: Order recency distribution — churned vs retained")
plt.tight_layout()
plt.savefig(FIG_DIR / "02_recency_by_churn.png", bbox_inches="tight")
plt.close()

# Chart 3
tickets_labeled = tickets_pre.merge(churn_labels[["customer_id", "churn_next_60d"]], on="customer_id")
tickets_labeled["churn_label"] = tickets_labeled["churn_next_60d"].map({0: "Retained", 1: "Churned"})
fig, ax = plt.subplots(figsize=(10, 5))
sns.violinplot(
    data=tickets_labeled,
    x="churn_label",
    y="sentiment_score",
    cut=0,
    ax=ax,
    palette=["#55A868", "#C44E52"],
)
ax.set_xlabel("Churn status (next 60d)")
ax.set_ylabel("Ticket sentiment score")
ax.set_title("Chart 3: Support ticket sentiment — churned vs retained customers")
plt.tight_layout()
plt.savefig(FIG_DIR / "03_sentiment_by_churn.png", bbox_inches="tight")
plt.close()

# Chart 4
analysis_base["churn_label"] = analysis_base["churn_next_60d"].map({0: "Retained", 1: "Churned"})
fig, ax = plt.subplots(figsize=(10, 5))
sns.boxplot(
    data=analysis_base,
    x="churn_label",
    y="sessions_30d",
    ax=ax,
    palette=["#55A868", "#C44E52"],
)
ax.set_xlabel("Churn status (next 60d)")
ax.set_ylabel("Sessions (30d)")
ax.set_title("Chart 4: Web/app sessions in last 30 days vs churn")
plt.tight_layout()
plt.savefig(FIG_DIR / "04_sessions_by_churn.png", bbox_inches="tight")
plt.close()

# Chart 5
return_by_churn = analysis_base.groupby("churn_label")["return_rate"].mean().reset_index()
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(data=return_by_churn, x="churn_label", y="return_rate", ax=ax, palette=["#55A868", "#C44E52"])
ax.set_ylabel("Mean return rate (pre-snapshot orders)")
ax.set_xlabel("Churn status (next 60d)")
ax.set_title("Chart 5: Average order return rate vs churn")
plt.tight_layout()
plt.savefig(FIG_DIR / "05_return_rate_by_churn.png", bbox_inches="tight")
plt.close()

# Chart 6
loyalty_df = analysis_base.copy()
loyalty_df["loyalty_tier"] = loyalty_df["loyalty_tier"].fillna("Not Enrolled")
loyalty_churn = loyalty_df.groupby("loyalty_tier", as_index=False).agg(
    churn_rate=("churn_next_60d", "mean"),
    n=("churn_next_60d", "count"),
)
loyalty_churn["churn_rate_pct"] = loyalty_churn["churn_rate"] * 100
fig, ax = plt.subplots(figsize=(9, 5))
sns.barplot(data=loyalty_churn.sort_values("churn_rate_pct"), x="loyalty_tier", y="churn_rate_pct", ax=ax, color="#8172B2")
ax.set_ylabel("Churn rate (%)")
ax.set_xlabel("Loyalty tier")
ax.set_title("Chart 6: Churn rate by loyalty tier")
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig(FIG_DIR / "06_loyalty_churn.png", bbox_inches="tight")
plt.close()

print("OK: generated", len(list(FIG_DIR.glob("*.png"))), "figures in", FIG_DIR)
